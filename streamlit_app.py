import streamlit as st
import requests
import json
import pandas as pd

# Optional: Try importing matplotlib for charts. If not available, show a warning.
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    st.warning("Matplotlib is not installed. Charts will not be displayed.")

# Function to upload file and send it to AWS Lambda or your backend service
def process_excel_file(file):
    # Replace with your actual AWS Lambda or other backend service URL
    url = "http://54.145.184.214:5000/predict"  

    # Prepare the file for the request
    files_to_upload = {
        'file': (file.name, file.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    }

    # Make the POST request to your backend service
    response = requests.post(url, files=files_to_upload)

    # Check for a successful response
    if response.status_code == 200:
        try:
            # Try to parse the JSON response
            result = response.json()
            
            # Check if the 'result' key is in the response
            if 'result' in result:
                return result['result']
            else:
                st.error("The 'result' key was not found in the response.")
                st.write("Response JSON:", result)  # Display the full JSON response for debugging
                return None
        except json.JSONDecodeError:
            st.error("Failed to decode JSON response.")
            st.write("Response content:", response.content)  # Display the raw response content
            return None
    else:
        st.error(f"Error: {response.status_code}")
        st.write("Response content:", response.content)  # Show the full response content in case of an error
        return None

# Streamlit UI
# Add image to the top left corner (make sure to replace 'your_logo.png' with your actual image path)
st.image("your_logo.png", width=100)

# Title
st.title("Predictive Analysis")

st.write("Upload an Excel file to process and analyze the data.")

# Upload file section
uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx', 'csv'])

# Ensure a file is uploaded
if uploaded_file:
    if st.button("Process File"):
        # Process file and display results
        result = process_excel_file(uploaded_file)
        
        if result:
            st.write("Processing completed! Here are the results:")
            
            # Assuming the result contains a dataset that can be converted to a DataFrame
            if isinstance(result, list) and isinstance(result[0], dict):
                # Convert result to DataFrame
                df = pd.DataFrame(result)
                
                # Display the DataFrame
                st.write("### Data Table")
                st.dataframe(df)
                
                # Plot a chart if matplotlib is available and the required columns exist
                if plt is not None:
                    if 'value' in df.columns and 'category' in df.columns:  # Replace with your column names
                        st.write("### Data Chart")
                        fig, ax = plt.subplots()
                        df.groupby('category')['value'].sum().plot(kind='bar', ax=ax)
                        st.pyplot(fig)
                    else:
                        st.write("No chart generated, as required columns are missing.")
                else:
                    st.warning("Matplotlib is not available. Charts will not be displayed.")
                    
            else:
                st.write(result)  # Show raw result if it's not a tabular format
else:
    st.warning("Please upload an Excel file.")

