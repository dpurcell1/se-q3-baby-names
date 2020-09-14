#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

__author__ = """Darrell Purcell with help from
http://www.python-ds.com/python-3-list-methods
https://www.youtube.com
/watch?v=Uh2ebFW8OYM&list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU&index=26&t=0s
https://www.guru99.com/python-regular-expressions-complete-tutorial.html
https://www.codespeedy.com/convert-a-dictionary-into-a-list-in-python/
and Daniel's Argparse Demo
"""

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration. Here's what the HTML looks like in the
baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract all the text from the file and print it
 - Find and extract the year and print it
 - Extract the names and rank numbers and print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extracted_names list
"""

import sys
import re
import argparse


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a
    single list starting with the year string followed by
    the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', 'Aaron 57', 'Abagail 895', ...]
    """
    # create empty dict and set initialize year value
    names = []
    baby_dict = {}
    year = None
    # define year and name regex patterns to match in html files
    year_regex = re.compile(r'(Popularity in \d{4})')
    name_rank_regex = re.compile(
        r'<(tr\s\w+="\w+"><td>)(\d+)(</td><td>)(\w+)(</td><td>)(\w+)(</td>)')
    # create file reader to scan html file line by line
    with open(filename, 'r') as f:
        for line in f:
            # assign pattern matches for year and name/rank to variables
            # year_match returns list
            year_match = re.findall(year_regex, line)
            # rank_match returns string
            rank_match = re.match(name_rank_regex, line)
            # extract year from year_match list via slicing
            if year_match:
                year = year_match[0][-4:]
            # create string of rank/match pairs and append to names list
            if rank_match:
                names.append(rank_match.group(4) + ' ' + rank_match.group(2))
                names.append(rank_match.group(6) + ' ' + rank_match.group(2))
    # define rank regex pattern to match in names list
    rank_regex = re.compile(r'(\w+\s)(\d+)')
    # sort names list alphabetically
    names.sort()
    # find rank pattern in every list item
    for name in names:
        rank = re.match(rank_regex, name)
        # when found, assign name and rank to variables
        if rank:
            ranking = rank.group(2)
            name = rank.group(1)
            # create dictionary of name/rank pairs
            if name not in baby_dict.keys():
                baby_dict[name] = ranking
            # if name exists in dict, assign key a value of highest rank found
            elif int(ranking) < int(baby_dict[name]):
                baby_dict[name] = ranking
    # clear out names list
    names = []
    # create list of tuples from dictionary
    dict_list = baby_dict.items()
    # iterate through tuple list and append stringified name/rank pairs to list
    for key, value in dict_list:
        pair = key + str(value)
        names.append(pair)
    # insert year at beginning of names list
    names.insert(0, year)
    # return names list from function
    return names


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more
    # filenames. It will also expand wildcards just like the shell.
    # e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    # Create a command line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command line arguments into a
    # NAMESPACE called 'ns'
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    # option flag
    create_summary = ns.summaryfile

    # For each filename, call `extract_names()` with that single file.
    # Format the resulting list as a vertical list (separated by newline \n).
    # Use the create_summary flag to decide whether to print the list
    # or to write the list to a summary file (e.g. `baby1990.html.summary`).

    # iterate through file_list of filenames passed via cmd line arguments
    for file in file_list:
        # pass each filename to extract_names function
        baby_names = extract_names(file)
        # format list returned from extract_names
        text = '\n'.join(baby_names)
        # validation for create_summary boolean
        if create_summary:
            # create file with specified filename
            filename = file + '.summary'
            with open(filename, 'w') as f:
                f.write(text)
        # print to console if create_summary = false
        else:
            print(text)


if __name__ == '__main__':
    main(sys.argv[1:])
