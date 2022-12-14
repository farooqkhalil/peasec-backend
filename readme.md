# To setup project in PyCharm
 
- cd Project\Folder\Path\toPipfile
- C:\Users\DELL\Workspaces\peasec_restapi>pip install --user pipenv
- C:\Users\DELL\Workspaces\peasec_restapi>python -m site --user-base
  result of above is the location for pipenv.exe
- In database.py change
  - SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:password@db:3306/restapi" 
  - => SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:password@localhost:3306/restapi"
- Setup pycharm using Pipfile
- Run main.py

# To Run Docker
- In database.py change
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:password@localhost:3306/restapi"
=> SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:password@db:3306/restapi"
- run: docker compose up
