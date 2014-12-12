# Original version written by Henning Thielemann http://www.henning-thielemann.de

import re
import requests
from bs4 import BeautifulSoup

dict_saxlet = {
    'computer': 'gombjudor',
    'windows': 'windoof',
    'microsoft': 'mükroschrodd',
    'gates': 'gejts',
    'pentium': 'penndsium',
    'system': 'süsdem',
    'feature': 'mergmal',
    'features': 'mergmale',
    'software': 'sofdwehr',
    'hardware': 'hardwehr',
    'instruction': 'insdrakdschn',
    'extension': 'ixtenschn',
    'expansion': 'ixpanschn',
    'download': 'daunlohd',
    'download_': 'runnerladen_',
    'downloaden_': 'runnerladen_',
    'homepage': 'hohmbejdsch',
    'byte': 'beit',
    'update': 'abdejt',
    'team_': 'diehm_',
    'crew_': 'kruh_',
    'chat_': 'schedd_',
    'cool': 'guhl',
    'cookies': 'gegse',
    'netiquette': 'neddigedde',
    'power': 'bauer',
    'backup': 'bäggab',
    'myspace': 'maischbäß',
    'space': 'schbäß',
    'provider': 'verneddsor',  # 'broweidor',
    # 'halsabschneidor',
    'free': 'frieh',
    'screenshot': 'bildschirmfoddo',
    'compiler': 'übersedsor',
    'compilieren': 'übersedsn',
    'quellcode': 'quälkod',
    'sourcecode': 'quälkod',
    'meeting': 'dreffn',  # 'dsusammengunfd',
    'developer': 'endwigglor',
    'release': 'rielies',
    '_user': '_benuddsor',
    '_link_': '_vorweis_',
    'hyperlink': 'nedsvorweis',
    '_fan_': '_fenn_',
    'office': 'büro',
    'chip': 'schipp',
    'feedback': 'fiedbegg',
    'recyceln': 'widderverwerdn',
    'recyclen': 'widderverwerdn',
    'recycling': 'widderverwerdung',
    'style': 'sdil',
    'luther': 'ludder',
    'saison': 'sesong',
    # 'garage': 'garahsche',
    'garage': 'karahsche',
    'manege': 'manehsche',
    'passagier': 'bassaschier',
    'vietnamese': 'fidschi',
    'vietnamesen': 'fidschis',
    'google': 'guhgel',
    'pool': 'buhl',
    'service': 'sörwis',
    'haskell': 'hässgl',
    'news': 'njuhs',
    '_new_': '_njuh_',
    '_york_': '_jorg_',
    'layout': 'lejaud',
    # 'mund_': 'gusche_',
    'mund_': 'nischl_',
    'schnitte_': 'bemme_',
    'arbeit_': 'orbeit_',
    '_arbeiten_': '_klechen_',
    '_arbeite_': '_kleche_',
    '_arbeitet_': '_klecht_',
    '_arbeitest_': '_klechst_',
    '_mutter_': '_olle_',
    '_vater_': '_vadda_',
    'digital': 'diggedal',
    'medien': 'medchen',
    'fernseher_': 'glotze_',
    '_taxi_': '_taxe_',
    'fünfzig': 'fuffzich',
    'spam': 'sbämm',
    'slogan': 'slogän',
    'honecker': 'honi',
    'trabant': 'trabbi',
    'germany': 'dschörmeni',
    'community': 'gemeenschofd',
    'chemnitz': 'gorl-Morgs-Stodd',
    # Karl-Marx-Denkmal -> Nischl
    # ein - 'n
    # eine - 'ne
    # nicht wahr - nuwor
    # kannst du - kannste
    '_nun_': '_nu_',
    '_aber_': '_awor_',
    '_nein_': '_nee_',
    '_auch_': '_och_',
    '_gleich_': '_glei_',
    'ex': 'eggs',  # Experte
    'ax': 'aggs',  # Praxis
    'ox': 'oggs',  # paradox
    'echse': 'eggse',  # wechseln
    'achse': 'aggse',  # wachsen
    'sp': 'schb',
    'st': 'schd',
    # St am Anfang fast immer Scht, Ausnahme: Stil, St., Story
    # 'sp': 'sb',
    'st_': 'sd_',   # Analyst, Gerüst, Ast, fast
    'ste_': 'sde_',
    'stel_': 'sdl_',
    'stem_': 'sdm_',
    'sten_': 'sdn_',
    'ster_': 'sder_',
    'stes_': 'sdes_',
    'stet_': 'sded_',
    'spe_': 'sbe_',
    'spen_': 'sbn_',
    'ck': 'gg',
    'k': 'g',
    'th': 'd',
    't': 'd',
    'ph': 'ph',
    'p': 'b',
    'ie': 'ie',  # prevent the 'e' from being treated as the only vowel in its environment, as in 'Beispiel'
    'y': 'ü',
    'ayer': 'aier',  # Bayern
    'eyer': 'eier',  # Meyer
    'ich': 'isch',
    'ech': 'esch',
    'äch': 'äsch',
    'üch': 'üsch',
    'lch': 'lsch',
    'agt': 'acht',  # gefragt
    'ägt': 'ächt',  # überträgt
    'egt': 'echt',  # überlegt
    'agen': 'ahchn',  # tragen
    'ägen': 'ähchn',  # Mägen
    'egen': 'ehchn',  # legen
    '_chemn': '_gemn',
    '_che': '_sche',
    '_den_': '_den_',  # prevent from being shrinked to 'dn'
    '_die_': '_de_',
    'der_': 'dor_',
    'ter_': 'dor_',
    'ein': 'een',
    'nen_': 'n\'_',
    'en_': 'n_',
    'el_': 'l_',
    'nd_': 'nn_',
    'tion': 'dsion',
    'tionen': 'dsion\'',
    'ig_': 'ich_',
    'igen_': 'chen_',  # mäßigen
    'pzig': 'pzisch',  # Leipzig
    'mpf_': 'mff_',
    'pf_': 'bb_',

    'eipzig': 'eibzsch',
    'der': 'dor',
    'auch': 'och',
    'schläge': 'schlähche'
}


def get_sorted_translations():
    all_keys = dict_saxlet.keys()
    key_list = [key for key in all_keys]
    key_list.sort(key=len, reverse=True)
    return key_list


def translate(phrase, engine, method='local'):
    """Translate a phrase by applying a local dictionary."""
    words = phrase.split()
    translation = []
    for word in words:

        if engine == 'twitter':
            if re.match('@.*?', word):
                # don't translate twitter account mentions
                translation.append(word)
                continue
            if re.match('http://*.*', word):
                # don't translate URLs
                translation.append(word)
                continue

        if method == 'saxophone':
            s_word = send_saxophone_request(word)
        else:
            s_word = apply_substitutions(word)

        # restore capitalization
        if word.isupper():
            s_word = s_word.upper()
        elif word[0].isupper():
            s_word = s_word[:1].upper() + s_word[1:]

        translation.append(s_word)

    return ' '.join(translation)


def apply_substitutions(word):
    """Apply the local dictionary to a given word."""
    word = word.lower()
    for translation in get_sorted_translations():
        # if translation.startswith('_') and translation.endswith('_'):
        #     regex = re.compile(r'(\W|^)%s(\W|$)' % translation[1:-1])
        #     word = regex.sub(translation[1:-1], dict_saxlet[translation][1:-1])
        # elif translation.startswith('_'):
        #     regex = re.compile(r'(\W|^)%s' % translation[1:])
        #     word = regex.sub(translation[1:], dict_saxlet[translation][1:])
        # elif translation.endswith('_'):
        #     regex = re.compile(r'%s(\W|$)' % translation[:-1])
        #     word = regex.sub(translation[:-1], dict_saxlet[translation][:-1])
        if translation in word:
            word = word.replace(translation, dict_saxlet[translation])
            # break
    return word


def send_saxophone_request(word):
    """Send a single word to the original Saxophone for translation."""
    r = requests.get(url='http://parallelnetz.de/Saxophone',
                     params={
                         'phrase': word.lower().encode('cp1252')
                     })
    if r.status_code == 200:
        soup = BeautifulSoup(r.content.decode('cp1252'))
        return soup.find_all('td')[-1].string
