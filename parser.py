#!/usr/bin/env python3

import argparse
import nltk.data as nltk_data
from nltk.grammar import Nonterminal
from nltk import CFG, ChartParser
from nltk.parse.generate import generate
import random
import sys
import os

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
    parser_generate.add_argument('--depth', type=int, default=10)
    parser_generate.add_argument('--max', type=int, default=100)
    parser_generate.add_argument('--start', default=None)

    args = arg_parser.parse_args()

    if args.grammar_file == 'ATIS':
        grammar_path = None
        for data_path in nltk_data.path:
            path = os.path.join(data_path, 'grammars', 'large_grammars', 'atis.cfg')
            if os.path.exists(path):
                grammar_path = path
                break
        if grammar_path is None:
            raise FileNotFoundError("Could not find ATIS grammar in nltk data path!")
        grammar_handle = open(grammar_path, encoding='ISO-8859-1')
    else:
        grammar_handle = open(args.grammar_file)

    grammar = CFG.fromstring(grammar_handle.read())
    grammar_handle.close()
    parser = ChartParser(grammar)

    if args.command == 'check':
        try:
            trees = parser.parse(args.text.split(' '))
            try:
                tree = trees.__next__()
                print("The given sentence does conform to the grammar")
                if args.draw:
                    tree.draw()
                sys.exit(0)
            except StopIteration:
                print(f"The given sentence does not conform to the grammar:\n  'Could not find a valid dependency graph'")
                sys.exit(1)
        except ValueError as e:
            print(f"The given sentence does not conform to the grammar:\n  '{e}'")
            sys.exit(1)

    elif args.command == 'generate':
        sentences = []
        kw_args = {}
        if args.start is not None:
            kw_args['start'] = Nonterminal(args.start)
        for count, sentence in enumerate(generate(grammar, depth=args.depth, **kw_args)):
            sentences.append(sentence)
            if args.all:
                print(' '.join(sentence))
            if count == args.max - 1:
                break

        if not args.all:
            print(' '.join(sentences[random.randint(0, len(sentences) - 1)]))
