Armada Assessment Test 1
----
This test covers reading in a csv with user login AND logout data. 
Present the user with a list of users and their total time in hours or individually.

Assumptions: There will always be a login action. | Any missing data is either `"NA"` or `np.nan` | Timestamp format is always the same

<b>How To Run:</b>
- Open project via command line or IDE
- Install requirements from requirements.txt
- - pip install -r requirements.txt
- run from main.py in IDE
- Grab all or an individual via console input


<b>Requirements Checklist:</b>
- [x] Read the data from the provided CSV file (user_activity.csv) into a suitable data
structure.
- [x] Calculate the total time spent by each student on the website in hours.
- [x] If a student logs in but does not log out, assume
that the session continues until the end of the data.
- [x] Output the student ID and their total time spent on the website in hours, sorted in
descending order of time spent.
- [x] Ensure that the output is in the following format ---
User ID: Total Time Spent (hours)
