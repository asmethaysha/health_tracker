# health_tracker

This is a web application which will be personal health tracker for our users. This application is designed to help users monitor their health and wellbeing. They can log their workout data, nutrition intake, weight and sleep and visualize trends in these metrics over time to assess their health overall.

Phase0
Phase0 and its corresponding commits are related to the configuration management exercise. This is likely to have limited consequence on the larger project.

Phase1 - DONE
Phase1 is about creating a script that takes advantage of Python's random package to create test files for our ingestion system to ingest and output sqlite files. Challenges included:

File ingestion formatting and making this cooperate with table structure
Data cleaning
Pytest implementation
Using random to generate test files
Simple steps for testing data ingestion (when running locally):

First make sure there are no .csvs in ~/test_files/ and no test.db file in main project directory
Then do:
cisc594_project>python generate_test_files.py
cisc594_project>python ingest_test_files.py
cisc594_project>pytest
This phase has been tested using github's in-built testing system that is able to take advantage of pytests.

Phase2 - DONE
Phase2 is about creating a script that takes the randomized data generated in Phase1 to read from the SQLite database and output .jpg and .pkl files containing results. Challenges included:

Generalizing the extraction of tables in SQLite to DataFrames
Using and making DataFrames comply with Matplotlib
Using Pytest to test whether data is displayable
cisc594_project>python generate_test_files.py
cisc594_project>python ingest_test_files.py
cisc594_project>python graph_results.py
cisc594_project>pytest
Phase3 - DONE
We created the GUI for the Application. Using the UI, user can log

Workouts
Sleep
Weight
Happiness index
Meal intake.
Processing this user data we build trends for these metrics and present to the user to study their health behavior and make informed decisions about their health.

User can view historical trends of data plotted with respect to time

Weight changes over time
Calories Burnt in workouts over time
Happiness Index reflecting mental health over time
Sleep hours trend over time
This is a reflection of over all health of the user.
