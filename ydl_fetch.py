import os
import re
import argparse
import time
import datetime
import inflect
p = inflect.engine()


def parse_folder(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".vtt"):
            yield os.path.join(directory, filename)

def parse_vtt(directory):
    for filename in parse_folder(directory):
        with open (filename, "r+") as fh:
            mod_lines = fh.readlines()
            unique_lines = set()
            unique_lines.add("\n")
            unique_lines.add("\r")
            for ind, line in enumerate(mod_lines):
                line = re.sub('<.*?>', '',line).replace("align:start position:0%", '')
                if "-->" in line:
                    lineparts = line.rstrip().split(" --> ")
                    modpart = datetime.datetime.strptime(lineparts[-1], "%H:%M:%S.%f") + datetime.timedelta(seconds=0.010)
                    lineparts[-1] = str(modpart.strftime('%H:%M:%S,%f ')[:-4] + " \n").replace(",", ".")
                    line = " --> ".join(lineparts)
                else:
                    line = line.replace("%", " percent").replace("/", " per ").replace("-", " ")
                    for x in line.split():
                        if x.isdigit():
                            line = line.replace(x, p.number_to_words(x)).replace("-", " ")

                if line not in unique_lines:
                    mod_lines[ind] = line
                    unique_lines.add(line)
                else:
                    mod_lines[ind] = ""
                    mod_lines[ind-2] = ""
            fh.truncate(0)
            fh.seek(0)
            fh.writelines(mod_lines[10:])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--indir", required=True)
    global_args = parser.parse_args()
    parse_vtt(global_args.indir)

