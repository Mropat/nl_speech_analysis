import nltk
import os
import argparse
from nltk import ngrams
from nltk import FreqDist
import matplotlib


def get_nl_grams(directory):
    def parse_folder(directory):
        for filename in os.listdir(directory):
            yield os.path.join(directory, filename)   
            
                
    name = str(global_args.indir).split("/")[-2]
    longest_ngram_hits = open(name+"_res_dump.txt", "w") 
    ngram_freqs = {}
    for n in range(2, 50):
        nlgrams = []
        for filename in parse_folder(directory):
            words = []
            with open(filename, "r") as fh:
                liones = fh.readlines()
                for line in liones:
                    if " --> " in line:
                        continue
                    elif line == "\n":
                        continue
                    else:
                        for word in line.strip().split():
                            words.append(word.lower())

            for ngrm in ngrams(words[20:-50], n):
                nlgrams.append(ngrm)
        freq_grams = FreqDist(nlgrams)
        freq_grams_iter = dict(freq_grams)
        for ngram, count in freq_grams.items():
            if count > 1:
                continue
            else:
                freq_grams_iter.pop(ngram)

        if len(freq_grams_iter) > 0:
            for ngram, count in ngram_freqs.items():
                if (count * n*(1+n/2)) > 15*n:
                    if any([" ".join(ngram) in " ".join(x) for x, c in freq_grams_iter.items()]) == False:
                        longest_ngram_hits.write(str(count) + ': ' + ' '.join(ngram) + "\n")
            ngram_freqs = freq_grams_iter
        else:
            for ngram, count in ngram_freqs.items():
                longest_ngram_hits.write(str(count) + ': ' + ' '.join(ngram) + "\n")
            break
    longest_ngram_hits.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--indir", required=True)
    global_args = parser.parse_args()
    get_nl_grams(global_args.indir)
