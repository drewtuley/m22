from yaml import YAMLObject


class System(YAMLObject):
    yaml_tag = u'!System'

    def __init__(self, name, avg_trip_time, generator_power_map, researched):
        self.name = name
        self.avg_trip_time = avg_trip_time
        self.generator_power_map = generator_power_map
        self.researched = researched

    def __repr__(self):
        return 'System: {n}\nAvg Trip Time: {a}\nResearched: {r}\nGenerators: {g}'.format(n=self.name,
                                                                                          a=self.avg_trip_time,
                                                                                          g=self.generator_power_map,
                                                                                          r=self.researched)

    def available_power(self, generator):
        return self.generator_power_map[generator.name]


class CelestialBody(YAMLObject):
    yaml_tag = u'!CelestialBody'

    def __init__(self, name, lifeform, materials, researched, system):
        self.name = name
        self.lifeform = lifeform
        self.materials = materials
        self.system = system
        self.researched = researched

    def __repr__(self):
        return 'Celestial Body: {n}\nLifeform: {l}\nSystem: {s}\nReserched: {r}\nMaterials: {m}'.format(n=self.name,
                                                                                                        l=self.lifeform,
                                                                                                        m=self.materials,
                                                                                                        s=self.system,
                                                                                                        r=self.researched)


class Spacecraft(YAMLObject):
    yaml_tag = u'!Spacecraft'

    def __init__(self, name, crew, capacity, researched):
        self.name = name
        self.crew = crew
        self.capacity = capacity
        self.researched = researched

    def __repr__(self):
        return 'Spacecraft: {n}\nCrew: {c}\nCapacity: {ca}\nResearched: {r}'.format(n=self.name, c=self.crew,
                                                                                    ca=self.capacity, r=self.researched)


class ProductionItem(YAMLObject):
    yaml_tag = u'!ProductionItem'

    def __init__(self, name, mass, power, time, materials, researched):
        self.name = name
        self.mass = mass
        self.power = power
        self.time = time
        self.materials = materials
        self.researched = researched

    def __repr__(self):
        return 'Production Item: {n}\nMass: {ma}\nPower: {p}\nTime: {t}\nResearched: {r}\nMaterials: {m}'.format(
            n=self.name,
            m=self.materials,
            ma=self.mass,
            p=self.power,
            t=self.time,
            r=self.researched)

    def can_build(self, available_power, available_materials):
        if self.researched:
            if available_power < self.power:
                return False
            for material in self.materials:
                if available_materials[material] < self.materials[material]:
                    return False
            return True
        else:
            return False


class Generator:
    def __init__(self, system, generator):
        self.system = system
        self.generator = generator

    def available_power(self):
        if self.generator is None:
            return 30  # battery power
        else:
            return self.system.available_power(self.generator)

    def set_generator(self, generator):
        self.generator = generator

    def __repr__(self):
        if self.generator is None:
            return 'Battery:\nPower: 30'
        else:
            return 'Generator: {n}\nPower: {p}'.format(n=self.generator.name, p=self.available_power())


class Refinery:
    def __init__(self, location):
        self.location = location
        self.active = False
        self.stock = {}
        for material in location.materials:
            self.stock[material] = 0

    def __repr__(self):
        return 'Location: {l}\nStock: {s}'.format(l=self.location.name, s=self.stock)

    def process(self, timeperiod):
        if self.active:
            for material in self.location.materials:
                volume = int(self.location.materials[material]) * (timeperiod / 24)
                self.stock[material] += volume / 1000

    def allocate_stock(self, production_item):
        for material in production_item.materials:
            self.stock[material] -= production_item.materials[material]


class Factory:
    def __init__(self, location):
        self.location = location
        self.current_production_item = None
        self.active = False
        self.progress = 0.0

    def __repr__(self):
        return 'Factory: {l}\nBuilding: {i}\nProgress: {p:3.2%}'.format(l=self.location.name,
                                                                        i=self.current_production_item,
                                                                        p=self.progress)

    def start_building(self, refinery, generator, production_item):
        if production_item.can_build(generator.available_power(), refinery.stock):
            refinery.allocate_stock(production_item)
            self.active = True
            self.current_production_item = production_item
            self.progress = 0.0

    def is_complete(self):
        return self.progress == 1.0

    def can_process(self, population):
        return population >= 50

    def process(self, timeperiod, generator):
        if self.active is not None and self.current_production_item is not None:
            if generator.available_power() < self.current_production_item.power:
                self.active = False
            else:
                self.progress += timeperiod / self.current_production_item.time
                if self.progress >= 1.0:
                    self.progress = 1.0
                    self.active = False


class LifeSupport:
    def __init__(self, location):
        self.location = location
        self.population = 16.0
        self.nodules = 1

    def __repr__(self):
        return 'LifeSupport: {l}\nPopulation: {p}'.format(l=self.location.lifeform, p=self.population)

    def max_population(self):
        if self.nodules is None:
            return 100
        else:
            return self.nodules * 100

    def process(self, timeperiod):
        """Calculation for population increase rate taken from:
        ..population starts at 16, it will take about 46 days for it to increase to 50
        """
        self.population += (34 / 46) * (timeperiod / 24)
        if self.population > self.max_population():
            self.population = self.max_population()


class Colony:
    def __init__(self, system, location):
        self.system = system
        self.location = location
        self.generator = Generator(self.system, None)
        self.life_support = LifeSupport(self.location)
        self.refinery = Refinery(self.location)

        if system.name == 'Moon':
            # Only Moon has Factory and Research Unit
            self.factory = Factory(self.location)
            self.life_support.population = 100
        else:
            self.factory = None
            self.research_unit = None

    def process(self, timeperiod):
        self.refinery.process(timeperiod)
        if self.factory is not None and self.factory.can_process(self.life_support.population):
            self.factory.process(timeperiod, self.generator)
        self.life_support.process(timeperiod)
