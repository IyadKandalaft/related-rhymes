import argparse
import sys
import graph
from related_rhymes import RelatedRhymes
import re
from logging.config import dictConfig
import logging

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers = {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    root = {
        'handlers': ['h'],
        'level': logging.DEBUG,
        },
)
dictConfig(logging_config)
logger = logging.getLogger()


def setup_args():
    """Setups up the argparse arguements for this script
        
    Returns:
        parse_args -- An object containing the values of arguements
    """
    parser = argparse.ArgumentParser(description='Creates a list of related words that rhyme')
    parser.add_argument('--progress', '-p', action='store_true',
                        help='Output progress text')
    parser.add_argument('--out', type=str, default="output.tab",
                        help='The output file path')
    parser.add_argument('--count', action='store_true',
                        help='Include the word count for each related words that rhyme')
    parser.add_argument('--related-words', '-r', type=str, default='related-words.txt',
                        help='File containing a list of related words on each line')
    parser.add_argument('--related-delim', '-rd', type=str, default='[#:\|;]',
                        help="Regex of delimeters to use to split lines in the related words file")
    parser.add_argument('--rhyme-words', '-y', type=str, default='rhymegroups.tab', 
                        help='File containing a list of related words on each line')
    parser.add_argument('--rhyme-delim', '-yd', type=str, default='[\t]',
                        help="Regex of delimeters to use to split lines in the rhyming words file")

    return parser.parse_args()

def load_words(file, delimeters, line_callback=None, reset_after_line=False):
    """Creates a graph of related or rhyming words from a file where the words are
    on one line and separated by delimeters

    line_callback is called and passed in graph

    Arguments:
        file {str} -- The file to load into 
        delimeters {str} -- Regular expression used to split lines into words
        line_callback {Callable} -- Class or function called after each line is processed
        reset_after_line {bool} -- Clears the graph after each line is processed
    
    Returns:
        Graph -- A graph object that permits traversal between the loaded words
    """
    words_graph = graph.Graph()

    with open(file, 'r') as fh:
        line_num = 0
        
        for line in fh:
            words = re.split(delimeters, line)
            # Remove empty values in the list
            #words = list(filter(None, words))
            #words = list(filter(lambda x:"\n" not in x, words))
            def hasNumbers(input):
                return bool(re.search(r'\d', input))

            words = [x for x in words if x != "" and x != "\n" and not hasNumbers(x)]

            # Provide progress information
            line_num += 1
            if line_num % 1000 == 0:
                logger.debug("Processing file %s line %d", file, line_num)

            skip_words = 1
            for word1 in words:
                words_graph.add_node(word1)

                # To avoid doubling the work, don't recreate graph edges for 
                # words that already have an edge between them
                skip_words += 1
                for word_num, word2 in enumerate(words, start=skip_words):
                    if word1 == word2:
                        continue

                    words_graph.add_node(word2)
                    words_graph.add_edge(word1, word2)

            if callable is not None and callable(line_callback):
                line_callback(words_graph)

            if reset_after_line:
                words_graph.clear()

    return words_graph

def write_lists_to_file(file, list_of_lists, count=False):
    separator = "\t"

    with open(file, 'w') as fh:
        
        for list in list_of_lists:
            if count:
                fh.write(str(len(list)) + separator)
            
            fh.write("\t".join(list) + "\n")
    
    fh.close()

def main():
    """Main method is executed if module is called directly
    
    Returns:
        int -- 0 for success, non-zero for failure
    """

    args = setup_args()

    if args.progress:
        logger.logLevel(logging.DEBUG)

    logger.info("Loading rhyming words from file %s", args.rhyme_words)
    rhyming_words = load_words(args.rhyme_words, args.rhyme_delim)

    rel_rhymes = RelatedRhymes(rhyming_words)

    logger.info("Loading related words from file %s", args.related_words)
    load_words(args.related_words, args.related_delim,
                                line_callback=rel_rhymes, reset_after_line=True)


    write_lists_to_file(file=args.out, list_of_lists=rel_rhymes.rhyming_related_lists, count=True)
    
    return 0

if __name__ == "__main__":
    main()