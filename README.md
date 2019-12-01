Related Rhymes
==============

Finds words that are related and rhyme when provided with two documents of 1) related words and 2) rhyming words.  This is done by creating in-memory graphs and comparing the words between them.

Getting Started
===============

Clone this repository and change directory to the repository folder

Download or create a file named @related-words.txt@ of related terms.  The content of the file should have all related words on the same line seperated by a common delimiter.

Downlaod or create a file named @rhyme-words.txt@ of rhyming groups where teh content of the file should have all words that rhyme on the same line.  Use the following tool to create such a file: https://github.com/IyadKandalaft/rhyming-groups .

Run the code

    python get_rhymes.py --out output.txt --related-words related-words.txt --rhyme-words rhyme-words.txt

Review the output

    less -S output.txt

Getting Help
============

The help is built in to the software. Use @--help@ for more information

    python get_rhymes.py --help