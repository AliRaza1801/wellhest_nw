INSTALLATION

1. Create a env variable:

    a. pip install venv
    
    b. pip -m venv env_name
    
    c. './env_name/scripts/activate'

2. Install dependencies:

    a. pip install -r requirement.txt

3. To create Database:

    a. Create a mysql database(name = wellhestdb) and the password as 'wellhest'

4. To run db Migrations:

    a. python -m flask db migrate  # To create a migration file after changes have been made

    b. python -m flask db upgrade  # To update the database according to the new migrations
    
4. To Run Server
    
    a. set FLASK_ENV=development
    
    b. python -m flask run


5. To push PR on github

    a. Make sure to run 'pip freeze > requirement.txt'
    
    b. create a PR with name related to your work and to get it merged please mark me for review
