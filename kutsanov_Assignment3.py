import sqlite3
import csv
#import pandas as pd
from pandas import DataFrame

conn = sqlite3.connect('./StudentDB.db') #establish a connection
cursor = conn.cursor() #allows python to execute sql statemetnts
cursor.execute("DROP TABLE Student")
cursor.execute("CREATE TABLE Student"
        "(StudentId INTEGER PRIMARY KEY,"
        "FirstName TEXT,"
        "LastName TEXT,"
        "Address TEXT,"
        "City TEXT,"
        "State TEXT,"
        "ZipCode TEXT,"
        "FacultyAdvisor TEXT,"
        "MobilePhoneNumber TEXT,"
        "Major TEXT,"
        "GPA REAL,"
        "isDeleted INTEGER)"
        )

#mycursor.execute()

#Write a python function to import the students.csv file (provided to you)
# into your newly created Students table
with open('students.csv', 'r') as file:
    #no_records = 0
    skip = next(file)
    for row in file:
        cursor.execute("INSERT INTO Student(FirstName, LastName, Address, City, State, Zipcode, MobilePhoneNumber, Major, GPA) VALUES(?,?,?,?,?,?,?,?,?)", row.split(","))
        conn.commit()
        #no_records += 1
print('\nRecords Transferred')

#Display all student attributes
conn.execute("SELECT * FROM Student")
print("Student Attributes:", cursor.fetchall())

#Add New Students. All attributes are required when creating
#a new student. Please make sure to validate user input appropriately.
#For example,a GPA can’t have a value of ‘foobar’etc.
print("1. To insert new Students, enter 'i'.")
print("2. To update a student field (Major, Advisor, Phone Number), enter 'u'.")
print("3. To delete a student record, enter 'd'.")
print("4. To search and query results, enter 's': ")
print("5. To finish with the dataset, enter 'e")
usr = input("Enter here: \n")
while usr != 'e':
    if usr == "i":
        try:
            f_name = input("Enter First Name: ")
            l_name = input("Enter Last Name: " )
            addy = input("Enter Address: ")
            city = input("Enter City: ")
            state = input("Enter State: ")
            zipcode = input("Enter ZipCode: ")
            phone = input("Enter Phone Number: ")
            major = input("Enter Major: ")
            gpa = float(input("Enter GPA: "))

            cursor = conn.cursor()
            cursor.execute("INSERT INTO Student(FirstName, LastName, Address, City, State, Zipcode, MobilePhoneNumber, Major, GPA) VALUES(?,?,?,?,?,?,?,?,?)",(f_name, l_name, addy, city, state, zipcode, phone, major, gpa))
            conn.commit()
            cursor.close()
            print("New Student Added\n")
            usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")

        except sqlite3.Error as e:
            print("Unexpected Error While Inserting\n", e)

#Update Students (Only = Major, Advisor, MobilePhoneNumber can be updated)
#Make sure that your UPDATE statement makes use of the correct keys so that you dont update every record in the database
    if usr == 'u':
        search_id = input("What is the Student ID of the student you are updating?: ")
        print("Would you like tp update the major('m'), advisor('a'), or number('n')?:")
        usr = input("Enter here('e' to exit): ")
        specific_upd = input("What would you like to change it to?: ")

        if usr == 'm':
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Student SET Major = ? WHERE StudentID = ?", (specific_upd, search_id))
                print("Update has been made\n")
                conn.commit()
                cursor.close()
                usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")
            except sqlite3.Error as e:
                print("Unexpected Error While Inserting\n", e)

        elif usr == 'a':
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentID = ?", (specific_upd, search_id))
                conn.commit()
                print("Update has been made\n")
                usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")
                cursor.close()
            except sqlite3.Error as e:
                print("Unexpected Error While Inserting\n", e)

        elif usr == 'n':
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentID = ?", (specific_upd, search_id))
                conn.commit()
                print("Update has been made\n")
                usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")
                cursor.close()
            except sqlite3.Error as e:
                print("Unexpected Error While Inserting\n", e)

#Delete Students by StudentId (Perform a “soft” delete on students that is, set isDeleted to true(1)
    if usr == 'd':
        delete_student = input("What is the ID of the Student you are deleting?: ")
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Student SET isDeleted = ? WHERE StudentID = ?", (True, delete_student))
            conn.commit()
            print("Delete has been made\n")
            usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")
            cursor.close()
        except sqlite3.Error as e:
            print("Unexpected Error While Inserting\n", e)

#Search/Display students by Major, GPA, City, State and Advisor (they should be able to search/query by these fields)
    if usr == 's':
        query = input("Which field (major, gpa, city, state and advisor) would you like to use to search the data? ").lower()
        if query == 'major':
            try:
                search_by = input("What major are you searching for?: ")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Student WHERE Major = ?", (search_by,))
                conn.commit()
                print("Your search results:\n ")
                df = DataFrame(cursor, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'Zipcode', 'MobilePhoneNumber', 'isDeleted'])
                print(df)
                usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")
                cursor.close()
            except sqlite3.Error as e:
                print("Unexpected Error While Inserting\n", e)

        elif query == 'gpa':
            try:
                search_by = input("What GPA are you searching for?: ")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Student WHERE GPA = ?", (search_by,))
                conn.commit()
                print("Your search results:\n ")
                df = DataFrame(cursor, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'Zipcode', 'MobilePhoneNumber', 'isDeleted'])
                print(df)
                usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")
                cursor.close()
            except sqlite3.Error as e:
                print("Unexpected Error While Inserting\n", e)

        elif query == 'city':
            try:
                search_by = input("What city are you searching for?: ")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Student WHERE City = ?", (search_by,))
                conn.commit()
                print("Your search results:\n ")
                df = DataFrame(cursor, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'Zipcode', 'MobilePhoneNumber', 'isDeleted'])
                print(df)
                usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")
                cursor.close()
            except sqlite3.Error as e:
                print("Unexpected Error While Inserting\n", e)

        elif query == 'state':
            try:
                search_by = input("What state are you searching for?: ")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Student WHERE State = ?", (search_by,))
                conn.commit()
                print("Your search results:\n ")
                df = DataFrame(cursor, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'Zipcode', 'MobilePhoneNumber', 'isDeleted'])
                print(df)
                usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")
                cursor.close()
            except sqlite3.Error as e:
                print("Unexpected Error While Inserting\n", e)

        elif query == 'advisor':
            try:
                search_by = input("What advisor are you searching for?: ")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Student WHERE Advisor = ?", (search_by,))
                conn.commit()
                print("Your search results:\n ")
                df = DataFrame(cursor, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'Zipcode', 'MobilePhoneNumber', 'isDeleted'])
                print(df)
                usr = input("Would you like to keep manipulating the database?: ('i', 'u', 'd', 's', 'e'): ")
                cursor.close()
            except sqlite3.Error as e:
                print("Unexpected Error While Inserting\n", e)

conn.close()