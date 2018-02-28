from lxml import etree
import re

if __name__ == "__main__":
    parser = etree.XMLParser(remove_comments=False)
    docn = etree.parse('data.xml', parser=parser)
    root = docn.getroot()
    if 'data' == root.tag:
        for table in root:
            print('# '+table.attrib['name'])
            tab_name = table.attrib['name']
            if tab_name == 'production list':
                hdr = False
                hdrs = []
                for row in table:
                    ix = 0
                    tabs = '  '
                    materials_comma =''
                    for col in row:
                        if not hdr:
                            hdrs.append(col.text.lower())
                        else:
                            if hdrs[ix] == 'item':
                                print('- !ProductionItem')
                                print('{tb}name: {d}'.format(tb=tabs, d=col.text))
                            elif hdrs[ix] == 'time':
                                time = 0
                                m=re.findall(r'(?P<unit>\d+)(?P<type>[dh])', col.text)
                                if m is not None:
                                    for g in m:
                                        if g[1] == 'd':
                                            time += int(g[0])*24
                                        if g[1] == 'h':
                                            time += int(g[0])

                                print('{tb}{h}: {t} #{d}'.format(tb=tabs, h=hdrs[ix], d=col.text, t=time))
                                print('{tb}materials: {ob}'.format(tb=tabs, ob='{'))
                                tabs = '    '
                                materials_comma=','
                            elif col.text is not None:
                                print('{tb}{t}: {d}{c}'.format(tb=tabs, t=hdrs[ix], d=col.text, c=materials_comma))
                        ix += 1
                    if hdr:
                        print('    blank: 0 }')
                    hdr = True
            elif tab_name == 'spacecraft':
                hdr = False
                hdrs = []
                for row in table:
                    ix = 0
                    tabs = '  '
                    for col in row:
                        if not hdr:
                            hdrs.append(col.text.lower())
                        else:
                            if hdrs[ix] == 'craft':
                                print('- !Spacecraft\n{tb}name: {t}'.format(tb=tabs, t=col.text))
                            else:
                                print('{tb}{t}: {d}'.format(tb=tabs, t=hdrs[ix], d=col.text))
                        ix += 1
                    hdr = True
            elif tab_name == 'planetary systems data':
                hdr = False
                hdrs = ['system','avg_trip_time','solargen_1','solargen_2','solargen_3','solargen_4','solargen_5','solargen_6','solargen_7','solargen_8','solargen_9','solargen_10']
                for row in table:
                    ix = 0
                    tabs = '  '
                    for col in row:
                        if hdr:
                            if hdrs[ix] == 'system':
                                print('- !System\n{tb}name: {t}'.format(tb=tabs, t=col.text))
                            elif hdrs[ix] == 'avg_trip_time':
                                print('{tb}{t}: {d}'.format(tb=tabs, t=hdrs[ix], d=col.text))
                                print('{tb}generators: {ob}'.format(tb=tabs, ob='{'))
                            else:
                                print('  {tb}{t}: {d},'.format(tb=tabs, t=hdrs[ix], d=col.text))
                        ix += 1
                    if hdr:
                        print('    blank: 0 }')
                    hdr = True
            elif tab_name == 'planet and moon data':
                hdr = False
                hdrs = []
                for row in table:
                    ix = 0
                    tabs = '  '
                    for col in row:
                        if not hdr:
                            hdrs.append(col.text.lower())
                        else:
                            if hdrs[ix] == 'body':
                                print('- !CelestialBody\n{tb}name: {t}'.format(tb=tabs, t=col.text))
                            elif hdrs[ix] == 'lifeform':
                                print('{tb}{t}: {d}'.format(tb=tabs, t=hdrs[ix], d=col.text))
                                print('{tb}materials: {ob}'.format(tb=tabs, ob='{'))
                            else:
                                if col.text is not None:
                                    print('  {tb}{t}: {d},'.format(tb=tabs, t=hdrs[ix], d=col.text))
                        ix += 1
                    if hdr:
                        print('    blank: 0 }')
                    hdr = True
