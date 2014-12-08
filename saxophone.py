# Originally written by Henning Thielemann http://www.henning-thielemann.de

import re

re_saxlet = re.compile(
    r'\Aden\Z|\Adie\Z|' +
    r'computer|[aeo]x|luther|google|service|news|' +
    r'nen\Z|en\Z|el\Z|nd\Z|ig\Z|mpf\Z|pf\Z|' +
    r'ste\Z|ste[lmnrst]\Z|yst|spe\Z|spen\Z|s[pt](?!\Z)|tion|tionen|' +
    r'der|ter|ein|' +
    r'ck|k|th|t|ph|p|ie|y|[ieäül]ch|\Achemn|\Ache',
    re.LOCALE)

dict_saxlet = {
    'computer': 'gombjudor',
    'luther':   'ludder',
    'google':   'guhgel',
    'service':  'sörwis',
    'news':     'njuhs',
    'ex':       'eggs',  # Experte
    'ax':       'aggs',  # Praxis
    'ox':       'oggs',  # paradox
    'sp':       'schb',
    'st':       'schd',
    'yst':      'üsd',
    'ste':      'sde',
    'stel':     'sdl',
    'stem':     'sdm',
    'sten':     'sdn',
    'ster':     'sder',
    'stes':     'sdes',
    'stet':     'sded',
    'spe':      'sbe',
    'spen':     'sbn',
    'ck':       'gg',
    'k':        'g',
    'th':       'd',
    't':        'd',
    'ph':       'ph',
    'p':        'b',
    'ie':       'ie',  # prevent the 'e' from being treated as the only vowel in its environment, as in 'Beispiel'
    'y':        'ü',
    'ich':      'isch',
    'ech':      'esch',
    'äch':      'äsch',
    'üch':      'üsch',
    'lch':      'lsch',
    'chemn':    'gemn',
    'che':      'sche',
    'den':      'den',  # prevent from being shrinked to 'dn'
    'die':      'de',
    'der':      'dor',
    'ter':      'dor',
    'ein':      'een',
    'nen':      'n',
    'en':       'n',
    'el':       'l',
    'nd':       'n',
    'tion':     'dsion',
    'tionen':   'dsion',
    'mpf':      'mff',
    'pf':       'bb',
    'ig':       'ich'
}


def sub_sax(mt):
    return dict_saxlet[mt.group()]


def make_sax(word):
    return re_saxlet.sub(sub_sax, word)
