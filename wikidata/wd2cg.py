#!/usr/bin/python
"""make causegraph based on wikidata JSON dump"""

from __future__ import absolute_import, division, print_function

import json
import os
import pprint
import subprocess
import sys
from collections import Counter

import networkx as nx
from networkx.drawing.nx_pydot import write_dot

from wd_constants import (all_times, cg_rels, combined_inverses,
                          fictional_items, lang_order, likely_nonspecific)


def get_label(obj):
    """get appropriate label, using language fallback chain"""
    has_sitelinks = 'sitelinks' in obj
    for lang in lang_order:
        site = lang + 'wiki'
        if has_sitelinks and site in obj['sitelinks']:
            return obj['sitelinks'][site]['title']
        elif lang in obj['labels']:
            return obj['labels'][lang]['value']
    return None


def get_date_claims(claims, props):
    """get date claims in the specified collection of properties"""
    result = []
    for claim in claims:
        if claim in props:
            for spec in claims[claim]:
                if 'time' in spec['mainsnak'].get('datavalue', {}).get(
                        'value', {}):
                    date = spec['mainsnak']['datavalue']['value']['time']
                    result.append([claim, date])
    return result


# (though I'll have to get more precise in the future, for modern-day stuff)
def dates_to_years(claims):
    """grab usable years from wikidata dates, to inform CauseGraph layout"""
    years = {}
    for item in claims:
        earliest_year = sys.maxsize
        for c in claims[item]:
            try:
                # example date: '+2014-10-14T00:00:00Z'
                # so split on '-' (but only the two on the right, so rsplit 2)
                # and take the first
                year = int(c[1].rsplit('-', 2)[0])
                if year < earliest_year:
                    earliest_year = year
            except Exception as e:
                print("error on", item, '-', e.message)
        if earliest_year < 10000 and earliest_year > -10000:
            years[item] = earliest_year
    return years


def is_real(qid, claims):
    """check for claims that an item is fictional"""
    if 'P31' in claims:
        for spec in claims['P31']:
            if 'id' in spec['mainsnak'].get('datavalue', {}).get('value', {}):
                thing = spec['mainsnak']['datavalue']['value']['id']
                if thing in fictional_items:
                    return False
    elif 'P279' in claims:
        for spec in claims['P279']:
            if 'id' in spec['mainsnak'].get('datavalue', {}).get('value', {}):
                thing = spec['mainsnak']['datavalue']['value']['id']
                if thing in fictional_items and qid not in fictional_items:
                    print("new fictional class:", qid)
                    return False

    # we don't actually know it's real, but it isn't labeled as fictional
    return True


def check_claims(qid, claim, claim_set):
    spec_stmts = []
    other_qids = []
    for spec in claim_set:
        if 'id' in spec['mainsnak'].get('datavalue', {}).get('value', {}):
            other_qid = spec['mainsnak']['datavalue']['value']['id']
            other_qids.append(other_qid)
            spec_stmts.append(qid + ' ' + claim + ' ' + other_qid)
    return spec_stmts, other_qids


def process_dump(dump_path):
    nodes = set()
    date_claims = {}
    labels = {}
    statements = []

    # collect statements of interest
    # TODO optimize this - there *has* to be a way
    with open(dump_path) as infile:
        infile.readline()
        for line in infile:
            try:
                obj = json.loads(line.rstrip(',\n'))
                qid = obj['id']

                if qid not in labels:
                    obj_label = get_label(obj)
                    if obj_label is not None:
                        labels[qid] = obj_label

                is_item = obj['type'] == 'item'
                real_claims = 'claims' in obj and is_real(qid, obj['claims'])
                if is_item and real_claims:
                    claims = obj['claims']
                    cg_rel_claims = [c for c in claims if c in cg_rels]
                    item_dates = [c for c in claims if c in all_times]

                    if cg_rel_claims:
                        nodes.add(qid)
                    if item_dates and (qid not in date_claims):
                        date_claims[qid] = get_date_claims(claims, all_times)

                    for claim in cg_rel_claims:
                        spec_stmts, other_qids = check_claims(
                            qid, claim, claims[claim])
                        nodes.update(other_qids)
                        statements += spec_stmts
            except Exception as e:
                if line != ']\n':
                    print("*** Exception", type(e), "-", e.message,
                          "on following line:")
                    print(line)

    return nodes, date_claims, labels, statements


def write_statements(statements, path):
    """write file containing list of statements/relationships"""
    with open(path, 'w') as csvfile:
        for item in statements:
            csvfile.write("%s\n" % item)


def write_items_json(items, path):
    with open(path, 'w') as itemsfile:
        itemsfile.write(json.dumps(items, indent=True))


def translate_statements(statements, labels):
    """translate statements to natural language with labels"""
    statements_en = []
    for statement in statements:
        splitup = statement.split()
        new_statement = []
        for item in splitup:
            try:
                new_statement.append(labels[item])
            except Exception:
                print("*** Exception: no label for", item)
                new_statement.append(item)
        statements_en.append(' '.join(new_statement))


def write_neo4j_nodes(nodes, labels):
    """write nodes to file for neo4j-import or neo4j-admin import"""
    # TODO switch to item header with year in it
    # future_item_header = ':ID\tname\tyear:int\t:LABEL\n'
    item_header = ':ID\tname\t:LABEL\n'
    with open('nodes.tsv', 'w') as nodesfile:
        nodesfile.write(item_header)
        for node in nodes:
            label = labels[node] if node in labels else node
            # TODO stop hardcoding "Article"; use "instance of" or something
            line = "%s\t|%s|\tArticle\n" % (node, label)
            try:
                nodesfile.write(line.encode('utf-8'))
            except Exception:
                print("exception writing to neo4j node file:", node)


def write_neo4j_rels(statements, labels):
    rel_header = ':START_ID\t:END_ID\t:TYPE\n'
    with open('relationships.tsv', 'w') as relsfile:
        relsfile.write(rel_header)
        for statement in statements:
            splitup = statement.split()
            relsfile.write("%s\t%s\t%s\n" % (splitup[0], splitup[2],
                                             splitup[1]))


def make_nx_graph(statements, labels, years=None):
    # TODO: make sure this works in python 3
    g = nx.MultiDiGraph()
    for line in statements:
        try:
            splitup = line.strip().split()
            if splitup[0] in labels:
                source = labels[splitup[0]].encode('utf-8')
            else:
                source = splitup[0]
            if splitup[2] in labels:
                destination = labels[splitup[2]].encode('utf-8')
            else:
                destination = splitup[2]
            if years is not None:
                if splitup[0] in years:
                    g.add_node(source, year=years[splitup[0]])
                if splitup[2] in years:
                    g.add_node(destination, year=years[splitup[2]])
            g.add_edge(source, destination, type=splitup[1])
        except Exception:
            print("error on line:", line)
    return g


def make_qid_nx_graph(statements, years=None):
    g = nx.MultiDiGraph()
    for line in statements:
        try:
            splitup = line.strip().split()
            source = splitup[0]
            destination = splitup[2]
            if years is not None:
                if splitup[0] in years:
                    g.add_node(source, year=years[splitup[0]])
                if splitup[2] in years:
                    g.add_node(destination, year=years[splitup[2]])
            g.add_edge(source, destination, type=splitup[1])
        except Exception:
            print("error on line:", line)
    return g


def graph_report(nxgraph):
    """report graph statistics, violations of rules/constraints, etc."""
    def edge_type(e):
        edge_data = nxgraph.get_edge_data(*e)
        return edge_data.get(0, {}).get('type', None)

    report = {}
    report['node_count'] = nxgraph.number_of_nodes()
    report['edge_count'] = nxgraph.number_of_edges()
    report['rel_stats'] = Counter([edge_type(e) for e in nxgraph.edges()])
    report['selfloops'] = nxgraph.nodes_with_selfloops()
    # TODO parents born after "children", or maybe died before (although...)
    # TODO people "influenced by" others who weren't alive yet (at most, people
    # would be influenced by the idea of such a person existing)
    # TODO identical reciprocal relationships that can't happen (or maybe are
    #  unlikely and/or indicate a likely misuse of a property)
    # TODO check other constraints of the various cg_rels
    return report


def direct(statement):
    """ensure that a statement is pointing in the right direction, for purposes
    of labeling and checking based on in-degree and out-degree"""
    splitup = statement.split()
    if splitup[1] in combined_inverses:
        return (splitup[2] + ' ' + combined_inverses[splitup[1]] + ' ' +
                splitup[0])
    else:
        return statement


def dedupe_and_direct(statements):
    """create a set of unique statements oriented in the same direction"""
    print('starting dedupe_and_direct with', len(statements), 'statements')
    result = {direct(s) for s in statements}
    print('finishing dedupe_and_direct with', len(result), 'statements')
    return result


def specific_only(statements, years):
    """return the subset of statements for which at least one end of a causal
    statement has a time specified"""

    def is_specific(statement):
        splitup = statement.split()
        likely = splitup[1] in likely_nonspecific
        if likely and splitup[0] not in years and splitup[2] not in years:
            return False
        else:
            return True

    return {statement for statement in statements if is_specific(statement)}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dump_path = sys.argv[1]
    else:
        dump_path = 'latest-all.json'

    nodes, date_claims, labels, statements = process_dump(dump_path)
    years = dates_to_years(date_claims)
    unique_statements = dedupe_and_direct(statements)
    statements_final = specific_only(unique_statements, years)

    write_statements(statements, 'statements.txt')
    write_statements(unique_statements, 'unique_statements.txt')
    write_statements(statements_final, 'statements_final.txt')
    write_items_json(labels, 'wd_labels.json')
    write_items_json(date_claims, 'date_claims.json')
    write_items_json(years, 'wd_years.json')

    # TODO use deduped statements here?
    write_neo4j_nodes(nodes, labels)
    write_neo4j_rels(statements, labels)

    nxgraph = make_qid_nx_graph(statements_final, years=years)
    graph_report = graph_report(nxgraph)
    pprint.pprint(graph_report)
    write_dot(nxgraph, 'nxcg.dot')