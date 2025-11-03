import streamlit as st
import pandas as pd 
import os 


FILE_PATH="books.csv"

# load csv file/create 
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        df=pd.DataFrame(columns=["Books","Title","Author","Status"])
        df.to_csv(FILE_PATH,index=False)

# Save data 
def save_data(df):
    df.to_csv(FILE_PATH,index=False)

st.title("Library Management System")

# Session data 
if "books" not in st.session_state: 
    st.session_state.books=load_data()

menu = st.sidebar.selectbox("Select option ",["view books","Add book","Issue book","Return book"])

# View 
if menu == "View books":
    st.header("Books List")
    st.dataframe(st.session_state.books)


# Add book 
elif menu == "Add book":
    st.header("Add book ")
    title=st.text_input("Book Title")
    author=st.text_input("Author Name")

    if st.button("Add"):
        if title and author:
            new_id=len(st.session_state.books)+1
            new_book=pd.DataFrame({
            "Book ID":[new_id],
            "Title":[title],
            "Author":[author],
            "Status":["Available"]
        })
            st.session_state.books=pd.concat([st.session_state.books,new_book],
            ignore_index=True)
            save_data(st.session_state.books)
            st.text("Book added successfully")
    else:
        st.text("Enter both entry")

# Issue
elif menu =="Issue book":
    st.header("Issue book")
    available=st.session_state.book[st.session_state.books["Status"]=="Available"]

    if available.empty:
        st.text("No Books available to issue")
    else:
        book_id=st.selectbox("Select Book ID",available["Book ID"])
        if st.button("Issue"):
            st.session_state.books.loc[st.session_state.books["Book ID"]==book_id,
            "Status"]="Issued"
            save_data(st.session_state.books)
            st.text("Book issued successfully")

# return 
elif menu =="Return Book":
    st.header("Return Book")
    issued=st.session_state.books[st.session_state.books["Status"]=="Issued"]
    if issued.empty:
        st.text("No issued books to return")
    else:
        book_id=st.selectbox("Select Book ID",issued["Book ID"])
        if st.button("Return"):
            st.session_state.books.loc[st.session_state.books["Book ID"]==book_id,
            "Status"]="Available"
            save_data(st.session_state.books)
            st.text("Book return successfully")