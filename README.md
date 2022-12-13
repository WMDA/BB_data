# BB_data

A repo of all the scripts and notebooks used to clean and analyse the data from Examining the Longitudinal Trajectory of Biopsychosocial Difficulties in Anorexia Nervosa Within a Bayesian Framework paper.

## Repo structure

analysis_scripts folder contains notebooks used to conduct the PCA as well as to build the bayesian models

data_preprocessing folder contains scripts to calculate and impute the questionnaire measures

storage folder contains scripts to interact with remote MYSQL/marnia db server which stores the data on

helper_scripts contains scripts to be used by members of the team who are less familar with python

## Basic usages

This is the basic usage if data wants to be replicated.

1) Install the repo
```pip install . ```

2) Add a .env file to the base directory with absolute paths to directories where data is stored like so:

```
root= absolute path to root data storage
t1= absolute path to time point one data
t2=  absolute path to time point two data
(the following config options are used IF a remote mysql server is used)
host=<ip address of remote mysql server>
user=<base64 encoded username>
password=<base64 encoded password>
```
NO CREDENTIALS FOR SQL SERVERS ARE STORED ON GITHUB

3)  All scripts are run

```
python3 script.py
```

Apart from ipynb notebooks which need to be viewed using a ipynb platform.


