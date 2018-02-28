import yaml
from generator import Generator
from vessel import Vessel

if __name__ == "__main__":

    d = yaml.load(open('rmg.yaml', 'r'))
    print(d)
    for unit in d['production_item']:

        conf = d['production_item'][unit]
        if conf['type'] == 'generator':
            g=Generator(conf['name'])
            g.config(conf)
            print(g)
        elif conf['type'] == 'vessel':
            v=Vessel(conf['name'])
            v.config(conf)
            print(v)
