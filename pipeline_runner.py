#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import subprocess
import argparse

defaults = {"run_file_folder": "data/trec-19-web-run-files/trec19/web/",
            "qrel_file": "third-party/anserini/src/main/resources/topics-and-qrels/qrels.web.51-100.txt",
            "topics_file": "third-party/anserini/src/main/resources/topics-and-qrels/topics.web.51-100.txt",
            "topicreader": "Webxml",
            "chosen_run_file": "data/trec-19-web-run-files/trec19/web/chosen-run-file.gz",
            "output_file_of_chosen_run_file_reranking": "/tmp/reranked.run",
            "runtag": "CombinedResultsRunTag",
            "feature_vector_file_trainable": "/tmp/features_with_relevance.fv",
            "feature_vector_file_complete": "/tmp/only_features.fv",
            "ltr_model": "/tmp/model",
            "algorithm_ltr": "1",
            "evaluate": True,
            "metric": "P@10",
            "preview": False,
            "do-everything-with-default-values": False}


def execute(run_file_folder=defaults["run_file_folder"],
            qrel_file=defaults["qrel_file"],
            topics_file=defaults["topics_file"],
            topicreader=defaults["topicreader"],
            chosen_run_file=defaults["chosen_run_file"],
            output_file_of_chosen_run_file_reranking=defaults[
                "output_file_of_chosen_run_file_reranking"],
            runtag=defaults["runtag"],
            feature_vector_file_trainable=defaults["feature_vector_file_trainable"],
            feature_vector_file_complete=defaults["feature_vector_file_complete"],
            ltr_model=defaults["ltr_model"],
            algorithm_ltr=defaults["algorithm_ltr"],
            evaluate=defaults["evaluate"],
            metric=defaults["metric"],
            preview=defaults["preview"]):
    if(run_file_folder is not None):
        if(len(run_file_folder) == 0):
            run_file_folder = defaults["run_file_folder"]
        if not preview:
            import run2fv
            run2fv.execute(input_folder=run_file_folder,
                           output_file=feature_vector_file_trainable, qrel_file=qrel_file, combine=False)
            run2fv.execute(input_folder=run_file_folder,
                           output_file=feature_vector_file_complete, qrel_file=qrel_file, combine=True)
        else:
            print('python3 run2fv.py --input_folder "{}" --output_file "{}" --qrel_file "{}"'.format(
                run_file_folder, feature_vector_file_trainable, qrel_file))
            print('python3 run2fv.py --input_folder "{}" --output_file "{}" --qrel_file "{}" --combine'.format(
                run_file_folder, feature_vector_file_complete, qrel_file))
    else:
        run_file_folder = defaults["run_file_folder"]
    if(algorithm_ltr is not None):
        if(len(algorithm_ltr) == 0):
            algorithm_ltr = defaults["algorithm_ltr"]
        if not preview:
            import train
            train.train_ranklib_model(feature_vector_file=feature_vector_file_trainable, ranklib_algorithm=algorithm_ltr,
                                      metric_to_train=metric, model_file=ltr_model)
        else:
            print('third-party/anserini/target/appassembler/bin/RankLibCli',
                  '-ranker', algorithm_ltr,
                  '-train', feature_vector_file_trainable,
                  '-metric2t', metric,
                  '-save', ltr_model)
    else:
        algorithm_ltr = defaults["algorithm_ltr"]
    if(chosen_run_file is not None):
        if(len(chosen_run_file) == 0):
            chosen_run_file = defaults["chosen_run_file"]
        command = ["third-party/anserini/target/appassembler/bin/RerankExistingRunfile",
                   "-output", output_file_of_chosen_run_file_reranking,
                   "-runFileToRerank", chosen_run_file,
                   "-topicreader", topicreader,
                   "-topics", topics_file,
                   "-bm25",
                   "-arbitraryScoreTieBreak",
                   "-model", ltr_model,
                   "-experimental.args",
                   "-rankLibFeatureVectorFile="+feature_vector_file_complete,
                   "-runtag", runtag]
        if not preview:
            subprocess.check_output(command, stderr=subprocess.DEVNULL)
        else:
            print(" ".join(command))
    else:
        chosen_run_file = defaults["chosen_run_file"]
    if(evaluate is not None):
        command = ["third-party/anserini/target/appassembler/bin/Eval",
                   "-run", chosen_run_file,
                   "-qrels", qrel_file]
        if not preview:
            output = subprocess.check_output(command)
            print("Chosen Run File:\n------\n", output.decode("utf-8"))
        else:
            print(" ".join(command))

        command = ["third-party/anserini/target/appassembler/bin/Eval",
                   "-run", output_file_of_chosen_run_file_reranking,
                   "-qrels", qrel_file]
        if not preview:
            output = subprocess.check_output(command)
            print("Reranked Run File:\n------\n", output.decode("utf-8"))
        else:
            print(" ".join(command))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Overview of algorithms to use for LTR
# 0: MART (gradient boosted regression tree)
# 1: RankNet
# 2: RankBoost
# 3: AdaRank
# 4: Coordinate Ascent
# 6: LambdaMART
# 7: ListNet
# 8: Random Forests
# 9: Linear Regression

Recommended to use the -p True flag first, so you can see what this programm will do for you.
    """)
    parser.add_argument('-r', '--run-file-folder', type=str,  help='If given, we convert the runfiles in the folder to a feature vector' +
                        ' file by using the scores each document got for different queries as a feature vector for that document. Default:'+str(defaults["run_file_folder"]))
    parser.add_argument('-q', '--qrel-file', default=defaults["qrel_file"], type=str,
                        help='Which qrel file to use for run-files to feature vector conversion and reranking. Default:'+str(defaults["qrel_file"]))
    parser.add_argument('-t', '--topics-file', default=defaults["topics_file"], type=str,
                        help='Which topic file to use for reranking. Default:'+str(defaults["topics_file"]))
    parser.add_argument('-tr', '--topicreader', default=defaults["topicreader"], type=str,
                        help='Which topicreader to use for reranking. Default:'+str(defaults["topicreader"]))
    parser.add_argument('-c', '--chosen-run-file', type=str,  help='If given, we rerank the given run-file with a learned LTR model' +
                        ' on the feature vector file. Default:'+str(defaults["chosen_run_file"]))
    parser.add_argument('-o', '--output-file-of-chosen-run-file-reranking', default=defaults["output_file_of_chosen_run_file_reranking"], type=str,
                        help='Reranked run-file ready to be evaluated. Default:'+str(defaults["output_file_of_chosen_run_file_reranking"]))
    parser.add_argument('-rt', '--runtag', default=defaults["runtag"], type=str,
                        help='Runtag for the reranker. Default:'+str(defaults["runtag"]))
    parser.add_argument('-ft', '--feature-vector-file-trainable', default=defaults["feature_vector_file_trainable"],
                        type=str,  help='Name of the file with the feature vectors and their assigned relevance. Default:'+str(defaults["feature_vector_file_trainable"]))
    parser.add_argument('-fc', '--feature-vector-file-complete', default=defaults["feature_vector_file_complete"],
                        type=str,  help='Name of the file with the feature vectors. Default:'+str(defaults["feature_vector_file_complete"]))
    parser.add_argument('-l', '--ltr-model', default=defaults["ltr_model"], type=str,
                        help='Name of the file the LTR model is (to be) saved in. Default:'+str(defaults["ltr_model"]))
    parser.add_argument('-a', '--algorithm-ltr', type=str,
                        help='If given, we train a model of the given type on the feature vector file. Default:'+str(defaults["algorithm_ltr"]))
    parser.add_argument('-m', '--metric', type=str, default=defaults["metric"],
                        help='metric to use in the training. Supported: MAP, NDCG@k, DCG@k, P@k, RR@k, ERR@k. Default:'+str(defaults["metric"]))
    parser.add_argument('-e', '--evaluate', type=bool,
                        help='If given, we use anserini Eval on the run file and the reranked run file. Default:'+str(defaults["evaluate"]))
    parser.add_argument('-p', '--preview', type=bool, default=defaults["preview"],
                        help='Only print commands which would be executed. Default:'+str(defaults["preview"]))
    parser.add_argument('-d', '--do-everything-with-default-values', type=bool, default=defaults["do-everything-with-default-values"],
                        help='Every other argument exept -p will be overwritten by this. ' +
                        'This also means the entire pipeline will be executed. Default:'+str(defaults["do-everything-with-default-values"]))
    try:  # If you want bash completion take a look at https://pypi.org/project/argcomplete/
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass
    args = parser.parse_args()
    if(not args.do_everything_with_default_values):
        execute(run_file_folder=args.run_file_folder,
                qrel_file=args.qrel_file,
                topics_file=args.topics_file,
                topicreader=args.topicreader,
                chosen_run_file=args.chosen_run_file,
                output_file_of_chosen_run_file_reranking=args.output_file_of_chosen_run_file_reranking,
                runtag=args.runtag,
                feature_vector_file_trainable=args.feature_vector_file_trainable,
                feature_vector_file_complete=args.feature_vector_file_complete,
                ltr_model=args.ltr_model,
                algorithm_ltr=args.algorithm_ltr,
                metric=args.metric,
                evaluate=args.evaluate,
                preview=args.preview)
    else:
        execute(preview=args.preview)
