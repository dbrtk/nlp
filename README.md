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

Nlp can be connected to a django project, it contains a django app (https://github.com/dbrtk/nlp/tree/master/nlp/api/djapp). There is a sample of a django project in proximity-bot (https://github.com/dbrtk/proximity-bot).
