from __future__ import absolute_import, division, print_function

# language fallback chain; get labels in the first language that works
# the goal being to provide readable labels
lang_order = ('en', 'de', 'fr', 'es', 'it', 'pl', 'pt', 'nl', 'sv', 'no', 'fi',
              'ro')

cg_rels = {
    'P737': 'influenced by',
    'P941': 'inspired by',
    'P2675': 'reply to',
    'P144': 'based on',
    'P828': 'has cause',
    'P1542': 'cause of',
    'P1478': 'has immediate cause',
    'P1536': 'immediate cause of',
    'P1479': 'has contributing factor',
    'P1537': 'contributing factor of',
    'P22': 'father',
    'P25': 'mother',
    'P40': 'child',
    'P184': 'doctoral advisor',
    'P185': 'doctoral student',
    'P1066': 'student of',
    'P802': 'student'
}

# if a statement using one of these doesn't have a date on either end,
# then it's probably something like "ethanol cause of ethanol exposure",
# which isn't suitable for CauseGraph.  TODO: Filter that stuff.
likely_nonspecific = frozenset(
    ['P828', 'P1542', 'P1478', 'P1536', 'P1479', 'P1537'])

# these aren't that great, would need lots of filtering
# 'P509': 'cause of death', 'P770': 'cause of destruction',

# there's also P523 and P524 for 'temporal range' for e.g. dinosaurs

# TODO get subproperties for times below; you're still missing some
# TODO use earliest and latest when present with an unknown date

starts = {
    'P580': 'start time',
    'P571': 'inception',
    'P569': 'date of birth',
    'P575': 'time of discovery',
    'P1191': 'first performance',
    'P577': 'publication date',
    'P2031': 'work period (start)',
    'P1619': 'date of official opening'
}

ends = {
    'P582': 'end time',
    'P576': 'dissolved, abolished or demolished',
    'P570': 'date of death',
    'P2032': 'work period (end)'
}

others = {
    'P793': 'significant event',
    'P585': 'point in time',
    'P1317': 'floruit'
}

all_times = frozenset(list(starts.keys()) + list(ends.keys()) + list(others.keys()))

# these inverse relationships are present in Wikidata
original_inverses = {
    'P22': 'P40',  # father/mother more specific
    'P25': 'P40',
    'P828': 'P1542',
    # 'P828': 'P1536',  # both listed as inverses? not sure it makes sense
    'P184': 'P185',
    'P1066': 'P802',
    'P1478': 'P1536',
    'P1479': 'P1537'
}

combined_inverses = {
    'P22': 'P40',  # "father of"
    'P25': 'P40',  # "mother of"
    'P737': 'P737i',  # "influenced"
    'P941': 'P941i',  # "inspired"
    'P2675': 'P2675i',  # "received reply"
    'P144': 'P144i',  # "basis of"
    'P828': 'P1542',
    'P184': 'P185',
    'P1066': 'P802',
    'P1478': 'P1536',
    'P1479': 'P1537'
}

fictional_items = frozenset([
    'Q190', 'Q3465', 'Q5476', 'Q7246', 'Q7559', 'Q8028', 'Q9406', 'Q9410',
    'Q12581', 'Q14138', 'Q15830', 'Q16375', 'Q17304', 'Q19839', 'Q19842',
    'Q19873', 'Q19879', 'Q19884', 'Q19885', 'Q19913', 'Q20052', 'Q20069',
    'Q32884', 'Q34358', 'Q41511', 'Q45529', 'Q45713', 'Q46721', 'Q48444',
    'Q51724', 'Q51771', 'Q51785', 'Q51796', 'Q51805', 'Q52377', 'Q52383',
    'Q54230', 'Q54289', 'Q55515', 'Q56437', 'Q66016', 'Q74359', 'Q74574',
    'Q78493', 'Q78498', 'Q81741', 'Q83090', 'Q83203', 'Q95074', 'Q101609',
    'Q102059', 'Q108636', 'Q109411', 'Q110660', 'Q110910', 'Q117482',
    'Q126351', 'Q128430', 'Q128458', 'Q129264', 'Q129866', 'Q130223',
    'Q131087', 'Q131156', 'Q134154', 'Q138840', 'Q146083', 'Q146978',
    'Q148057', 'Q148401', 'Q150986', 'Q152402', 'Q152519', 'Q154224',
    'Q162244', 'Q163709', 'Q164896', 'Q165510', 'Q165938', 'Q168827',
    'Q172451', 'Q174396', 'Q175255', 'Q177413', 'Q178342', 'Q178885',
    'Q180262', 'Q180287', 'Q180774', 'Q181291', 'Q181360', 'Q181414',
    'Q182037', 'Q182406', 'Q182559', 'Q184353', 'Q185569', 'Q186350',
    'Q188215', 'Q188784', 'Q190125', 'Q190327', 'Q191192', 'Q191796',
    'Q192032', 'Q194061', 'Q194077', 'Q201411', 'Q202474', 'Q203904',
    'Q205985', 'Q207041', 'Q207174', 'Q208167', 'Q208255', 'Q208361',
    'Q208446', 'Q214045', 'Q215605', 'Q215972', 'Q220453', 'Q221726',
    'Q222573', 'Q223194', 'Q235113', 'Q235157', 'Q236429', 'Q239872',
    'Q242663', 'Q244392', 'Q245204', 'Q246882', 'Q247297', 'Q247617',
    'Q247683', 'Q253026', 'Q259065', 'Q259745', 'Q273112', 'Q273320',
    'Q276453', 'Q281525', 'Q283024', 'Q290460', 'Q290562', 'Q290691',
    'Q305561', 'Q308661', 'Q308697', 'Q314806', 'Q321335', 'Q334425',
    'Q334794', 'Q335140', 'Q335179', 'Q336237', 'Q337935', 'Q338688',
    'Q340152', 'Q370547', 'Q373916', 'Q379032', 'Q385582', 'Q386208',
    'Q388924', 'Q392643', 'Q403964', 'Q428531', 'Q430551', 'Q433664',
    'Q440831', 'Q451147', 'Q460998', 'Q465434', 'Q466466', 'Q466470',
    'Q466830', 'Q468388', 'Q473165', 'Q473285', 'Q476682', 'Q478535',
    'Q479033', 'Q479165', 'Q485205', 'Q494382', 'Q494511', 'Q503186',
    'Q504377', 'Q511056', 'Q524158', 'Q527525', 'Q528820', 'Q533242',
    'Q537513', 'Q556947', 'Q559618', 'Q564946', 'Q565368', 'Q578380',
    'Q578584', 'Q580733', 'Q581450', 'Q582566', 'Q588296', 'Q595421',
    'Q595703', 'Q603432', 'Q608582', 'Q611361', 'Q615532', 'Q619300',
    'Q620744', 'Q621431', 'Q621460', 'Q624083', 'Q625320', 'Q627323',
    'Q628612', 'Q629060', 'Q631406', 'Q633799', 'Q634195', 'Q637245',
    'Q639891', 'Q642405', 'Q646049', 'Q652985', 'Q654361', 'Q657473',
    'Q657670', 'Q657957', 'Q660531', 'Q672799', 'Q677763', 'Q678418',
    'Q686623', 'Q690175', 'Q692111', 'Q715822', 'Q716204', 'Q716534',
    'Q718580', 'Q719506', 'Q719935', 'Q720378', 'Q721221', 'Q721683',
    'Q721838', 'Q724417', 'Q725249', 'Q728388', 'Q730052', 'Q740379',
    'Q740881', 'Q741961', 'Q742360', 'Q743931', 'Q747737', 'Q748994',
    'Q752184', 'Q752542', 'Q759746', 'Q778556', 'Q780650', 'Q782181',
    'Q782935', 'Q804258', 'Q816795', 'Q819381', 'Q819669', 'Q819684',
    'Q823310', 'Q823351', 'Q829590', 'Q830248', 'Q830493', 'Q835987',
    'Q841818', 'Q842127', 'Q842697', 'Q843824', 'Q844432', 'Q844479',
    'Q844794', 'Q845053', 'Q845294', 'Q845696', 'Q847723', 'Q850660',
    'Q853255', 'Q853329', 'Q853715', 'Q854827', 'Q855123', 'Q858784',
    'Q868442', 'Q878099', 'Q886778', 'Q890402', 'Q897028', 'Q897229',
    'Q897918', 'Q904183', 'Q917362', 'Q920028', 'Q922942', 'Q924827',
    'Q925144', 'Q926190', 'Q929799', 'Q933971', 'Q937840', 'Q940109',
    'Q940138', 'Q940713', 'Q967226', 'Q977690', 'Q979507', 'Q987803',
    'Q989255', 'Q989888', 'Q996004', 'Q997848', 'Q1018644', 'Q1018749',
    'Q1020115', 'Q1047698', 'Q1048023', 'Q1050285', 'Q1050486', 'Q1050840',
    'Q1051330', 'Q1053366', 'Q1055292', 'Q1055307', 'Q1056850', 'Q1056876',
    'Q1057701', 'Q1059791', 'Q1062234', 'Q1062345', 'Q1063470', 'Q1064669',
    'Q1065663', 'Q1067836', 'Q1068765', 'Q1070638', 'Q1071580', 'Q1073343',
    'Q1073785', 'Q1076022', 'Q1076157', 'Q1077257', 'Q1086098', 'Q1087392',
    'Q1088986', 'Q1089054', 'Q1094617', 'Q1095530', 'Q1100491', 'Q1107241',
    'Q1108464', 'Q1113875', 'Q1114461', 'Q1122064', 'Q1124812', 'Q1125911',
    'Q1126085', 'Q1130152', 'Q1130518', 'Q1132049', 'Q1132238', 'Q1133563',
    'Q1133632', 'Q1134605', 'Q1136342', 'Q1136607', 'Q1138561', 'Q1140626',
    'Q1141550', 'Q1142281', 'Q1144339', 'Q1145276', 'Q1146055', 'Q1149537',
    'Q1149649', 'Q1150212', 'Q1150640', 'Q1152040', 'Q1153462', 'Q1156741',
    'Q1157625', 'Q1165928', 'Q1168065', 'Q1178242', 'Q1186933', 'Q1187635',
    'Q1187704', 'Q1188443', 'Q1190089', 'Q1198159', 'Q1207630', 'Q1222779',
    'Q1226311', 'Q1228667', 'Q1234666', 'Q1235772', 'Q1236181', 'Q1247809',
    'Q1249918', 'Q1250520', 'Q1251283', 'Q1255488', 'Q1255927', 'Q1261621',
    'Q1262613', 'Q1266031', 'Q1274180', 'Q1293747', 'Q1294900', 'Q1307329',
    'Q1311613', 'Q1317575', 'Q1321618', 'Q1325707', 'Q1325848', 'Q1326372',
    'Q1326754', 'Q1341149', 'Q1346442', 'Q1347516', 'Q1361380', 'Q1365947',
    'Q1368147', 'Q1370621', 'Q1377489', 'Q1379405', 'Q1381762', 'Q1387388',
    'Q1395190', 'Q1397757', 'Q1402016', 'Q1402155', 'Q1406822', 'Q1408706',
    'Q1409501', 'Q1410962', 'Q1412386', 'Q1412790', 'Q1414963', 'Q1416066',
    'Q1424792', 'Q1427313', 'Q1434313', 'Q1460155', 'Q1460798', 'Q1462606',
    'Q1472233', 'Q1473823', 'Q1483833', 'Q1492735', 'Q1506107', 'Q1520864',
    'Q1528409', 'Q1532556', 'Q1544627', 'Q1547161', 'Q1549047', 'Q1569167',
    'Q1569856', 'Q1574094', 'Q1580954', 'Q1587839', 'Q1601710', 'Q1605251',
    'Q1621322', 'Q1628701', 'Q1636104', 'Q1646179', 'Q1647092', 'Q1647099',
    'Q1647221', 'Q1649366', 'Q1651438', 'Q1654422', 'Q1657782', 'Q1659605',
    'Q1700422', 'Q1709306', 'Q1750329', 'Q1750900', 'Q1750998', 'Q1751361',
    'Q1752151', 'Q1752154', 'Q1752601', 'Q1761892', 'Q1771133', 'Q1771804',
    'Q1771860', 'Q1774273', 'Q1776453', 'Q1783949', 'Q1786347', 'Q1792372',
    'Q1798461', 'Q1800601', 'Q1805119', 'Q1831952', 'Q1838844', 'Q1852689',
    'Q1865902', 'Q1870313', 'Q1872715', 'Q1878695', 'Q1879888', 'Q1885489',
    'Q1886894', 'Q1903444', 'Q1907582', 'Q1916821', 'Q1932138', 'Q1936706',
    'Q1938640', 'Q1958128', 'Q1964689', 'Q1965565', 'Q1966805', 'Q1969230',
    'Q1969604', 'Q1972451', 'Q1972868', 'Q1975114', 'Q1978113', 'Q1996036',
    'Q1999796', 'Q2000106', 'Q2006573', 'Q2014788', 'Q2027417', 'Q2032847',
    'Q2035494', 'Q2036243', 'Q2043034', 'Q2043389', 'Q2053305', 'Q2056639',
    'Q2068284', 'Q2069999', 'Q2070080', 'Q2074025', 'Q2074728', 'Q2075930',
    'Q2083347', 'Q2086998', 'Q2087138', 'Q2088628', 'Q2089060', 'Q2093615',
    'Q2095353', 'Q2107711', 'Q2113005', 'Q2115739', 'Q2120119', 'Q2126491',
    'Q2128806', 'Q2141342', 'Q2156379', 'Q2159960', 'Q2160362', 'Q2160472',
    'Q2165091', 'Q2166642', 'Q2182453', 'Q2193253', 'Q2210089', 'Q2211604',
    'Q2229858', 'Q2235021', 'Q2239243', 'Q2239518', 'Q2248485', 'Q2249508',
    'Q2253424', 'Q2256412', 'Q2259848', 'Q2264398', 'Q2265058', 'Q2266278',
    'Q2266831', 'Q2287182', 'Q2288847', 'Q2291541', 'Q2292021', 'Q2292783',
    'Q2292830', 'Q2294716', 'Q2295955', 'Q2299282', 'Q2302504', 'Q2304007',
    'Q2308429', 'Q2309875', 'Q2311829', 'Q2324677', 'Q2330255', 'Q2331347',
    'Q2331666', 'Q2332499', 'Q2333502', 'Q2335769', 'Q2338879', 'Q2339078',
    'Q2349384', 'Q2354107', 'Q2358328', 'Q2369882', 'Q2370441', 'Q2373676',
    'Q2380428', 'Q2385451', 'Q2402310', 'Q2405545', 'Q2422387', 'Q2427597',
    'Q2437812', 'Q2444451', 'Q2447475', 'Q2448831', 'Q2452634', 'Q2455773',
    'Q2457508', 'Q2458837', 'Q2460831', 'Q2467613', 'Q2470052', 'Q2470538',
    'Q2471355', 'Q2472713', 'Q2473303', 'Q2474636', 'Q2477725', 'Q2479076',
    'Q2479507', 'Q2480489', 'Q2481679', 'Q2485700', 'Q2496279', 'Q2497303',
    'Q2501934', 'Q2509384', 'Q2517292', 'Q2517599', 'Q2521850', 'Q2524477',
    'Q2527857', 'Q2537344', 'Q2537829', 'Q2539287', 'Q2541568', 'Q2541847',
    'Q2543227', 'Q2545452', 'Q2547846', 'Q2550974', 'Q2551561', 'Q2556757',
    'Q2561222', 'Q2570664', 'Q2577796', 'Q2588730', 'Q2590445', 'Q2593744',
    'Q2606266', 'Q2607197', 'Q2610332', 'Q2615371', 'Q2616282', 'Q2619342',
    'Q2623733', 'Q2630136', 'Q2630558', 'Q2630686', 'Q2633918', 'Q2633927',
    'Q2636437', 'Q2639049', 'Q2646546', 'Q2658345', 'Q2658888', 'Q2671523',
    'Q2700354', 'Q2705874', 'Q2708585', 'Q2711905', 'Q2713362', 'Q2715082',
    'Q2717759', 'Q2721184', 'Q2737172', 'Q2738053', 'Q2738246', 'Q2738581',
    'Q2740163', 'Q2753115', 'Q2754375', 'Q2755014', 'Q2755612', 'Q2775969',
    'Q2783522', 'Q2784080', 'Q2784317', 'Q2801524', 'Q2803468', 'Q2803758',
    'Q2819123', 'Q2821703', 'Q2827210', 'Q2834778', 'Q2835056', 'Q2839930',
    'Q2840352', 'Q2840769', 'Q2846066', 'Q2859386', 'Q2871786', 'Q2890129',
    'Q2891866', 'Q2892336', 'Q2915835', 'Q2916976', 'Q2917692', 'Q2927327',
    'Q2927431', 'Q2928121', 'Q2928475', 'Q2934676', 'Q2961426', 'Q2962906',
    'Q2962925', 'Q2969329', 'Q2972851', 'Q2977779', 'Q2979768', 'Q2991805',
    'Q2998321', 'Q3002683', 'Q3003193', 'Q3003194', 'Q3008212', 'Q3015692',
    'Q3027575', 'Q3027597', 'Q3028813', 'Q3030758', 'Q3032311', 'Q3034813',
    'Q3036206', 'Q3036932', 'Q3038541', 'Q3049532', 'Q3050815', 'Q3051190',
    'Q3058816', 'Q3059255', 'Q3071490', 'Q3077255', 'Q3077746', 'Q3087542',
    'Q3094480', 'Q3109521', 'Q3109899', 'Q3116728', 'Q3123281', 'Q3125960',
    'Q3140581', 'Q3143655', 'Q3143966', 'Q3174429', 'Q3196369', 'Q3217335',
    'Q3228303', 'Q3234352', 'Q3236334', 'Q3238123', 'Q3241867', 'Q3244549',
    'Q3246774', 'Q3246821', 'Q3247351', 'Q3248946', 'Q3249581', 'Q3249740',
    'Q3250794', 'Q3253065', 'Q3253086', 'Q3263954', 'Q3265302', 'Q3267861',
    'Q3267913', 'Q3268032', 'Q3268330', 'Q3273210', 'Q3274408', 'Q3275517',
    'Q3275581', 'Q3275872', 'Q3287136', 'Q3296155', 'Q3301944', 'Q3303128',
    'Q3304744', 'Q3312360', 'Q3316552', 'Q3335069', 'Q3335212', 'Q3339527',
    'Q3346693', 'Q3348159', 'Q3352887', 'Q3356199', 'Q3356597', 'Q3358427',
    'Q3359656', 'Q3375719', 'Q3375722', 'Q3375726', 'Q3375761', 'Q3375984',
    'Q3388498', 'Q3389608', 'Q3393456', 'Q3396544', 'Q3403565', 'Q3409401',
    'Q3410535', 'Q3413976', 'Q3414453', 'Q3433708', 'Q3434376', 'Q3437937',
    'Q3446340', 'Q3474751', 'Q3491164', 'Q3492104', 'Q3492920', 'Q3498598',
    'Q3504142', 'Q3504206', 'Q3506363', 'Q3516425', 'Q3521824', 'Q3522530',
    'Q3526162', 'Q3526964', 'Q3538741', 'Q3539838', 'Q3541421', 'Q3542731',
    'Q3550383', 'Q3553321', 'Q3553329', 'Q3556272', 'Q3567065', 'Q3570103',
    'Q3572302', 'Q3588756', 'Q3589107', 'Q3589148', 'Q3590870', 'Q3601279',
    'Q3622170', 'Q3634804', 'Q3640883', 'Q3649279', 'Q3655456', 'Q3656814',
    'Q3658341', 'Q3683506', 'Q3694884', 'Q3699744', 'Q3699748', 'Q3704791',
    'Q3706151', 'Q3707571', 'Q3708018', 'Q3735738', 'Q3745984', 'Q3750416',
    'Q3750425', 'Q3750888', 'Q3752974', 'Q3753909', 'Q3753924', 'Q3754255',
    'Q3758946', 'Q3759592', 'Q3771604', 'Q3772698', 'Q3775000', 'Q3775002',
    'Q3775957', 'Q3778311', 'Q3782442', 'Q3783895', 'Q3786070', 'Q3815021',
    'Q3825492', 'Q3831861', 'Q3834302', 'Q3834368', 'Q3834377', 'Q3834378',
    'Q3834387', 'Q3834434', 'Q3834458', 'Q3842925', 'Q3855553', 'Q3855874',
    'Q3859469', 'Q3870124', 'Q3873406', 'Q3873407', 'Q3874316', 'Q3879085',
    'Q3879313', 'Q3885647', 'Q3895768', 'Q3900216', 'Q3900257', 'Q3900420',
    'Q3900455', 'Q3900481', 'Q3930941', 'Q3931823', 'Q3932529', 'Q3943941',
    'Q3951734', 'Q3959879', 'Q3962172', 'Q3962332', 'Q3966183', 'Q3966468',
    'Q3967406', 'Q3968288', 'Q3968289', 'Q3968291', 'Q3968293', 'Q3972967',
    'Q3972970', 'Q3977640', 'Q3979554', 'Q3997384', 'Q3998527', 'Q4003173',
    'Q4003311', 'Q4006563', 'Q4008465', 'Q4011059', 'Q4023335', 'Q4056406',
    'Q4058003', 'Q4071774', 'Q4086886', 'Q4096043', 'Q4111219', 'Q4119683',
    'Q4128201', 'Q4137843', 'Q4141731', 'Q4206741', 'Q4222484', 'Q4228437',
    'Q4233121', 'Q4235016', 'Q4241789', 'Q4251777', 'Q4258797', 'Q4258825',
    'Q4271324', 'Q4272028', 'Q4272038', 'Q4281243', 'Q4316005', 'Q4318321',
    'Q4319923', 'Q4327996', 'Q4335750', 'Q4336983', 'Q4348996', 'Q4359224',
    'Q4359230', 'Q4378475', 'Q4388180', 'Q4390702', 'Q4397403', 'Q4418079',
    'Q4436935', 'Q4449663', 'Q4454486', 'Q4463225', 'Q4464511', 'Q4525327',
    'Q4532179', 'Q4537764', 'Q4538908', 'Q4686758', 'Q4690705', 'Q4698551',
    'Q4736579', 'Q4736592', 'Q4739380', 'Q4747416', 'Q4759471', 'Q4762337',
    'Q4774440', 'Q4787327', 'Q4789398', 'Q4793435', 'Q4801075', 'Q4803091',
    'Q4833247', 'Q4849602', 'Q4854809', 'Q4917693', 'Q4952170', 'Q4986144',
    'Q4995044', 'Q5053017', 'Q5073812', 'Q5073837', 'Q5098353', 'Q5102249',
    'Q5156303', 'Q5160063', 'Q5173143', 'Q5175225', 'Q5185942', 'Q5187727',
    'Q5199354', 'Q5199884', 'Q5210747', 'Q5221580', 'Q5223537', 'Q5234795',
    'Q5256232', 'Q5288845', 'Q5304649', 'Q5304654', 'Q5305337', 'Q5305345',
    'Q5312223', 'Q5359353', 'Q5368029', 'Q5375389', 'Q5402595', 'Q5408769',
    'Q5418464', 'Q5446120', 'Q5446561', 'Q5446565', 'Q5446570', 'Q5446571',
    'Q5446573', 'Q5446574', 'Q5446575', 'Q5446577', 'Q5459401', 'Q5463565',
    'Q5474944', 'Q5509838', 'Q5533603', 'Q5551095', 'Q5557393', 'Q5557475',
    'Q5562337', 'Q5565083', 'Q5574746', 'Q5575807', 'Q5580462', 'Q5580712',
    'Q5609593', 'Q5638490', 'Q5641605', 'Q5641611', 'Q5647910', 'Q5666568',
    'Q5682593', 'Q5723622', 'Q5725560', 'Q5742800', 'Q5752079', 'Q5764991',
    'Q5766954', 'Q5769264', 'Q5790485', 'Q5797488', 'Q5816092', 'Q5874604',
    'Q5876727', 'Q5887925', 'Q5891887', 'Q5893346', 'Q5912461', 'Q5913245',
    'Q5928932', 'Q5928934', 'Q5928936', 'Q5939065', 'Q5960757', 'Q5960957',
    'Q5962290', 'Q5966658', 'Q5985368', 'Q6005514', 'Q6017045', 'Q6019476',
    'Q6029519', 'Q6032338', 'Q6033495', 'Q6034141', 'Q6037755', 'Q6041439',
    'Q6049607', 'Q6053638', 'Q6070836', 'Q6092436', 'Q6103015', 'Q6110908',
    'Q6130553', 'Q6131444', 'Q6133222', 'Q6133514', 'Q6138702', 'Q6138715',
    'Q6150892', 'Q6389420', 'Q6407573', 'Q6424471', 'Q6436283', 'Q6461198',
    'Q6470816', 'Q6471709', 'Q6498903', 'Q6503347', 'Q6527819', 'Q6543175',
    'Q6549417', 'Q6560621', 'Q6571966', 'Q6604094', 'Q6619391', 'Q6619693',
    'Q6619719', 'Q6619729', 'Q6619802', 'Q6623509', 'Q6623809', 'Q6630667',
    'Q6631812', 'Q6636192', 'Q6639573', 'Q6664756', 'Q6667893', 'Q6672460',
    'Q6674339', 'Q6680208', 'Q6692423', 'Q6704725', 'Q6742819', 'Q6742856',
    'Q6748179', 'Q6804478', 'Q6808352', 'Q6819084', 'Q6863432', 'Q6869122',
    'Q6899808', 'Q6912019', 'Q6935446', 'Q6949149', 'Q6949155', 'Q6967817',
    'Q7040846', 'Q7051385', 'Q7071194', 'Q7080259', 'Q7113356', 'Q7113796',
    'Q7132715', 'Q7180622', 'Q7181605', 'Q7187284', 'Q7200341', 'Q7248127',
    'Q7254930', 'Q7290203', 'Q7301562', 'Q7302723', 'Q7308032', 'Q7317883',
    'Q7332305', 'Q7365208', 'Q7382755', 'Q7419514', 'Q7442290', 'Q7448531',
    'Q7460258', 'Q7463279', 'Q7468941', 'Q7474061', 'Q7474647', 'Q7474818',
    'Q7477723', 'Q7482125', 'Q7495423', 'Q7502903', 'Q7503864', 'Q7515806',
    'Q7524666', 'Q7534379', 'Q7536905', 'Q7539070', 'Q7540385', 'Q7542241',
    'Q7572579', 'Q7578018', 'Q7581665', 'Q7601947', 'Q7643449', 'Q7644616',
    'Q7674899', 'Q7692543', 'Q7692627', 'Q7698940', 'Q7703309', 'Q7709448',
    'Q7798117', 'Q7798389', 'Q7805266', 'Q7832314', 'Q7882980', 'Q7886513',
    'Q7887205', 'Q7912957', 'Q7918367', 'Q7941901', 'Q7983240', 'Q7983268',
    'Q7983270', 'Q7999637', 'Q8014790', 'Q8036370', 'Q8036570', 'Q8045321',
    'Q8053031', 'Q8075880', 'Q8076927', 'Q8247410', 'Q8328506', 'Q8458384',
    'Q8458627', 'Q8770760', 'Q9030509', 'Q9051280', 'Q9051700', 'Q9062190',
    'Q9076777', 'Q9078666', 'Q9078668', 'Q9197420', 'Q9198291', 'Q9274099',
    'Q9281624', 'Q9286954', 'Q9298900', 'Q9300083', 'Q9303881', 'Q9328551',
    'Q9362102', 'Q9368323', 'Q10261131', 'Q10270932', 'Q10290417',
    'Q10290691', 'Q10294005', 'Q10298203', 'Q10313095', 'Q10314610',
    'Q10314696', 'Q10329177', 'Q10351134', 'Q10385917', 'Q10395041',
    'Q10405146', 'Q10420711', 'Q10540811', 'Q10556460', 'Q10567373',
    'Q10592812', 'Q10599132', 'Q10690571', 'Q10725720', 'Q10729490',
    'Q10750731', 'Q10752596', 'Q10752909', 'Q10843084', 'Q10856762',
    'Q10856764', 'Q10857773', 'Q10857997', 'Q10878611', 'Q10923898',
    'Q10953847', 'Q11050647', 'Q11298393', 'Q11301630', 'Q11310550',
    'Q11321874', 'Q11338744', 'Q11566978', 'Q11595976', 'Q11631135',
    'Q11675186', 'Q11687022', 'Q11688446', 'Q11705365', 'Q11705366',
    'Q11705495', 'Q11821507', 'Q11827646', 'Q11853643', 'Q11886341',
    'Q11905176', 'Q11954120', 'Q11988051', 'Q11996080', 'Q12000499',
    'Q12050670', 'Q12084330', 'Q12105592', 'Q12150414', 'Q12164049',
    'Q12176345', 'Q12271627', 'Q12275535', 'Q12275537', 'Q12287702',
    'Q12293367', 'Q12322669', 'Q12334344', 'Q12358473', 'Q12372870',
    'Q12405827', 'Q12481383', 'Q12649774', 'Q12669048', 'Q12713690',
    'Q12787150', 'Q12791197', 'Q12793659', 'Q12793666', 'Q12806365',
    'Q12907069', 'Q12964959', 'Q13099528', 'Q13114416', 'Q13403607',
    'Q13405593', 'Q13417132', 'Q13418047', 'Q13518413', 'Q13533319',
    'Q13534353', 'Q13627710', 'Q13634582', 'Q14136353', 'Q14401963',
    'Q14421408', 'Q14494199', 'Q14514600', 'Q14589648', 'Q14623646',
    'Q14637321', 'Q14752002', 'Q14831768', 'Q14897293', 'Q14904358',
    'Q14905896', 'Q14906746', 'Q14917741', 'Q15053464', 'Q15135719',
    'Q15141715', 'Q15238535', 'Q15295645', 'Q15295660', 'Q15298195',
    'Q15298221', 'Q15298259', 'Q15304430', 'Q15306849', 'Q15331236',
    'Q15632617', 'Q15642557', 'Q15690029', 'Q15698310', 'Q15698333',
    'Q15698359', 'Q15702752', 'Q15706911', 'Q15707521', 'Q15707532',
    'Q15707563', 'Q15707583', 'Q15708422', 'Q15709963', 'Q15709969',
    'Q15710942', 'Q15711870', 'Q15720564', 'Q15720567', 'Q15720625',
    'Q15720641', 'Q15720793', 'Q15720870', 'Q15720873', 'Q15728054',
    'Q15731071', 'Q15731648', 'Q15736052', 'Q15773317', 'Q15773347',
    'Q15780329', 'Q15795874', 'Q15796005', 'Q15812741', 'Q15820363',
    'Q15831457', 'Q15831596', 'Q15831598', 'Q15832079', 'Q15838659',
    'Q15839082', 'Q15909505', 'Q15912682', 'Q16010250', 'Q16077793',
    'Q16101952', 'Q16141399', 'Q16153191', 'Q16219295', 'Q16236249',
    'Q16252321', 'Q16256201', 'Q16326794', 'Q16338046', 'Q16363493',
    'Q16363579', 'Q16387027', 'Q16500104', 'Q16513639', 'Q16513881',
    'Q16513904', 'Q16514343', 'Q16515166', 'Q16520001', 'Q16521098',
    'Q16558082', 'Q16568497', 'Q16594772', 'Q16632615', 'Q16640151',
    'Q16648953', 'Q16655677', 'Q16658189', 'Q16658194', 'Q16669523',
    'Q16694396', 'Q16697870', 'Q16705798', 'Q16705943', 'Q16708006',
    'Q16798524', 'Q16827266', 'Q16844807', 'Q16850199', 'Q16864745',
    'Q16884104', 'Q16888407', 'Q16933879', 'Q16957922', 'Q16959276',
    'Q16963820', 'Q16963825', 'Q16992350', 'Q17000743', 'Q17001361',
    'Q17004377', 'Q17029379', 'Q17059194', 'Q17094399', 'Q17097794',
    'Q17145824', 'Q17174370', 'Q17176222', 'Q17176955', 'Q17198419',
    'Q17199338', 'Q17297775', 'Q17305127', 'Q17364638', 'Q17412519',
    'Q17412582', 'Q17412916', 'Q17413155', 'Q17424291', 'Q17424312',
    'Q17427986', 'Q17428218', 'Q17468125', 'Q17478752', 'Q17480821',
    'Q17480830', 'Q17480853', 'Q17480908', 'Q17486927', 'Q17560936',
    'Q17564712', 'Q17624054', 'Q17624058', 'Q17627659', 'Q17636505',
    'Q17636534', 'Q17682891', 'Q17709301', 'Q18011126', 'Q18011131',
    'Q18011141', 'Q18011146', 'Q18011202', 'Q18011336', 'Q18019775',
    'Q18029370', 'Q18032959', 'Q18039177', 'Q18039300', 'Q18058299',
    'Q18086661', 'Q18086665', 'Q18086666', 'Q18086667', 'Q18086671',
    'Q18089574', 'Q18089575', 'Q18099930', 'Q18100125', 'Q18120271',
    'Q18205610', 'Q18229458', 'Q18230293', 'Q18237053', 'Q18275259',
    'Q18298271', 'Q18325582', 'Q18327510', 'Q18327525', 'Q18340183',
    'Q18340294', 'Q18341292', 'Q18352980', 'Q18370757', 'Q18379832',
    'Q18379871', 'Q18381143', 'Q18396311', 'Q18463561', 'Q18507190',
    'Q18533645', 'Q18533896', 'Q18544860', 'Q18555735', 'Q18563354',
    'Q18563360', 'Q18572946', 'Q18596004', 'Q18596079', 'Q18610047',
    'Q18616317', 'Q18670171', 'Q18683244', 'Q18697071', 'Q18706995',
    'Q18710467', 'Q18713194', 'Q18810260', 'Q18814068', 'Q18889352',
    'Q18889371', 'Q18889411', 'Q18889701', 'Q18913069', 'Q18922463',
    'Q18948595', 'Q19324463', 'Q19374571', 'Q19593537', 'Q19594644',
    'Q19594662', 'Q19595246', 'Q19595266', 'Q19656546', 'Q19657408',
    'Q19708268', 'Q19709295', 'Q19760060', 'Q19791817', 'Q19826142',
    'Q19826161', 'Q19826163', 'Q19833563', 'Q19833595', 'Q19838071',
    'Q19838114', 'Q19838115', 'Q19844540', 'Q19844542', 'Q19856510',
    'Q19857028', 'Q19896979', 'Q19915253', 'Q19943557', 'Q20005020',
    'Q20011098', 'Q20037067', 'Q20080483', 'Q20085850', 'Q20086260',
    'Q20086263', 'Q20089147', 'Q20098682', 'Q20101877', 'Q20102242',
    'Q20107434', 'Q20110896', 'Q20167498', 'Q20203727', 'Q20203735',
    'Q20280384', 'Q20354077', 'Q20529153', 'Q20530221', 'Q20552059',
    'Q20604277', 'Q20631508', 'Q20643955', 'Q20666461', 'Q20667393',
    'Q20668295', 'Q20671864', 'Q20723931', 'Q20750954', 'Q20751022',
    'Q20790614', 'Q20790847', 'Q20814410', 'Q20828805', 'Q20830276',
    'Q20853453', 'Q20871196', 'Q20902363', 'Q20950064', 'Q20962530',
    'Q20965826', 'Q21005194', 'Q21009653', 'Q21009670', 'Q21009825',
    'Q21009831', 'Q21009855', 'Q21011318', 'Q21015525', 'Q21029220',
    'Q21088131', 'Q21130120', 'Q21130150', 'Q21190845', 'Q21191150',
    'Q21192416', 'Q21192430', 'Q21192438', 'Q21192474', 'Q21286623',
    'Q21451536', 'Q21451754', 'Q21480268', 'Q21501357', 'Q21501360',
    'Q21505007', 'Q21505200', 'Q21548091', 'Q21561303', 'Q21593141',
    'Q21597574', 'Q21720598', 'Q21779750', 'Q21780594', 'Q21856103',
    'Q21976118', 'Q22011935', 'Q22074477', 'Q22074483', 'Q22442629',
    'Q22442634', 'Q22813672', 'Q22813674', 'Q22815043', 'Q22906376',
    'Q22988604', 'Q22989102', 'Q23010327', 'Q23015914', 'Q23015925',
    'Q23090938', 'Q23542216', 'Q23955658', 'Q24267081', 'Q24284226',
    'Q24286894', 'Q24286897', 'Q24296329', 'Q24334299', 'Q24334685',
    'Q24334893', 'Q24334976', 'Q24335044', 'Q24335536', 'Q24335595',
    'Q24335742', 'Q24335796', 'Q24336031', 'Q24336068', 'Q24336341',
    'Q24336466', 'Q24336490', 'Q24336550', 'Q24336784', 'Q24337077',
    'Q24337101', 'Q24434794', 'Q24515688', 'Q24533670', 'Q24534061',
    'Q24541613', 'Q24541873', 'Q24542467', 'Q24542476', 'Q24560679',
    'Q24565470', 'Q24565488', 'Q24565968', 'Q24573088', 'Q24573232',
    'Q24574658', 'Q24577122', 'Q24577840', 'Q24577895', 'Q24577906',
    'Q24630543', 'Q24649035', 'Q24652348', 'Q24653904', 'Q24654004',
    'Q24668252', 'Q24668264', 'Q24668268', 'Q24668282', 'Q24702845',
    'Q24717924', 'Q24718207', 'Q24718226', 'Q24718264', 'Q24718382',
    'Q24841318', 'Q25336664', 'Q25338401', 'Q25378225', 'Q25545648',
    'Q25707067', 'Q25810847', 'Q25885414', 'Q25930490', 'Q25930493',
    'Q25930495', 'Q25930498', 'Q25930532', 'Q25930653', 'Q25930717',
    'Q25930719', 'Q25930733', 'Q25930740', 'Q25930744', 'Q25930752',
    'Q25930757', 'Q25930759', 'Q25930806', 'Q25930811', 'Q25930813',
    'Q25930814', 'Q25991640', 'Q26051996', 'Q26085597', 'Q26215116',
    'Q26273842', 'Q26700453', 'Q26714783', 'Q26714784', 'Q26714841',
    'Q26728105', 'Q26897926', 'Q26898569', 'Q26924395', 'Q26954987',
    'Q27055917', 'Q27104330', 'Q27104461', 'Q27104473', 'Q27104489',
    'Q27104510', 'Q27115727', 'Q27116566', 'Q27118406', 'Q27118793',
    'Q27120684', 'Q27120778', 'Q27121162', 'Q27121348', 'Q27121407',
    'Q27121443', 'Q27132946', 'Q27145256', 'Q27145814', 'Q27147375',
    'Q27147479', 'Q27147738', 'Q27147769', 'Q27148238', 'Q27148339',
    'Q27149557', 'Q27149727', 'Q27180948', 'Q27189873', 'Q27229763',
    'Q27229996', 'Q27230132', 'Q27230195', 'Q27242186', 'Q27267085',
    'Q27272451', 'Q27276270', 'Q27276405', 'Q27277631', 'Q27301047',
    'Q27301300', 'Q27301420', 'Q27301467', 'Q27301864', 'Q27302054',
    'Q27302146', 'Q27303676', 'Q27303706', 'Q27303776', 'Q27303890',
    'Q27303911', 'Q27303980', 'Q27304409', 'Q27304428', 'Q27304565',
    'Q27304634', 'Q27304713', 'Q27305032', 'Q27430110', 'Q27430202',
    'Q27437572', 'Q27480045', 'Q27491055', 'Q27493204', 'Q27493488',
    'Q27493788', 'Q27506244', 'Q27534557', 'Q27555137', 'Q27556043',
    'Q27556708', 'Q27556771', 'Q27564320', 'Q27598544', 'Q27623618',
    'Q27653431', 'Q27654639', 'Q27666239', 'Q27680988', 'Q27681726',
    'Q27687433', 'Q27689085', 'Q27713372', 'Q27825487', 'Q27826502',
    'Q27862048', 'Q27863646', 'Q27870157', 'Q27892737', 'Q27913316',
    'Q27920423', 'Q27921916', 'Q27924370', 'Q27924374', 'Q27924377',
    'Q27924383', 'Q27924386', 'Q27924389', 'Q27924973', 'Q27925170',
    'Q27926245', 'Q27926250', 'Q27926256', 'Q27926261', 'Q27926262',
    'Q27926263', 'Q27926883', 'Q27926935', 'Q27926938', 'Q27926939',
    'Q27926942', 'Q27926943', 'Q27926970', 'Q27927515', 'Q27927522',
    'Q27927527', 'Q27927530', 'Q27927534', 'Q27927537', 'Q27927541',
    'Q27927544', 'Q27927548', 'Q27927549', 'Q27927551', 'Q27927554',
    'Q27927560', 'Q27927568', 'Q27928369', 'Q27928377', 'Q27928381',
    'Q27955757', 'Q27955772', 'Q27973511', 'Q27977946', 'Q27990795',
    'Q28018927', 'Q28020127', 'Q28031512', 'Q28035102', 'Q28035625',
    'Q28061934', 'Q28061975', 'Q28100286', 'Q28121026', 'Q28146473',
    'Q28240858', 'Q28468092', 'Q28555642', 'Q28599528', 'Q28647546',
    'Q28813646', 'Q28842757', 'Q28872880', 'Q28933526', 'Q28942586',
    'Q29006203', 'Q29051834', 'Q29479187', 'Q29546406', 'Q29553694',
    'Q29553892', 'Q29584772', 'Q29585394', 'Q29586380', 'Q29586452',
    'Q29586504', 'Q29587254', 'Q29591412', 'Q29610130', 'Q29633511',
    'Q29645378', 'Q29645406', 'Q29645425', 'Q29688492', 'Q29842037',
    'Q29842052', 'Q29885770', 'Q29885778', 'Q29885819', 'Q30017383',
    'Q30061294', 'Q30061299', 'Q30061312', 'Q30061417', 'Q30061600',
    'Q30070324', 'Q30075473', 'Q30092197', 'Q30106090', 'Q30131044',
    'Q30131069', 'Q30147469', 'Q30158685', 'Q30167070', 'Q30167264',
    'Q30167705', 'Q30167902', 'Q30167980', 'Q30168244', 'Q30168533',
    'Q30169184', 'Q30170627', 'Q30172593', 'Q30174902', 'Q30174967',
    'Q30301473', 'Q30301487', 'Q30301495', 'Q30301514', 'Q30302572',
    'Q30302594', 'Q30307315', 'Q30307328', 'Q30307611', 'Q30307677',
    'Q30308127', 'Q30309605', 'Q30318016', 'Q30318085', 'Q30318131',
    'Q30319077', 'Q30322563', 'Q31854313', 'Q32012717', 'Q32066628',
    'Q32114761', 'Q32585054', 'Q32851726', 'Q32859515', 'Q32859534',
    'Q32859549', 'Q32999896', 'Q33093124', 'Q33125444', 'Q33293152',
    'Q33294038', 'Q33381018', 'Q33498716', 'Q33499497', 'Q33515508',
    'Q34315358', 'Q34500764'
])

fictional_properties = ('P1074')

# TODO remove this if filtering code works
do_not_show = frozenset([
    'Q166231',  # infection
    'Q21396183',  # arsenic pentoxide exposure
    'Q16943283',  # Rape of Europa
    'Q21175052',  # phosphine exposure
    'Q21504975',  # lewisite exposure
    'Q12147416',  # drug resistance
    'Q21167939',  # benzene exposure
    'Q408089',  # mercury poisoning
    'Q1784308',  # Judgement of Paris
    'Q12090',  # cholera
    'Q21174755',  # hydrogen fluoride exposure
    'Q21175308',  # sodium cyanide exposure
    'Q21513721',  # mechlorethamine exposure
    'Q21973551',  # chemical
    'Q21167853',  # chemical
    'Q21175069',  # chem
    'Q21514015',  # chem
    'Q21174754',  # chem
    'Q21173555',  # chem
    'Q21174113',  # chem
    'Q21402492',  # chem
    'Q21174897',  # chem
    'Q21175054',  # chem
    'Q21506740',  # chem
    'Q47912',  # lung cancer
    'Q11663',  # weather; yes, just weather, in general
    'Q3196',  # fire
    'Q173022',  # bronchitis
    'Q5421292',  # exploding animal
    'Q1366544',  # beached whale
])

# these came into existence at a certain time that can be pointed to
# (generally ~2000 years ago), but they don't have date info in Wikidata now
unsure = [
    'Q9309699',  # Madonna and child, artistic theme
    'Q370665',  # Sacred conversation, artistic theme
    'Q34726',  # Ancient Greek mythology
    'Q154326',  # Annunciation, holiday and artistic theme
    'Q9184',  # Book of Genesis
    'Q5989722',  # Penitent Magdalene, yet another Christian artistic theme
    'Q488841',  # Adoration of the Magi
    'Q16930210',  # Susanna and the Elders
    'Q2509393',  # Saint George and the Dragon
    'Q633534',  # Death of Cleopatra - artistic theme based on actual event
    'Q19786',  # Old Testament
    'Q18813',  # New Testament
    'Q1029715',  # Adoration of the shepherds, Christian artistic theme
    'Q15914389',  # ancient Chinese monarch, precise date of birth not known
    'Q51628',  # Nativity of Jesus
    'Q7885664',  # Dance of the Seven Veils
    'Q42040',  # Book of Revelation
    'Q1004401',  # Bridal theology, yet another Christian artistic theme
    'Q837143',  # Flight into Egypt, "biblical episode"
    'Q202129',  # Book of Judith
    'Q910606',  # music of Brittany; exclude as too general?
]

todo = [
    'Q20984804',  # Lars Kai Hansen, needs date of birth
    'Q735117',  # a reminder to use earliest/latest in the case of unknown date
    'Q462',  # Star Wars - need some sort of date, but item has none
    'Q1092',  # Start Trek - same thing
    'Q1233460'  # labors of Hercules: exclude all ancient Greek mythology?
]
