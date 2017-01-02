### Introduction

A Python script to crawl through .docx files, parse out interesting information and save to a MongoDB collection. Specifically the documents hold information relating to patient dose estimates, but this will work with any tabular information contained in Word documents.

### Assumptions

The data are written into tables in template Word files, but the templates are often modified to suit the specific case. As such the script does some guesswork as to pairing up key:value pairs from tables. 

### Requirements

You'll need to have an instance of MongoDB running in the background, so first run `mongod` in a terminal. Installation instructions for MongoDB can be found [here](https://docs.mongodb.com/manual/installation/)

### Installation

The packages required to run the scripts can be installed using:

`pip install -r requirements.txt`

### Usage

###### Inserting data

Inserting data into the database can be done using:

`python insertdata.py`

or by importing the package:

```python
from pydocxdb import analysedata
analysedata()
```

You can check that your data has been correctly inserted in the database using the mongo CLI:

`db.pat_dose_ests.find().pretty()`

###### Analysing data

I've written a couple of quick and dirty examples to show how the database can be queried to return data which can be plotted and analysed further. The examples are contained in `analysedata.py`.

### Caveats

The scripts aren't going to be clever at adapting to Word documents that deviate significantly from the template of | Key | Value |, so mileage may vary. This is a work in progress.

 
