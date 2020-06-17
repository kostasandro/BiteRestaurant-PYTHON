import sqlite3
con = sqlite3.connect("restaurant.db")
print("Database opened successfully")

con.execute("create table customer (Customer_ID INTEGER PRIMARY KEY AUTOINCREMENT, First_name varchar(20) NOT NULL, Last_name varchar(20) NOT NULL,Gender varchar(10) DEFAULT NULL)")  

con.execute("create table employee (Employee_ID INTEGER PRIMARY KEY AUTOINCREMENT, First_name varchar(20) NOT NULL, Last_name varchar(20) NOT NULL, Address varchar(50) NOT NULL, Phone_number INTEGER NOT NULL)")  
 
con.execute("create table open_date (id INTEGER PRIMARY KEY AUTOINCREMENT, date_from date NOT NULL, date_to date NOT NULL)")  

con.execute("create table open_dates_hours (id INTEGER PRIMARY KEY AUTOINCREMENT, open_date_id INTEGER NOT NULL, work_hours_id INTEGER NOT NULL)")  

con.execute("create table work_hours (id INTEGER PRIMARY KEY AUTOINCREMENT, hour_from datetime NOT NULL, hour_to datetime  NOT NULL)") 

con.execute("create table reservation_table (ID INTEGER PRIMARY KEY AUTOINCREMENT, Table_ID INTEGER NOT NULL, Reservation_ID INTEGER NOT NULL)")  

con.execute("create table res_table (Table_ID INTEGER PRIMARY KEY AUTOINCREMENT, Capacity INTEGER NOT NULL)")  

con.execute("create table review (ID INTEGER PRIMARY KEY AUTOINCREMENT, Customer_ID INTEGER NOT NULL, Comment varchar(255) NOT NULL, Date date NOT NULL)")  

con.execute("create table users (User_ID INTEGER PRIMARY KEY AUTOINCREMENT, Role varchar(10) NOT NULL, Email varchar(20) UNIQUE NOT NULL, Password varchar(50) NOT NULL, Employee_ID INTEGER DEFAULT NULL,  Customer_ID INTEGER DEFAULT NULL, FOREIGN KEY (Employee_ID) REFERENCES employee(Employee_ID), FOREIGN KEY (Customer_ID) REFERENCES customer(Customer_ID))")  

con.execute("create table reservation (Reservation_ID INTEGER PRIMARY KEY AUTOINCREMENT, Date date NOT NULL, Persons INTEGER NOT NULL, Start_time varchar(10) NOT NULL, Customer_ID INTEGER NOT NULL,Employee_ID INTEGER DEFAULT NULL, Status INTEGER NOT NULL, FOREIGN KEY (Customer_ID) REFERENCES customer(Customer_ID),FOREIGN KEY (Employee_ID) REFERENCES employee(Employee_ID))") 
 
print("Table created successfully")
con.close()