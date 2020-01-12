# TREC-combining-all-results

Using the results of all teams to produce a feature vector.

# Install

Just clone this repo and run `make install`

# Testing

Some basic nosetests are implemented and can be run with `make tests`

# Running

A visualization of the data flow for this project, can be viewed here: https://www.yworks.com/yed-live/

Just open the `ProjectVisualization.graphml` file there.

To make the whole pipeline run, it's fastest to use the `pipeline_runner.py`. 
As a first step with this programm you could execute it like this:
```
python3 pipeline_runner.py --do-everything-with-default-values True --preview True
```
This will show you which commands it would execute.
As the default example we want to train on the trec-19-web-run-files, which you should put at the input_folder
location.
The right qrels for this task are contained in some resource folder of anserini.
If you now rename one of the run files to `chosen-run-file.gz` you can execute the whole pipeline with
```
python3 pipeline_runner.py -d True
```
The result of the evaluation will be printed to stdout.
The files which where created on the way should all be in the /tmp folder.

You could now take a look at `python3 pipeline_runner.py --help`. 
The description of some arguments, starts with "If given,".
It's important to provide all these arguments if you want to run the entire pipeline.
If you still want to fall back on their default values you should set them to ""

To achieve the same result as before you could run
```
python3 pipeline_runner.py -r "" -c "" -a "" -e "" # which is equivalent to
python3 pipeline_runner.py -r data/trec-19-web-run-files/trec19/web/ \
                           -c data/trec-19-web-run-files/trec19/web/chosen-run-file.gz \
                           -a 1 \
                           -e True
```
