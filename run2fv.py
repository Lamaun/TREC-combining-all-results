#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import os
import gzip
import argparse

defaults = ["test/resources/input_single_topic",
            "ranklib.fv", "test/resources/test.qrel", True]


def msgExit(msg="", rc=0):
    print(msg)
    exit(rc)


def execute(input_folder=defaults[0], output_file=defaults[1], qrel_file=defaults[2], trainable=defaults[3]):
    out = dict()
    queryset = dict()
    teamset = set()
    for filename in os.listdir(input_folder):
        f = gzip.open(os.path.join(input_folder, filename), "rt")
        for line in f:
            words = line.split()
            # words[0] query id (with defaults: 51-100)
            # words[1] always Q0 -> irrelevant
            # words[2] alphanumeric docid (something like clueweb09-en0000-16-19379)
            # words[3] rank (from 1- whatever)
            # words[4] score (depends on the team, should decrease with score)
            # words[5] runTag (team)
            if(len(words) < 6):
                continue
            teamset.add(words[5])
            out[words[2]] = out.get(words[2], dict())
            out[words[2]][words[0]] = out[words[2]].get(words[0], dict())
            out[words[2]][words[0]][words[5]] = [words[3], words[4], 1]
            if not trainable:
                queryset[words[2]] = queryset.get(
                    words[2], [])+[(words[0], "0")]
        f.close()
    teamset = list(teamset)
    teamset = sorted(teamset)
    if trainable:
        f = open(qrel_file, "rt")
        for line in f:
            words = line.split()
            # words[0] query id (with defaults: 51-100)
            # words[1] always 0 -> irrelevant
            # words[2] alphanumeric docid (something like clueweb09-en0000-16-19379)
            # words[3] assigned relevance (mostly between -2 and 2)
            if(len(words) < 4):
                continue
            queryset[words[2]] = queryset.get(
                words[2], [])+[(words[0], words[3])]
        f.close()
    f = open(output_file, "w+")
    f.write("# Feature-Descriptions\n#\n")
    feature_id = 1
    for team in teamset:
        f.write("# "+str(feature_id)+": Run '" +
                team+"' - Position (default=-1000)\n")
        feature_id += 1
        f.write("# "+str(feature_id)+": Run '" +
                team+"' - Score (default=-1000)\n")
        feature_id += 1
        f.write("# "+str(feature_id)+": Run '"+team +
                "' - document listed in the ranking (0=no; 1=yes)\n#\n")
        feature_id += 1
    for doc in out:
        for query in queryset.get(doc, []):
            s = query[1] + " qid:" + str(query[0])+" "
            feature_id = 1
            for team in teamset:
                for score in out.get(doc, dict()).get(query[0], dict()).get(team, [-1000, -1000, 0]):
                    s += str(feature_id)+":"+str(score)+" "
                    feature_id += 1
            f.write(s+" # "+doc+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Creates a feature vector file (See https://sourceforge.net/p/lemur/wiki/RankLib%20File%20Format/) from run files ')
    parser.add_argument('-i', '--input_folder', default=defaults[0], type=str,
                        help='All files in the directory will be read. Default:'+str(defaults[0]))
    parser.add_argument('-o', '--output_file',
                        default=defaults[1], type=str,  help='Where to write to. Default:'+str(defaults[1]))
    parser.add_argument('-q', '--qrel_file', default=defaults[2], type=str,
                        help='The qrel file needed for the target relevance. Default:'+str(defaults[2]))
    parser.add_argument('-t', '--trainable', default=defaults[3], type=bool,
                        help='If set to False we will not read the qrel file and just write every score from' +
                        'the run files into the feature vector. Default:'+str(defaults[3]))
    try:  # If you want bash completion take a look at https://pypi.org/project/argcomplete/
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass
    args = parser.parse_args()
    execute(args.input_folder, args.output_file,
            args.qrel_file, args.trainable)
