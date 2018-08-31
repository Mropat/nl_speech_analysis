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
import json
import ast
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
            try:
                syllable_speed = syllables / seconds_chatting
            except ZeroDivisionError:
                print(filename.split("/")[-1][:-7])
                continue

            with open("/home/maria/Documents/nl_speech_analysis/working/Uploads from Northernlion/"+filename.split("/")[-1][:-7]+".info.json",  "r") as jhandle:
                j_dict = json.loads(jhandle.read())
                yield syllable_speed, filename.split("/")[-1][:-7], j_dict["upload_date"]


def plot_speeds(dirname):
    sylspeed = []
    fnames = []
    upyear = []
    for syl, fname, year in get_speech_stat(dirname):
        sylspeed.append(syl)
        fnames.append(fname)
        upyear.append(year)
    sylspeed.reverse()
    fnames.reverse()
    upyear.reverse()

    sylspeed_avg = []
    offset = 3
    for i in range(len(sylspeed)-(offset-1)):
        sylspeed_avg.append(np.mean(sylspeed[i:i+offset]))

    plt.plot(range(len(sylspeed)), sylspeed, lw=0.1,
             color="grey", label="NLSS syl/sec per episode")
    plt.plot(range(int((offset-1)/2), len(sylspeed)-int((offset-1)/2)),
             sylspeed_avg, lw=0.5, color="black", label="%s uploads avg" % offset)

    new_year = []
    new_years =[]
    for ind, upl in enumerate(upyear):
        if upl[:4] not in new_years:
            new_year.append(ind) 
            new_years.append(upl[:4]) 

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    for ind, y in enumerate(new_year[:-1]):
        try:                
            plt.axvspan(y, new_year[ind+1], facecolor=colors[-ind], alpha=0.15)
            plt.annotate(s=str(upyear[y][:4]), xy=[y, 3.5-0.07*ind], color=colors[-ind])
        except IndexError:
            plt.axvspan(y, new_year[ind+1], facecolor=colors[0], alpha=0.15)
            plt.annotate(s=str(upyear[y][:4]), xy=[y, 3.5-0.07*ind], color=colors[0])

    plt.annotate(s=str(upyear[-1][:4]), xy=[new_year[-1], 3.5-len(new_year)*0.07])
    plt.title("NLSS speed over the years")
    plt.legend()
    plt.xlabel("Video upload order")
    plt.ylabel("Syllables/sec")
    p_name = str(dirname).split("/")[-2]
    plt.savefig("%s_lionnlss.pdf" % p_name)

    print("Slowest episode: " + fnames[np.argmin(sylspeed)])
    print("Fastest episode: " + fnames[np.argmax(sylspeed)])

    speed_dict = {}
    for ind, x in enumerate(sylspeed):
        if x in speed_dict:
            speed_dict[str(x)+"S/s (" + str(ind) + ")"] = (fnames[ind], upyear[ind])
        speed_dict[str(x)+"S/s"] = (fnames[ind], upyear[ind])

    with open (p_name+"_nl_order_nlss.txt", "w") as wh:
        for k in sorted(speed_dict):
            wh.write(str(k) +"  Uploaded:" + speed_dict[k][1] + " Title: " + speed_dict[k][0]+ "\n")


def parse_folder(directory):
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".vtt"):
            if "The Northernlion Live Super Show!" in filename:
                yield os.path.join(directory, filename)
            elif "NLSS" in filename:
                yield os.path.join(directory, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--indir", required=True,
                        default="/home/maria/Documents/NLstat/working/binding_of_isaac/antibirth/")
    global_args = parser.parse_args()
    plot_speeds(global_args.indir)
