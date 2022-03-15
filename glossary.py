import os
import re
import random
import argparse

Extensions = [".sql", ".txt", ".c", ".cpp", ".java", ".py", ".xml"]

def extract_words(content_str):
    """
        Extracting unique whole words from a string.
        for example:
            >>> content_str =   import numpy as np
                                import random

                                def func1(arg, arg1, arg_name):
                                    variable = 13+16/87
                                    print("hello world {}".format(arg2_name))
                                    return arg + arg1 # words in comments included
            >>> words = extract_words(content_str)
            # words = {'arg', 'name', 'as', 'comments', 'def', 'format', 'func', 'hello', 'import', 'in', 'included', 'np', 'numpy', 'print', 'random', 'return', 'variable', 'words', 'world'}
        
        Note:
            a. Only letters stay.
            b. All words included (words in comments etc are important too).
            c. The order of words in the input(s) will not leak whatsoever. Because in Glossary object we are shuffling the words (And Set object ignores the original order either way). 
            d. The frequencies of words will not leak, because we don't save it at all.
            
    """    
    content_str = re.sub("\W", " ", content_str) # keeping only alphanumeric (and underscores)
    content_str = re.sub("\d", " ", content_str) # now keeping only alphabetical
    content_str = re.sub("_{1,}", " ", content_str) # removing underscore. Note: better to use {2,} if possible
    content_str = re.sub("\s+", " ", content_str)
    unique_words = set(content_str.strip().split(" "))
    return unique_words

class Glossary():
    def __init__(self, glossary_path, load):
        self.glossary_path = glossary_path
        self.glossary = set()
        if load:
            self.glossary = self.load()
        
    def add(self, new_words):
        self.glossary.update(set(new_words))
    
    def dump(self):
        self.shuffle()
        with open(self.glossary_path, "w") as f:
            print("\n* Writing glossary to {}".format(self.glossary_path))
            f.write("\n".join(self.glossary))
        
    def load(self):
        glossary = set()
        if os.path.isfile(self.glossary_path):
            with open(self.glossary_path, "r") as f:
                print("* Loading glossary from {}".format(self.glossary_path), end = " ")
                glossary = set(f.read().split("\n"))
                print("(loaded glossary size = {})".format(len(glossary)))
                print()
        return glossary
    
    def shuffle(self): # just to avoid any possible leakage of information from words' order
        glossary = list(self.glossary)
        random.shuffle(glossary)
        self.glossary = set(glossary)

class Parser():
    def __init__(self, glossary_path, load=True):
        self.glossary_ = Glossary(glossary_path, load)

    def parse_path(self, path):
        if not os.path.isfile(path):
            print("ERROR. {} is not a file".format(path))
            return
        
        print("parsing a file | {}".format(path).ljust(120), end = "| ")
        _glossary_size_before = len(self.glossary)
        with open(path) as f:
            content_str = f.read()
            words = extract_words(content_str)
            self.glossary_.add(words)
            
            _nwords = len(words)
            _glossary_size_after = len(self.glossary)
            _nnew = _glossary_size_after-_glossary_size_before
            print("found {0: <10} new {1: <10} glossary size {2} => {3}".format(_nwords, _nnew, _glossary_size_before, _glossary_size_after))
            
    def parse_paths(self, paths):
        for path in paths:
            self.parse_path(path)
    
    def parse_files(self, directory, files):
        files = [file for file in files if os.path.splitext(file)[1] in Extensions]
        paths = [os.path.join(directory, file) for file in files]
        self.parse_paths(paths)
             
    def parse_directory(self, directory_path, recursive):
        if not os.path.isdir(directory_path):
            print("ERROR. {} is not a directory".format(directory_path))
            return
        
        for root, dirs, files in os.walk(directory_path):
            self.parse_files(root, files)
            if not recursive:
                break
    def parse(self, path, recursive=False):
        if os.path.isfile(path):
            self.parse_path(path)
        elif os.path.isdir(path):
            self.parse_directory(path, recursive)
        else:
            print("ERROR. {} should be either a file or a directory")
    
    def dump(self):
        self.glossary_.dump()
    
    @property
    def glossary(self):
        return self.glossary_.glossary

def parse_args():
    description = 'Basic Glossary Extractor'
    example = "Example:\tpython glossary.py --input_data_path ExampleInput --glossary_path glossary.txt --load_glossary 0 --recursive 1"
    example = ">>>  " + example

    arg_parser = argparse.ArgumentParser(description=description, epilog=example)
    arg_parser.add_argument('--input_data_path', type=str, required=True,
                    help="a path to a directory or a file that contains words to extract")
    arg_parser.add_argument('--glossary_path', type=str, required=True,
                    help='a path to glossary file that will contains the words')
    arg_parser.add_argument('--load_glossary', type=int, choices = [0,1], default=0, required=False,
                    help='either to load the existing glossary or ignore it (ignoring is actually overiding it)')
    arg_parser.add_argument('--recursive', type=int, choices = [0,1], default=False, required=False,
                    help='if input_data_path is a directory - to run recursively on all internal files or not')
    # arg_parser.add_argument('--verbose', type=bool, default=False, required=False)

    args = arg_parser.parse_args()
    
    return args

if __name__ == '__main__':
    args = parse_args()
    print()
    print("* NOTE: Accepted extensions are: {}\n".format(Extensions))
    parser = Parser(glossary_path = args.glossary_path, load = bool(args.load_glossary))
    parser.parse(path = args.input_data_path, recursive=bool(args.recursive))
    parser.dump()


