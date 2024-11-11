import streamlit as st
import pandas as pd
import hashlib

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sample data
books_data = [
    {"ID": 1, "Title": "The Great Gatsby", "Author": "F. Scott Fitzgerald", "Available": 5},
    {"ID": 2, "Title": "1984", "Author": "George Orwell", "Available": 3},
    {"ID": 3, "Title": "To Kill a Mockingbird", "Author": "Harper Lee", "Available": 4}
]

students_data = [
    {"ID": 1, "Name": "John Doe", "BooksIssued": 0, "Fine": 0},
    {"ID": 2, "Name": "Jane Smith", "BooksIssued": 1, "Fine": 5}
]

librarians_data = [
    {"ID": 1, "Name": "Libby Librarian", "Username": "librarian1", "Password": hash_password("librarianpass")}
]

# Convert to DataFrame
books_df = pd.DataFrame(books_data)
students_df = pd.DataFrame(students_data)
librarians_df = pd.DataFrame(librarians_data)

# Admin and librarian credentials
admin_credentials = {"admin": hash_password("adminpass")}
user_type = ""

# Streamlit app
st.title("Library Management System")

# Login interface
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
hashed_password = hash_password(password)

# Authentication
if username == "admin" and admin_credentials["admin"] == hashed_password:
    user_type = "Admin"
    st.sidebar.success("Logged in as Admin")
elif username in librarians_df["Username"].values and any(librarians_df[librarians_df["Username"] == username]["Password"] == hashed_password):
    user_type = "Librarian"
    st.sidebar.success("Logged in as Librarian")
else:
    st.sidebar.error("Invalid Username or Password")

# Admin interface
if user_type == "Admin":
    st.header("Admin Dashboard")
    st.subheader("Manage Librarians")
    
    action = st.selectbox("Choose Action", ["Add Librarian", "Edit Librarian", "Delete Librarian", "Clear Form"])
    
    if action == "Add Librarian":
        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Add Librarian"):
            new_id = librarians_df["ID"].max() + 1
            librarians_df.loc[len(librarians_df)] = [new_id, name, username, hash_password(password)]
            st.success("Librarian added successfully")
    
    elif action == "Edit Librarian":
        librarian_id = st.number_input("Enter Librarian ID to Edit", min_value=1)
        if librarian_id in librarians_df["ID"].values:
            name = st.text_input("New Name", librarians_df.loc[librarians_df["ID"] == librarian_id, "Name"].values[0])
            username = st.text_input("New Username", librarians_df.loc[librarians_df["ID"] == librarian_id, "Username"].values[0])
            if st.button("Update Librarian"):
                librarians_df.loc[librarians_df["ID"] == librarian_id, ["Name", "Username"]] = [name, username]
                st.success("Librarian details updated successfully")
        else:
            st.error("Librarian ID not found")
    
    elif action == "Delete Librarian":
        librarian_id = st.number_input("Enter Librarian ID to Delete", min_value=1)
        if st.button("Delete Librarian"):
            librarians_df = librarians_df[librarians_df["ID"] != librarian_id]
            st.success("Librarian deleted successfully")
    
    elif action == "Clear Form":
        st.info("Form cleared")

# Librarian interface
elif user_type == "Librarian":
    st.header("Librarian Dashboard")
    
    option = st.selectbox("Select an action", ["Manage Books", "Manage Students", "View Inventory", "Issue Books", "View Students with Fine"])
    
    if option == "Manage Books":
        st.subheader("Book Management")
        book_action = st.selectbox("Choose Action", ["Add Book", "Edit Book", "Delete Book", "Clear Form"])
        
        if book_action == "Add Book":
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            available = st.number_input("Available Copies", min_value=1)
            if st.button("Add Book"):
                new_id = books_df["ID"].max() + 1
                books_df.loc[len(books_df)] = [new_id, title, author, available]
                st.success("Book added successfully")
        
        elif book_action == "Edit Book":
            book_id = st.number_input("Enter Book ID to Edit", min_value=1)
            if book_id in books_df["ID"].values:
                title = st.text_input("New Title", books_df.loc[books_df["ID"] == book_id, "Title"].values[0])
                author = st.text_input("New Author", books_df.loc[books_df["ID"] == book_id, "Author"].values[0])
                available = st.number_input("New Available Copies", books_df.loc[books_df["ID"] == book_id, "Available"].values[0], min_value=0)
                if st.button("Update Book"):
                    books_df.loc[books_df["ID"] == book_id, ["Title", "Author", "Available"]] = [title, author, available]
                    st.success("Book details updated successfully")
            else:
                st.error("Book ID not found")
        
        elif book_action == "Delete Book":
            book_id = st.number_input("Enter Book ID to Delete", min_value=1)
            if st.button("Delete Book"):
                books_df = books_df[books_df["ID"] != book_id]
                st.success("Book deleted successfully")
        
        elif book_action == "Clear Form":
            st.info("Form cleared")

    elif option == "Manage Students":
        st.subheader("Student Management")
        student_action = st.selectbox("Choose Action", ["Add Student", "Edit Student", "Delete Student", "Clear Form"])
        
        if student_action == "Add Student":
            name = st.text_input("Student Name")
            if st.button("Add Student"):
                new_id = students_df["ID"].max() + 1
                students_df.loc[len(students_df)] = [new_id, name, 0, 0]
                st.success("Student added successfully")
        
        elif student_action == "Edit Student":
            student_id = st.number_input("Enter Student ID to Edit", min_value=1)
            if student_id in students_df["ID"].values:
                name = st.text_input("New Name", students_df.loc[students_df["ID"] == student_id, "Name"].values[0])
                if st.button("Update Student"):
                    students_df.loc[students_df["ID"] == student_id, "Name"] = name
                    st.success("Student details updated successfully")
            else:
                st.error("Student ID not found")
        
        elif student_action == "Delete Student":
            student_id = st.number_input("Enter Student ID to Delete", min_value=1)
            if st.button("Delete Student"):
                students_df = students_df[students_df["ID"] != student_id]
                st.success("Student deleted successfully")
        
        elif student_action == "Clear Form":
            st.info("Form cleared")
    
    elif option == "View Inventory":
        st.subheader("Inventory")
        st.write(books_df)
    
    elif option == "Issue Books":
        st.subheader("Issue Book")
        student_id = st.number_input("Enter Student ID", min_value=1)
        book_id = st.number_input("Enter Book ID", min_value=1)
        if st.button("Issue Book"):
            if student_id in students_df["ID"].values and book_id in books_df["ID"].values:
                book = books_df.loc[books_df["ID"] == book_id]
                student = students_df.loc[students_df["ID"] == student_id]
                
                if book["Available"].values[0] > 0:
                    books_df.loc[books_df["ID"] == book_id, "Available"] -= 1
                    students_df.loc[students_df["ID"] == student_id, "BooksIssued"] += 1
                    st.success("Book issued successfully")
                else:
                    st.error("Book not available")
            else:
                st.error("Invalid Student ID or Book ID")
    
    elif option == "View Students with Fine":
        st.subheader("Students with Fine")
        students_with_fine = students_df[students_df["Fine"] > 0]
        st.write(students_with_fine)

# Instructions
st.sidebar.header("Instructions")
st.sidebar.write("**Admin**: Username: admin, Password: adminpass")
st.sidebar.write("**Librarian**: Username: librarian1, Password: librarianpass")
