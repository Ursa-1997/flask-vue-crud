# flask-vue-crud
Single Page App with Flask and Vue.js
forked from testdrivenio/flask-vue-crud, so you can goto the original link for documents




# Ref

## Setup:  
  Flask==1.0.2  
  Flask-Cors==3.0.7  
  npm v6.14.6  
  vue cli 3.7.0  
  pip install flask_sqlalchemy  
  pip install mysqlclient  
  
## Get Stated:  
  [Great article to start here](https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/)

  ### How to create user in MySQL and then grant access?
  ```  
  USE mysql;
  CREATE USER 'zhongche'@'%' IDENTIFIED BY 'swjt111';
  GRANT ALL ON *.* TO 'zhongche'@'%';
  FLUSH PRIVILEGES;
  ``` 
  ### how to create database in MySQL?
  ```  
  CREATE DATABASE mydb;
  FLUSH PRIVILEGES;
  ``` 
  

## Connect to DB:  
  https://blog.miguelgrinberg.com/post/restful-authentication-with-flask  
  https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database  
