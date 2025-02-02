This is a web application which will be personal health tracker for our users. This application is designed to help users monitor their health and wellbeing. They can log their workout data, nutrition intake, weight and sleep and visualize trends in these metrics over time to assess their health overall.


# Phase0
Phase0 and its corresponding commits are related to the configuration management exercise. This is likely to have limited consequence on the larger project.

# Phase1 - DONE
Phase1 is about creating a script that takes advantage of Python's random package to create test files for our ingestion system to ingest and output sqlite files. 
Challenges included: 
- file ingestion formatting and making this cooperate with table structure
- data cleaning
- pytest implementation
- using random to generate test files

Simple steps for testing data ingestion (when running locally):
- First make sure there are no .csvs in ~/test_files/ and no test.db file in main project directory
- Then do:
```
cisc594_project>python generate_test_files.py
cisc594_project>python ingest_test_files.py
cisc594_project>pytest
```
This phase has been tested using github's in-built testing system that is able to take advantage of pytests.
# Phase2 - TBD
This phase will focus on data processing and visualization to allow users to develop effective ways to analyze and understand their data. 

# Phase3 - TBD
This phase will focus on UI development.
