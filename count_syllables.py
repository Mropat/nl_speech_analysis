import nltk
from nltk.corpus import cmudict
import datetime
import nltk.data
from datetime import timedelta
import hyphen
import matplotlib
import matplotlib.pyplot as plt
import os
import argparse
import numpy as np
matplotlib.style.use("ggplot")
d = cmudict.dict()


def get_speech_stat(dirname):

    def get_seconds(timestamp_duration):
        return int(timestamp_duration.strftime("%S")) + int(timestamp_duration.strftime("%H"))*3600 + int(timestamp_duration.strftime("%M"))*60

    for filename in parse_folder(dirname):
        with open(filename, "r") as fh:
            liones = fh.readlines()
            zero_time = datetime.datetime.strptime(
                "00:00:00.000", "%H:%M:%S.%f")
            time_chatting = datetime.datetime.strptime(
                "00:00:00.000", "%H:%M:%S.%f")
            words = []
            syllables = 0
            semiwords = []
            timestamps = ""
            for line in liones:
                if " --> " in line:
                    timestamps = line.strip().split(" --> ")
                    stamp_delta = datetime.datetime.strptime(
                        timestamps[1], "%H:%M:%S.%f") - datetime.datetime.strptime(timestamps[0], "%H:%M:%S.%f")
                    if get_seconds(zero_time + stamp_delta) < 8:
                        time_chatting += stamp_delta

                elif line == "\n":
                    continue
                else:
                    linecontent = [w.lower() for w in line.strip().split()]
                    for word in linecontent:
                        if word in d:
                            words.append(word)
                            syllables += len(d[word])
                        else:
                            semiwords.append(word)
                            if set('aeioyu').intersection(word.lower()):
                                for letter in word:
                                    if letter in "aeoiyu":
                                        syllables += 1
                            elif len(word) < 6:
                                syllables += len(word)

            seconds_chatting = get_seconds(time_chatting)
            syllable_speed = syllables / seconds_chatting
            yield syllable_speed, filename.split("/")[-1][:-7]


#        print(str(len(words)) + " total words")
#        print(str(len(semiwords)) + " words not recognized")
#        print(str(syllables + semiword_vowels) + " syllables")
#        print(str((syllables + semiword_vowels)/seconds_chatting) + " syl/second")
#        print(time_chatting.strftime('%H:%M:%S.%f ')[:-4].replace(",", "."))
#        print(timestamps[1])
#        print(semiwords)

def plot_speeds(dirname):
    sylspeed = []
    fnames = []
    for syl, fname in get_speech_stat(dirname):
        sylspeed.append(syl)
        fnames.append(fname)
    sylspeed.reverse()
    fnames.reverse()

    sylspeed_avg = []
    offset = 31
    for i in range(len(sylspeed)-(offset-1)):
        sylspeed_avg.append(np.mean(sylspeed[i:i+offset]))

    plt.plot(range(len(sylspeed)), sylspeed, lw=0.1, color="red")
    plt.plot(range(int((offset-1)/2), len(sylspeed)-int((offset-1)/2)),
             sylspeed_avg, lw=1, color="blue")
    plt.axis([0, len(sylspeed), 0, max(sylspeed) + 1])
    plt.savefig("lion.pdf")

    print("Slowest episode: " + fnames[np.argmin(sylspeed)])
    print("Fastest episode: " + fnames[np.argmax(sylspeed)])


def parse_folder(directory):
    for filename in sorted(os.listdir(directory)):
        yield os.path.join(directory, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--indir", required=True,
                        default="/home/maria/Documents/NLstat/working/binding_of_isaac/antibirth/")
    global_args = parser.parse_args()
    plot_speeds(global_args.indir)
