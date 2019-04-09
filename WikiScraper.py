"""
This utility fetches a desired number of random Wikipedia articles in a given language and scrapes them for sequences
of words.
@author Sergey Goldobin
4/9/19
"""


from sys import argv
import requests

# Denotes which version of Wikipedia to source articles from
SUPPORTED_LOCALES = {'EN', 'NL'}
API_KEYS = \
    {
        'EN': 'https://en.wikipedia.org/w/api.php',
        'NL': 'https://nl.wikipedia.org/w/api.php'
    }

PARAMS = \
    {
        'locale': 'EN',         # Default to English
        'articles': 100,        # Default to 100 articles
        'sample_length': 15,    # Default to 15 words
        'out_file': 'data.txt'  # Default output file name.
    }


def validate_params():
    """
    Validate provided command line arguments.
    :return: A dictionary of command line values.
    """

    if argv[1] not in SUPPORTED_LOCALES:
        print(f'Unsupported locale: {argv[1]}')
        exit(1)
    else:
        PARAMS['locale'] = argv[1]

    if not argv[2].isdigit():
        print(f'Unrecognized article count: {argv[2]}')
        exit(1)
    else:
        PARAMS['articles'] = int(argv[2])

    if not argv[3].isdigit():
        print(f'Unrecognized sample length: {argv[3]}')
        exit(1)
    else:
        PARAMS['sample_length'] = int(argv[3])

    if len(argv) == 5:
        PARAMS['out_file'] = argv[4]


def get_article_ids():
    """
    Query Wikipedia API for a set of X random article IDs.
    :return: (List[string]) -- Sequence of IDs of random articles.
    """
    session = requests.Session()
    url = API_KEYS[PARAMS['locale']]

    settings = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": PARAMS['articles']
    }

    reply = session.get(url=url, params=settings)
    parsed = reply.json()

    # According to https://www.mediawiki.org/wiki/API:Random, the reply is formatted as follows:
    # {
    # "batchcomplete": "",
    # "continue": {
    #     "rncontinue": "0.559881820010|0.559881954661|47659388|0",
    #     "continue": "-||"
    # },
    # "query": {
    #     "random": [
    #         {
    #             "id": 32381675,
    #             "ns": 0,
    #             "title": "Mallabhum Institute of Technology"
    #         },
    #         ...
    #    ]
    # }
    # Keep IDs as strings, since they could be too large for an int.
    ids = [str(x['id']) for x in parsed['query']['random']]

    return ids


def get_article_wikitext(ids):
    settings = \
        {
            'action': 'query',
            'prop': 'revisions',
            'rvprop': 'content',
            'format': 'json',
            'formatversion': 2,
            'pageids': '|'.join(ids)
        }

    pass


def main():
    if len(argv) < 4 or len(argv) > 5:
        print('Usage: python ./WikiScraper {EN|NL} article_count sample_length [out_file]')
        exit(1)

    validate_params()  # Validate command line args.
    ids = get_article_ids()




if __name__ == '__main__':
    main()
