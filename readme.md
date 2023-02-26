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


### Security Tasks to do upon deployment
- Change Access Key in app_utils
- Remove access key from git repo
- Change default password of SQL DB


### Improvements
- Hatespeech detection can be improved under app_utils.py
- functionality to verify content using web-of-trust concept can be included as well