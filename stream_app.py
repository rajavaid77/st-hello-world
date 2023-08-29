import streamlit as st

st.title('File Uploader')

# Display a file uploader widget
uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "xlsx"])

if uploaded_file is not None:
    # You can process the uploaded file here
    st.write("You selected the following file:")
    st.write(uploaded_file.name)
    
    # For example, you can read and display the contents of the file
    file_contents = uploaded_file.read()
    st.write("File Contents:")
    st.write(file_contents)
