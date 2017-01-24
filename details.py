directions = {'north': 0, 'east': 1, 'south': 2, 'west': 3, 'up': 4, 'down': 5}
inverted_directions = {'north': 2, 'east': 3, 'south': 0, 'west': 1, 'up': 5, 'down': 4}

road_directions = set(('secret pass', 'secret route', 'old road',
                       'narrow channel', 'rocky channel', 'secret sea route',
                       'underground'))
special_directions = road_directions.union(set(('out',)))

route_annotations = set(('hidden', 'impassable', 'port', 'port city', 'safe haven'))

province_kinds = set(('mountain', 'plain', 'swamp', 'forest', 'desert', 'ocean',
                     'tunnel', 'chamber', 'cloud', 'underground'))
has_6_directions = set(('tunnel', 'sewer', 'chamber'))

subloc_kinds = set(('island', 'ring of stones', 'mallorn grove', 'bog', 'cave',
                    'city', 'graveyard', 'ruins', 'battlefield', 'enchanted forest',
                    'rocky hill', 'circle of trees', 'pits', 'pasture', 'oasis',
                    'yew grove', 'sand pit', 'sacred grove', 'poppy field', 'lair',
                    'faery hill', 'sewer'))

structure_type = set(('castle', 'tower', 'galley', 'roundship', 'temple', 'mine', 'collapsed mine', 'inn'))

structure_er = {
    'castle':  '10000',
    'tower':    '2000',
    'galley':    '250',
    'roundship': '500',
    'temple':   '1000',
    'mine':      '500',
    'inn':       '300',
    'raft':       '45'}

ship_capacity = {
    'roundship': '25000',
    'galley':     '5000'}

mine_production = [['79',  '0', '1',   '0', '82', '0'],
                   ['79', '15', '1',  '25', '82', '0'],
                   ['79', '12', '1', '100', '82', '0'],
                   ['79', '10', '1', '200', '82', '0'],
                   ['79',  '8', '1', '500', '82', '1'],
                   ['79',  '5', '1', '500', '82', '0'],
                   ['79',  '3', '1', '400', '82', '0'],
                   ['79',  '0', '1', '150', '82', '0'],
                   ['79',  '0', '1',  '50', '82', '1'],
                   ['79',  '0', '1',   '0', '82', '2'],
                   ['79',  '0', '1',   '0', '82', '8'],
                   ['79',  '0', '1',   '0', '82', '5'],
                   ['79',  '0', '1',   '0', '82', '0'],
                   ['79', '10', '1',  '10', '82', '0'],
                   ['79', '10', '1',  '50', '82', '2'],
                   ['79',  '0', '1',  '10', '82', '1'],
                   ['79',  '0', '1',   '0', '82', '0'],
                   ['79', '10', '1',   '0', '82', '1'],
                   ['79',  '0', '1', '500', '82', '0'],
                   ['79',  '0', '1',   '0', '82', '0'],
                   ['79',  '0', '1',   '0', '82', '0']]

geo_inventory = {
    # ordered same as mapgen.c
    'ocean': ['59', '30', '87', '50', '274', '1', '275', '1', '276', '1'],
    'forest': ['77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1'],
    'swamp': ['66', '1', '96', '50', '101', '1', '274', '1'],
    'mountain': ['78', '50', '10', '10', '96', '50', '101', '1', '275', '1'],
    'plain': ['51', '5', '10', '10', '96', '50', '101', '1', '275', '1'],
    'desert': ['78', '10', '96', '50', '101', '1', '275', '1'],

    'island': ['59', '30'],
    'ring of stones': [],
    'mallorn grove': ['65', '2', '70', '2'],
    'bog': ['66', '4'],
    'cave': ['67', '2'],
    'city': ['10', '10', '294', '1', '277', '5', '96', '100', '101', '1'],
    # 'guild' -- generic name for non-land non-ocean sublocs
    'graveyard': ['31', '15', '273', '1'],
    'ruins': [],
    'battlefield': [],
    'enchanted forest': [],
    'rocky hill': ['78', '50'],
    'circle of trees': ['77', '5', '64', '3'],
    'pits': ['66', '4'],
    'pasture': ['51', '5'],
    'oasis': [],
    'yew grove': ['68', '5'],
    'sand pit': ['71', '1'],
    'sacred grove': ['77', '5'],
    'poppy field': ['93', '25'],
    'lair': [],

    # these are province-sized things in non-normal places
    'cloud': ['274', '1', '275', '1', '276', '1'],
    'underground': ['101', '1', '96', '50'],
    'tunnel': ['101', '1', '96', '50'],
    'chamber': ['101', '1', '96', '50'],

    # and two final special things that link normal-faery and normal-undercity
    'faery hill': [],
    'sewer': [],
}

skill_days = {
    '600': '21',
    '601': '14',
    '602': '14',
    '603': '14',
    '610': '21',
    '611': '28',
    '612': '28',
    '613': '14',
    '614': '14',
    '615': '21',
    '616': '14',
    '617': '14',
    '630': '28',
    '631': '14',
    '632': '14',
    '633': '14',
    '634': '14',
    '635': '28',
    '636': '14',
    '637': '21',
    '638': '28',
    '639': '21',
    '650': '28',
    '651': '21',
    '652': '28',
    '653': '28',
    '654': '28',
    '655': '14',
    '656': '14',
    '657': '21',
    '658': '21',
    '659': '21',
    '661': '21',
    '670': '28',
    '671': '14',
    '672': '21',
    '673': '14',
    '674': '21',
    '675': '21',
    '676': '14',
    '680': '21',
    '681': '14',
    '682': '14',
    '690': '28',
    '691': '21',
    '692': '21',
    '693': '21',
    '694': '21',
    '695': '14',
    '696': '21',
    '697': '28',
    '700': '21',
    '701': '14',
    '702': '14',
    '703': '14',
    '704': '14',
    '705': '14',
    '706': '14',
    '707': '14',
    '720': '21',
    '721': '14',
    '722': '14',
    '723': '14',
    '730': '21',
    '731': '14',
    '732': '14',
    '733': '14',
    '750': '35',
    '751': '28',
    '752': '28',
    '753': '21',
    '754': '28',
    '755': '28',
    '756': '28',
    '800': '28',
    '801': '14',
    '802': '14',
    '803': '14',
    '804': '21',
    '805': '21',
    '806': '21',
    '807': '14',
    '808': '21',
    '809': '21',
    '811': '21',
    '812': '21',
    '813': '21',
    '814': '21',
    '820': '35',
    '821': '21',
    '822': '21',
    '823': '21',
    '824': '21',
    '825': '21',
    '826': '21',
    '827': '21',
    '828': '21',
    '829': '21',
    '831': '28',
    '832': '21',
    '833': '21',
    '840': '35',
    '841': '21',
    '842': '21',
    '843': '14',
    '844': '21',
    '845': '21',
    '846': '21',
    '847': '21',
    '848': '21',
    '849': '21',
    '851': '21',
    '852': '21',
    '860': '35',
    '861': '14',
    '862': '14',
    '863': '21',
    '864': '14',
    '865': '14',
    '866': '14',
    '867': '21',
    '868': '21',
    '869': '14',
    '871': '14',
    '872': '21',
    '880': '43',
    '881': '14',
    '882': '21',
    '883': '21',
    '884': '21',
    '885': '21',
    '886': '14',
    '887': '14',
    '888': '14',
    '889': '21',
    '891': '28',
    '892': '14',
    '893': '21',
    '894': '21',
    '900': '42',
    '901': '21',
    '902': '21',
    '903': '21',
    '904': '21',
    '905': '21',
    '906': '21',
    '907': '28',
    '908': '21',
    '909': '21',
    '911': '28',
    '920': '42',
    '921': '28',
    '922': '28',
}

skill_experience = {
    'apprentice': '0',
    'journeyman': '5',
    'adept': '12',
    'master': '21',
    'grand master': '35',
}

trade_map = {
    'buy': '1',
    'sell': '2',
    'produce': '3',
    'consume': '4'
}

noble_ranks = {'lord': '10',
               'knight': '20',
               'baron': '30',
               'count': '40',
               'earl': '60',
               'marquess': '60',
               'duke': '70',
               'king': '80'}

numbers = {'one': 1,
           'two': 2,
           'three': 3,
           'four': 4,
           'five': 5,
           'six': 6,
           'seven': 7,
           'eight': 8,
           'nine': 9,
           'ten': 10}

item_to_inventory = {
    'gold': '1',
    'peasant': '10',
    'worker': '11',
    'soldier': '12',
    'archer': '13',
    'knight': '14',
    'elite guard': '15',
    'pikeman': '16',
    'pikemen': '16',
    'blessed soldier': '17',
    'ghost warrior': '18',
    'sailor': '19',
    'swordsman': '20',
    'swordsmen': '20',
    'crossbowman': '21',
    'crossbowmen': '21',
    'elite archer': '22',
    'angry peasant': '23',
    'pirate': '24',
    'elf': '25',
    'elves': '25',
    'spirit': '26',
    'undead': '31',
    'savage': '32',
    'skeleton': '33',
    'barbarian': '34',
    'wild horse': '51',
    'riding horse': '52',
    'warmount': '53',
    'winged horse': '54',
    'nazgul': '55',
    'floatsam': '59',
    'battering ram': '60',
    'catapult': '61',
    'siege tower': '62',
    'ratspider venom': '63',
    'lana bark': '64',
    'avinia leaf': '65',
    'avinia leaves': '65',
    'spiny root': '66',
    'farrenstone': '67',
    'yew': '68',
    'elfstone': '69',
    'mallorn wood': '70',
    'pretus bones': '71',
    'longbow': '72',
    'plate armor': '73',
    'longsword': '74',
    'pike': '75',
    'ox': '76',
    'oxen': '76',
    'wood': '77',
    'stone': '78',
    'iron': '79',
    'leather': '80',
    'ratspider': '81',
    'mithril': '82',
    'gate crystal': '83',
    'blank scroll': '84',
    'crossbow': '85',
    'fish': '87',
    'opium': '93',
    'woven basket': '94',
    'clay pot': '95',
    'drum': '98',
    'hide': '99',
    'lead': '102',
    'pitch': '261',
    'centaur': '271',
    'minotaur': '272',
    'giant spider': '278',
    'rat': '279',
    'lion': '280',
    'giant bird': '281',
    'giant lizard': '282',
    'bandit': '283',
    'chimera': '284',
    'harpie': '285',
    'dragon': '286',
    'orc': '287',
    'gorgon': '288',
    'wolf': '289',
    'wolves': '289',
    'cyclops': '291',
    'giant': '292',
    'faerie': '293',
    'faeries': '293',
    'hound': '295'
}

mage_ranks = set(('conjurer', 'mage', 'wizard', 'sorcerer',
                  '6th black circle', '5th black circle', '4th black circle',
                  '3rd black circle', '2nd black circle', 'master of the black arts'))
