import yaml


class Weapon(yaml.YAMLObject):
    yaml_tag = u'!Weapon'

    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def __repr__(self):
        return '{c}(name=\'{n}\', hp={h})'.format(c=self.__class__.__name__, n=self.name, h=self.hp)


class Monster(yaml.YAMLObject):
    yaml_tag = u'!Monster'

    def __init__(self, name, hp, ac, attacks, weapon):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks
        self.weapon = weapon

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, hp={self.hp!r}, ac={self.ac!r}, attacks={self.attacks!r}, weapon={self.weapon!r}"


class Hero(Monster):
    yaml_tag = u'!Hero'

    def __init__(self, name, hp, ac, attacks, weapon):
        super(Hero, self).__init__(name, hp, ac, attacks, weapon)


for o in yaml.load(open('y2.yaml', 'r')):
    print(o)

w = Weapon(name="Sting", hp=100)
m1 = Monster(name='x', hp=[1,2], ac=10, attacks=['ME'], weapon=w)

print(yaml.dump([m1,m1]))