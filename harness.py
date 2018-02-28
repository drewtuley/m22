from rmg import Spacecraft, System, CelestialBody, ProductionItem, Refinery, Generator, Factory, LifeSupport
import yaml

if __name__ == "__main__":

    systems = {}
    production_items = {}
    spacecraft = {}
    bodies = {}
    generator_names = {}

    for o in yaml.load(open('rmg.yaml', 'r')):
        # print(o.name)
        if isinstance(o, ProductionItem):
            production_items[o.name] = o
        elif isinstance(o, Spacecraft):
            spacecraft[o.name] = o
        elif isinstance(o, System):
            systems[o.name] = o
        elif isinstance(o, CelestialBody):
            bodies[o.name] = o
        else:
            if 'generator_names' in o:
                generator_names = o['generator_names']

    print('Loaded {} Systems'.format(len(systems)))
    print('Loaded {} Production Items'.format(len(production_items)))
    print('Loaded {} Spacecraft'.format(len(spacecraft)))
    print('Loaded {} Celestial Bodies'.format(len(bodies)))
    moon_b = bodies['Moon']
    print(moon_b)

    moon_s = systems['Moon']
    print(moon_s)

    grazer = spacecraft['Grazer']
    print(grazer)

    pi = production_items[grazer.name]
    print(pi)

    print(generator_names)

    for g in generator_names:
        print('{n:15s}: {o}'.format(n=generator_names[g], o=moon_s.generator_power_map[g]))

    r = Refinery(moon_b)
    print(r)
    r.process(24)
    print(r)
    r.process(1)
    print(r)

    g = production_items['solargen_2']
    print(g)

    cb = g.can_build(100, r.stock)
    print(cb)
    g.researched = True
    cb = g.can_build(100, r.stock)
    print(cb)
    r.active = True
    r.process(72)
    cb = g.can_build(100, r.stock)
    print(cb)

    f = Factory(moon_b)
    print(f)

    g = Generator(moon_s, None)
    g1 = production_items['solargen_1']
    g1.researched = True
    print('R1 {}'.format(r))
    f.start_building(r, g, g1)
    print(f)
    while not f.is_complete():
        print('R2 {}'.format(r))
        f.process(24, g)
        print(f)
    print(g)
    g.set_generator(g1)
    print(g)

    g2 = production_items['solargen_2']
    g2.researched = True
    print('R1 {}'.format(r))
    f.start_building(r, g, g2)
    print(f)
    while not f.is_complete():
        print('R2 {}'.format(r))
        f.process(24, g)
        print(f)
    print(g)
    g.set_generator(g2)
    print(g)

    l = LifeSupport(moon_b)
    print(l)
    for x in range(46):
        l.process(24)
        print(l)
    for x in range(70):
        l.process(24)
    print(l)