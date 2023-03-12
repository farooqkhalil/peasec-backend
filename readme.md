# To setup project in PyCharm
 
- cd Project\Folder\Path\toPipfile
- C:\Users\DELL\Workspaces\peasec_restapi>pip install --user pipenv
- C:\Users\DELL\Workspaces\peasec_restapi>python -m site --user-base
  result of above is the location for pipenv.exe
- In database.py set
  - SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:password@localhost:3306/restapi"
- Setup pycharm using Pipfile
- Run main.py

### To Run Docker
- In database.py set
  - SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:password@db:3306/restapi"
- run: docker compose up
- If you see an Error: "sqlalchemy.exc.DatabaseError: (mysql.connector.errors.DatabaseError) 2003 (HY000): Can't connect to MySQL server on 'db:3306' (111)" - 
  - wait for SQL DB container to start - logs will show "/usr/sbin/mysqld: ready for connections" 
  - then re-run WebApp container


### Security Tasks to do upon deployment
- Change Access Key in app_utils
- Remove access key from git repo
- Change default password of SQL DB


## Explaining File Structure
#### models.py
- Used to declare table structure to store tables in DataBase
- refer to these classes and instances declared here interact with the database
### schemas.py
- Here we declare pydantic models
- Used to define Schema to format Input and Output formats
### database.py
- Connection to Database is configured in this class
### main.py
- Entry point for all the APIs
- Initial Verification like user authentication is done here
- The requests are then forwarded to crud.py
### crud.py
- Different functions for CRUD are declared to provide data to main.py
- Here we execute crud operations on database
### app_utils.py
- Utility functions
  - Create Access Token
  - Decode Access Token
  - Hate-speech Detection
  - Expiry Date Determination


## Improvements
### Content Moderation
#### Hatespeech
- Hatespeech detection has been implemented under app_utils using library "better_profanity"
- This can be improved furhter by adding word list that should be classified as hate speech

#### Content Verification/Validation
- An option to validate the reports using official channels would be a great addition and potentially make those reports even more trustworthy
- functionality to verify content using web-of-trust concept can be included as well
  - This can be done by allowing users to approve / disapprove content of a report
  - No. of approvals/disapprovals should be then weighted by trustworthiness of the user
  - This weighted score should determine if a report is real or fake

### Criticality Weightage of Events
- Except for the expiry function, at the moment all the events are assumed to have same criticality
- This can be further improved by assigning certain criticality flags to each event and highlight the critical events in sequence of criticality factor

### User Management
- Add Email address for user registration
- Add functionality for password reset