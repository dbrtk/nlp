# NLP

NLP implements algorithms for feature extraction; it extracts topics from large amounts of files that contain text. Moreover,it does some preparatory text processing; i.e. lemmatization, language-detection. 

The dependencies:
* rmxbin (https://github.com/dbrtk/rmxbin);
* pyhton3.

All pyhton dependencies are listed in the requirements (https://github.com/dbrtk/nlp/blob/master/requirements.txt).

## Installation

1. Clone nlp:
```
git clone git@github.com:dbrtk/nlp.git
```
2. Create a virtual enviroment:
```
python3 -m venv --copies env
```
3. Activate:
```
. env/bin/activate
```
4. Install nlp:
```
cd nlp
pip install -e .
cd
```
5. Create a directory where nlp will store some data and save text files. 
6. One of the requirements is nltk (Natural Language Toolkit); it will be installed along with other packages. But it is imoportant to download nltk_data:
```
. env/bin/activate
python -m nltk.downloader all
```
OR
```
. env/bin/activate
python -m nltk.downloader all -d /path/to/nltk_data

```

Nlp can be connected to a django project, it contains a django app (https://github.com/dbrtk/nlp/tree/master/nlp/api/djapp). There is a sample of a django project in proximity-bot (https://github.com/dbrtk/proximity-bot). Before running NLP, it is very important to update some variables in the configuraiton file (section below).

### Configuration file

The configuration file can be found within the nlp package (https://github.com/dbrtk/nlp/blob/master/nlp/config/__init__.py). The variables that need to be updated are:
* `PROXIMITYBOT_IS_REMOTE` - (https://github.com/dbrtk/nlp/blob/master/nlp/config/__init__.py#L12). this variable defines whether proximity-bot runs on a separate server;
* `PROXIMITYBOT_HOST_NAME` - host name of the proximity-bot server;
* `PROXIMITYBOT_ENDPOINT` - http endpoint to the proximity-bot server;
* `DATA_ROOT` - path where nlp can store files and matrices when processing materials. A data directory can exist under: 
os.path.join(os.environ['HOME'], 'data'. This directory should be created by user (see above); 
* `RSYNC_SCRIPTS_PATH` - path to the location of rmxbin (https://github.com/dbrtk/rmxbin);
* `NLTK_DATA_PATH` - path to the directory that holds nltk data.


