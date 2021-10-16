"""Contains the bots data dictionary."""
from typing import Union

from absl import logging

bots = {
    'ElizaHahns': {
        'username': 'ElizaHahns',
        'password': 'AKJHD97434%^%',
        'phone_number': '+61404245906',
        'followed_accounts': [
            '@Jim_Jordan',
            '@michellemalkin',
            '@michaeljohns',
            '@Heritage',
            '@RedState',
            '@townhallcom',
            '@NRO',
            '@theMRC',
            '@DailyCaller',
            '@TuckerCarlson',
            '@JudgeJeanine',
            '@seanhannity',
            '@IngrahamAngle',
            '@FoxNews',
            '@JesseBWatters',
            '@GregGutfeld'
        ],
        'relevant_tags': [
            '#conservative',
            '#trump',
            '#maga',
            '#republican',
            '#donaldtrump',
            '#kag',
            '#makeamericagreatagain',
            '#trumptrain',
            '#keepamericagreat',
            '#americafirst',
            '#draintheswamp',
            '#rightwing',
            '#republicans',
            '#gop',
            '#fakenews',
            '#alllivesmatter',
            '#libtards',
            '#liberalsnowflakes'
            'freedom',
            'guns',
            'trump',
            'maga',
            'god'
        ]
    },
    'Allison45555547': {
        'username': 'Allison45555547',
        'password': 'A2IHNDjPu23SNEjfy4ts',
        'phone_number': '+61404328304',
        'followed_accounts': [
            '@democracynow',
            '@IlhanMN',
            '@AOC',
            '@thenation',
            '@joshtpm',
            '@DavidCornDC',
            '@maddow',
            '@SenWarren',
            '@JamesFallows',
            '@KevinMKruse',
            '@SenSanders',
            '@slpng_giants',
            '@RBReich',
            '@mmfa',
            '@thinkprogress',
        ],
        'relevant_tags': [
            '#liberal',
            '#blm',
            '#vote',
            '#berniesanders',
            '#voteblue',
            '#blacklivesmatter',
            '#berniesanders',
            '#progressives',
            '#democrats',
            '#bernie',
            '#socialism',
            '#resist',
            '#votebluenomatterwho',
            '#leftists',
            '#democrat',
            '#republicanssuck',
            '#getoutthevote',
            'liberal',
            'social justice',
            '#BernieSanders',
            'alexandria ocasio cortez'
        ]
    },
    'Melinda06678369': {
        'username': 'Melinda06678369',
        'password': 'MM8Q\=oks.p;nDFOeFe0',
        'phone_number': '+61404328304',
        'followed_accounts': [
            '@Greens',
            '@AustralianLabor',
            '@sarahinthesen8',
            '@AdamBandt',
            '@SenatorWong',
            '@AlboMP',
            '@tanya_pilbersek',
            '@BernardKeane',
            '@GuardianAus'
        ],
        'relevant_tags': []
    },
    'AgnesSursula': {
        'username': 'AgnesSursula',
        'password': 'OQCtrUUpGCzfa1HyOhhZ',
        'phone_number': '+61404328304',
        'followed_accounts': [
            '@SkyNews',
            '@theboltreport',
            '@rowandean',
            '@RealMarkLatham',
            '@PaulineHansonOz',
            '@mattjcan',
            '@OneNationAus',
            '@Barnaby_Joyce',
            '@HonTonyAbbott',
            '@LiberalAus',
            '@HonJulieBishop',
            '@The_Nationals',
            '@MRobertsQLD'
        ],
        'relevant_tags': [
        ]
    }
}


def get_bot(bot_username: str, info: str) -> Union[list, str]:
    """Function to get bot info from bot_info.py."""
    try:
        bot = bots[bot_username][info]
        return bot
    except:
        logging.error("Bot does not exist in bot_info.py")
        return
