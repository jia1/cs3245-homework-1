#!/usr/bin/python
import re
import nltk
import sys
import getopt

n = 4

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    # This is an empty method
    # Pls implement your code in below
    labels_indexer = {} # indexer[label] = label_index
    ngrams_indexer = {} # indexer[ngram] = ngram_index
    ngrams_counter = {} # counter[label][ngram] = ngram_count
    models = [] # models[label_index][ngram_index] = ngram_probability
    ngrams_next_index = 0
    with open(in_file) as f:
        for line in f:
            label, sentence = line.strip().split(' ', 1)
            if label not in labels:
                labels[label] = len(model)
                ngrams_counter[label] = {}
                model.append([])
            for i in range(len(sentence) - n):
                ngram = tuple([ch.lower() for ch in sentence[i:i+n]])
                if ngram not in ngrams:
                    ngrams_indexer[ngram] = ngrams_next_index
                    ngrams_next_index += 1
                    ngrams_counter[label][ngram] = 1
                else:
                    ngrams_counter[label][ngram] += 1
        for label, label_index in labels.items():
            models[label_index] = [1 for ngram in ngrams_indexer]
            for ngram, ngram_count in ngrams_table[label]:
                ngram_index = ngrams_indexer[ngram]
                models[label_index][ngram_index] = ngram_count
            models[label_index] = [ngram_count / len(ngrams_indexer) for ngram_count in models[label_index]]
    return models

def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below

def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
