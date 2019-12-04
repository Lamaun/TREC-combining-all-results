#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import subprocess
import math
import random  # random.randint(0,32)
import os
import argparse
import time  # time.time()
import tempfile  # tempfile.TemporaryDirectory()

defaults = ["ranklib.fv", "P@10"]


def msgExit(msg="", rc=0):
    print(msg)
    exit(rc)


def execute(input_file=defaults[0], metric=defaults[1]):
    print([metric, "used_time in seconds", "modelsize in byte"])
    modelname="/tmp/trec_combining_all_results_current_model"
    for i in range(0,10):
        train_ranklib_model(input_file, str(i), metric,modelname)
        

def use_ranklib_model(feature_vector_file, ranklib_algorithm, metric_to_train, model_file):
    #Not implemented yet
    return True

def train_ranklib_model(feature_vector_file, ranklib_algorithm, metric_to_train, model_file):
    command = [
        'third-party/anserini/target/appassembler/bin/RankLibCli',
        '-ranker', ranklib_algorithm,
        '-train', feature_vector_file,
        '-metric2t', metric_to_train,
        '-save', model_file
    ]
    # -ranker <type>	Specify which ranking algorithm to use
    # 0: MART (gradient boosted regression tree)
    # 1: RankNet
    # 2: RankBoost
    # 3: AdaRank
    # 4: Coordinate Ascent
    # 6: LambdaMART
    # 7: ListNet
    # 8: Random Forests
    # 9: Linear Regression
    # [ -metric2t <metric> ]	Metric to optimize on the training data. Supported: MAP, NDCG@k, DCG@k, P@k, RR@k, ERR@k (default=ERR@10)
    start = time.time()
    output = subprocess.check_output(command)
    used_time = time.time()-start
    modelsize = os.path.getsize(model_file)
    output = str(output).split("on training data: ")[1].split("\\n")[0]
    print([metric_to_train, "used_time in seconds", "modelsize in byte"])
    print([output, used_time, modelsize])
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Wraps the RankLibCli from Anserini and trains different models and outputs simple statistics.')
    parser.add_argument(
        '-i', '--fv_file', default=defaults[0], type=str,  help='the input file. Default:'+str(defaults[0]))
    parser.add_argument(
        '-m', '--metric', default=defaults[1], type=str,
        help='Metric to optimize on the training data. Supported: MAP, NDCG@k, DCG@k, P@k, RR@k, ERR@k Default:'+str(defaults[1]))
    try:  # If you want bash completion take a look at https://pypi.org/project/argcomplete/
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass
    args = parser.parse_args()
    execute(args.fv_file,args.metric)
