#!/usr/bin/python
import re
import nltk
import sys
import getopt
import math

n = 4 # 4-grams
k = 1 # For add-k smoothing
add_start_end_token = True
has_case_folding = True
is_log_probability = True
can_belong_to_unseen_label = True
seen_label_threshold = -4 # If exceed label then label = unseen label

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print('building language models...')

    # Initialize data structures
    labels_indexer = {} # indexer[label] = label_index
    ngrams_indexer = {} # indexer[ngram] = ngram_index
    ngrams_counter = {} # counter[label][ngram] = ngram_count
    models = [] # models[label_index][ngram_index] = ngram_probability
    ngrams_next_index = 0 # Index to index new ngrams in models[label_index]
    with open(in_file) as f:
        for line in f:
            label, sentence = line.strip().split(' ', 1)
            if add_start_end_token:
                sentence = '^' + sentence + '$'
            # If label not indexed, index it in the indexer and create a new row in the models list
            if label not in labels_indexer:
                labels_indexer[label] = len(models)
                ngrams_counter[label] = {}
                models.append([])
            # For each n-gram, lower the letter case, index the n-gram, and increment the n-gram count
            for i in range(len(sentence) - n):
                if has_case_folding:
                    ngram = tuple([ch.lower() for ch in sentence[i:i+n]])
                else:
                    ngram = tuple([ch for ch in sentence[i:i+n]])
                if ngram not in ngrams_indexer:
                    ngrams_indexer[ngram] = ngrams_next_index
                    ngrams_next_index += 1
                    ngrams_counter[label][ngram] = 1
                else:
                    if ngram not in ngrams_counter[label]:
                        ngrams_counter[label][ngram] = 1
                    else:
                        ngrams_counter[label][ngram] += 1
        # N-gram counts are inside dictionaries that have their own key sets so we add all to the model
        for label, label_index in labels_indexer.items():
            models[label_index] = [1 for ngram in ngrams_indexer]
            for ngram, ngram_count in ngrams_counter[label].items():
                ngram_index = ngrams_indexer[ngram]
                models[label_index][ngram_index] = ngram_count
            models[label_index] = [ngram_count / len(ngrams_indexer) for ngram_count in models[label_index]]
    return (labels_indexer, ngrams_indexer, models)

def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print('testing language models...')

    labels_indexer, ngrams_indexer, models = LM
    with open(out_file, 'w') as g:
        with open(in_file) as f:
            for line in f:
                # Initialize the probabilities for each label
                probabilities = {label: (0 if is_log_probability else 1) for label in labels_indexer} # probabilities[label] = probability
                sentence = line.strip()
                num_ngrams = len(sentence) - n
                for i in range(num_ngrams):
                    ngram = tuple([ch.lower() for ch in sentence[i:i+n]])
                    if ngram not in ngrams_indexer:
                        continue
                    ngram_index = ngrams_indexer[ngram]
                    # Retrieve probability based on label and n-gram
                    for label, label_index in labels_indexer.items():
                        ngram_probability = models[label_index][ngram_index]
                        if is_log_probability and ngram_probability:
                            probabilities[label] += math.log(ngram_probability)
                        else:
                            # 1. Multiply probabilities regardless of zero probability
                            # probabilities[label] *= ngram_probability

                            # 2. Multiply non-zero probabilities
                            # '''
                            if ngram_probability:
                                probabilities[label] *= ngram_probability
                            # '''
                label = max(probabilities, key=probabilities.get)
                if can_belong_to_unseen_label:
                    probabilities = { label: probability / num_ngrams for (label, probability) in probabilities.items() }
                    if max(probabilities.values()) > seen_label_threshold:
                        label = 'other'
                g.write('{label} {sentence}'.format(label=label, sentence=line))

def usage():
    print('usage: ' + sys.argv[0] + ' -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file')

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except (getopt.GetoptError, err) as e:
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
