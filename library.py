#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import hashlib
import datetime

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize data
books_data = [
    {"ID": 1, "Title": "The Great Gatsby", "Author": "F. Scott Fitzgerald", "Available": 5},
    {"ID": 2, "Title": "1984", "Author": "George Orwell", "Available": 3},
    {"ID": 3, "Title": "To Kill a Mockingbird", "Author": "Harper Lee", "Available": 4},
    {"ID": 4, "Title": "Moby Dick", "Author": "Herman Melville", "Available": 2}
]

students_data = [
    {"ID": 1, "Name": "John Doe", "BooksIssued": 0},
    {"ID": 2, "Name": "Jane Smith", "BooksIssued": 1}
]

# Convert to DataFrame
books_df = pd.DataFrame(books_data)
students_df = pd.DataFrame(students_data)

# User management
admin_credentials = {"admin": hash_password("password123")}
user_type = ""

# Streamlit app
st.title("Library Management System")

# Login interface
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
hashed_password = hash_password(password)

# Authentication
if username in admin_credentials and admin_credentials[username] == hashed_password:
    user_type = "Admin"
    st.sidebar.success("Logged in as Admin")
elif username in students_df["Name"].values and hashed_password == hash_password("student123"):
    user_type = "Student"
    st.sidebar.success(f"Logged in as {username}")
else:
    st.sidebar.error("Invalid Username or Password")

# Admin interface
if user_type == "Admin":
    st.header("Admin Dashboard")
    
    option = st.selectbox("Select an action", ["Manage Books", "Manage Students", "View Inventory"])
    
    if option == "Manage Books":
        st.subheader("Book Management")
        action = st.selectbox("Choose Action", ["Add Book", "Remove Book"])
        
        if action == "Add Book":
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            available = st.number_input("Available Copies", min_value=1)
            if st.button("Add Book"):
                new_id = books_df["ID"].max() + 1
                books_df.loc[len(books_df)] = [new_id, title, author, available]
                st.success("Book added successfully")
        elif action == "Remove Book":
            book_id = st.number_input("Enter Book ID to Remove", min_value=1)
            if st.button("Remove Book"):
                books_df = books_df[books_df["ID"] != book_id]
                st.success("Book removed successfully")
    
    elif option == "Manage Students":
        st.subheader("Student Management")
        st.write(students_df)
    
    elif option == "View Inventory":
        st.subheader("Inventory Management")
        st.write(books_df)

# Student interface
elif user_type == "Student":
    st.header(f"Welcome {username}")
    option = st.selectbox("Select an action", ["Issue Book", "Return Book"])
    
    if option == "Issue Book":
        book_id = st.number_input("Enter Book ID to Issue", min_value=1)
        if st.button("Issue Book"):
            if book_id in books_df["ID"].values:
                book = books_df[books_df["ID"] == book_id]
                if book["Available"].values[0] > 0:
                    books_df.loc[books_df["ID"] == book_id, "Available"] -= 1
                    students_df.loc[students_df["Name"] == username, "BooksIssued"] += 1
                    st.success("Book issued successfully")
                else:
                    st.error("Book not available")
            else:
                st.error("Invalid Book ID")
    
    elif option == "Return Book":
        book_id = st.number_input("Enter Book ID to Return", min_value=1)
        days_late = st.number_input("Days Late", min_value=0)
        if st.button("Return Book"):
            if book_id in books_df["ID"].values:
                books_df.loc[books_df["ID"] == book_id, "Available"] += 1
                students_df.loc[students_df["Name"] == username, "BooksIssued"] -= 1
                fine = days_late * 5
                st.success(f"Book returned successfully. Fine: ${fine}")
            else:
                st.error("Invalid Book ID")


# In[2]:




