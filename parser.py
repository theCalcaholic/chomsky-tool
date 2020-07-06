#!/usr/bin/env python3

import argparse
from nltk import CFG, ChartParser
from nltk.parse.generate import generate
import random
import sys

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    subparsers = arg_parser.add_subparsers()
    parser_check = subparsers.add_parser('check')
    parser_generate = subparsers.add_parser('generate')

    parser_check.add_argument('grammar_file')
    parser_check.set_defaults(command='check')

    parser_generate.add_argument('grammar_file')
    parser_generate.set_defaults(command='generate')

    parser_check.add_argument('text')
    parser_check.add_argument('--draw', '-d', action='store_true', default=False)

    parser_generate.add_argument('--all', action='store_true', default=False)

    args = arg_parser.parse_args()

    with open(args.grammar_file) as f_handle:
        grammar = CFG.fromstring(f_handle.read())
        parser = ChartParser(grammar)

    if args.command == 'check':
        try:
            trees = parser.parse(args.text.split(' '))
            tree = trees.__next__()
            print("The given sentence does conform to the grammar")
            if args.draw:
                tree.draw()
            sys.exit(0)
        except ValueError as e:
            print(f"The given sentence does not conform to the grammar:\n  '{e}'")
            sys.exit(1)

    elif args.command == 'generate':
        sentences = []
        for count, sentence in enumerate(generate(grammar, depth=10)):
            sentences.append(sentence)
            if args.all:
                print(' '.join(sentence))
            if count == 99:
                break

        if not args.all:
            print(' '.join(sentences[random.randint(0, len(sentences) - 1)]))
