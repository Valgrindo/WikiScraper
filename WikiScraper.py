"""
This utility fetches a desired number of random Wikipedia articles in a given language and scrapes them for sequences
of words.
@author Sergey Goldobin
4/9/19
"""


from sys import argv
import requests
import StringUtils as su

# Denotes which version of Wikipedia to source articles from
MAX_TAG = 11  # An HTML tag cannot be longer than 11 characters
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


def get_article_wikitext(count):
    """
    Fetch the wikitext of X random wikipedia articles.
    :param count: (int) -- How many articles to get the wikitext from.
    :return: (list[str]) -- A list of raw wikitext from random articles.
    """
    session = requests.Session()
    url = API_KEYS[PARAMS['locale']]

    settings = \
        {
            'action': 'query',
            'prop': 'revisions',
            'rvprop': 'content',
            'format': 'json',
            'generator': 'random',
            'grnnamespace': 0,
            'grnlimit': count
        }

    reply = session.get(url=url, params=settings)
    parsed = reply.json()
    result = [page['revisions'][0]['*'] for page in parsed['query']['pages'].values()]

    return result


def clean_wikitext(source):
    """
    Remove all non-natural language constructs from wiki text, sacrificing some if necessary.
        Things removed:
          =headers= of any level
          '''preformatted'''
          [[links]]
          {{tables}}
          <tag> Embedded HTML </tag>
          '*' and '#' list markers
    :param source: (list[str])
    :return:
    """

    result = ''
    i = 0

    while i < len(source):
        if source[i] in {'=', '\'', '*', '#'}:
            i += 1  # Simply skip these characters. Text can be preserved
        elif su.is_substring_at(source, i, '{{'):
            i = su.string_skip(source, (i + 2), '}}', '{{')
        elif su.is_substring_at(source, i, '[['):
            i = su.string_skip(source, (i + 2), ']]', '[[')
        elif su.is_substring_at(source, i, '{|'):
            i = su.string_skip(source, (i + 2), '|}', '{|')
        elif su.is_substring_at(source, i, '['):
            i = su.string_skip(source, (i + 1), ']', '[')
        elif su.is_substring_at(source, i, '<'):
            i = su.string_skip(source, (i + 1), '>', '<')
        # elif source[i] == '<':  # TODO Debug this
        #     j = source[i:i+MAX_TAG].find('>')
        #     if j > -1:
        #         tag = source[i:i+j+1]
        #         start = i
        #         if tag[len(tag)-2:len(tag)] == '/>':  # If the HTML tag was self-closing, skip just the tag.
        #             i = su.string_skip(source, i, tag)
        #         else:
        #             i = su.string_skip(source, i + len(tag), f'</{tag[1:]}', tag)
        #
        #         print(f'Skipped: {source[start:i]}')
        #     else:
        #         i += 1
        else:
            result += source[i]  # There was nothing wrong with the character. Save it to the result.
            i += 1

    return result



def main():
    if len(argv) < 4 or len(argv) > 5:
        print('Usage: python ./WikiScraper {EN|NL} article_count sample_length [out_file]')
        exit(1)

    validate_params()  # Validate command line args.
    content = get_article_wikitext(PARAMS['articles'])

    # Wikitext has been acquired. Now, clean it to eliminate non-text constructs (tables) and some markup.
    clean = []
    for raw in content:
        clean.append(clean_wikitext(raw))

    # Text has been cleaned of most wiki symbols and mostly resembles natural language.
    # Parse it into words, eliminating any loose punctuation.



if __name__ == '__main__':
    main()
