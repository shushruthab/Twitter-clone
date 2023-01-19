<h1 align="center">
  Twitter-Clone
</h1>
<p align="center">
  <img src="https://img.shields.io/badge/Python-blue">
  <img src="https://img.shields.io/badge/Flask-pink">
  <img src ="https://img.shields.io/badge/PostgreSQL-green">
  <img src ="https://img.shields.io/badge/SQLAlchemy-orange">
</p>

## Project Demo
![Final App](/demo.gif)

## Description
Twitter-clone is a full stack web application built using the Python - Flask - PostgreSQL stack. The idea was not to make the app look pretty but to get the functionality right in a simplistic approach. The database has four tables and the tables are linked as below:

![Database design](db_diagram.png)

## Key Features

- Create accounts
- Authentication for login, logout users
- Search, Follow/Unfollow users
- Create/Delete messages
- Delete user account

## Getting Started

```python
# Install dependencies for server & client
pip install -r requirements.txt

# Create database and seed
createdb warbler
python seed.py

# Run server
flask run 

# Server runs on http://localhost:5000 
```