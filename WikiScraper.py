"""
This utility fetches a desired number of random Wikipedia articles in a given language and scrapes them for sequences
of words.
@author Sergey Goldobin
4/9/19
"""


from sys import argv


def main():
    if len(argv) != 4:
        print('Usage: python ./WikiScraper locale article_count sentence_length')
        exit(1)


if __name__ == '__main__':
    main()
