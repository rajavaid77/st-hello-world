import streamlit as st
import boto3
import json


def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']
    return json.loads(secret_string)

def upload_to_s3(file, bucket_name, secret_data):
    s3 = boto3.client(
        's3',
        aws_access_key_id=secret_data['access_key'],
        aws_secret_access_key=secret_data['secret_key'],
        region_name=secret_data['region_name']  # Replace with your AWS region
    )

    try:
        s3.upload_fileobj(file, bucket_name, file.name)
        st.success(f"File '{file.name}' uploaded to '{bucket_name}'")
    except Exception as e:
        st.error(f"Error uploading file '{file.name}': {e}")

# Function to clear the form and results
# def clear_form():
#     st.session_state.state['S3_BUCKET_NAME'] = ""
#     st.session_state.state['uploaded_files'] = []
#     st.session_state.state['uploaded_file_names'] = []

# # Clear Form button
# if st.button("Clear Form"):
#     clear_form()

# Streamlit app
st.title("File Upload to S3")

uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True)
bucket_name = st.text_input("Enter S3 Bucket Name")

st.write("Preview of Uploaded Files:")
if uploaded_files:
    for file in uploaded_files:
        if file:
            file_contents = file.read()
            st.write(f"File: {file.name}")
            st.code(file_contents, language='text')  # Display contents of the file
            st.write("-" * 50)

if st.button("Upload Files"):
    if uploaded_files and bucket_name:
        secret_name = "StreamlitPOC"  # Replace with your actual secret name
        secret_data = get_secret(secret_name)
        
        for file in uploaded_files:
            upload_to_s3(file, bucket_name, secret_data)

# Clear Button to Reset the Form
if st.button("Clear Form"):
    bucket_name = ""
    secret_name = ""
    uploaded_files = []
    st.session_state.uploaded_results = []  # Clear the uploaded_results in session state
          
