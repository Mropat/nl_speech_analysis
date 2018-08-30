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

    nlgrams = []

    for n in range(4, 5):
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

            for ngrm in ngrams(words[100:-100], n):
                nlgrams.append(ngrm)
    freq_grams = FreqDist(nlgrams).most_common(500)
    print("\n".join(map(lambda ng: str(ng[1]) + ': ' + ' '.join(ng[0]), freq_grams)))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--indir", required=True)
    global_args = parser.parse_args()
    get_nl_grams(global_args.indir)
