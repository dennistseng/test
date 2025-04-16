import streamlit as st
import pandas as pd
import numpy as np

# Set page title
st.set_page_config(page_title="DataFrame Comparison Tool")

# Function to generate sample data (for demonstration purposes)
def generate_sample_data():
    # Create sample data for df1
    data1 = {
        'ID': list(range(1, 101)),
        'Text': [f"Sample text {i}" for i in range(1, 101)],
        'Numerical': np.random.randint(0, 100, 100),
        'Category1': np.random.choice(['A', 'B', 'C', 'D'], 100),
        'Category2': np.random.choice(['Low', 'Medium', 'High'], 100),
        'Category3': np.random.choice(['Red', 'Blue', 'Green', 'Yellow'], 100)
    }
    
    # Create sample data for df2 (with same IDs but different values)
    data2 = {
        'ID': list(range(1, 101)),
        'Text': [f"Other text {i}" for i in range(1, 101)],
        'Numerical': np.random.randint(0, 100, 100),
        'Category1': np.random.choice(['A', 'B', 'C', 'D'], 100),
        'Category2': np.random.choice(['Low', 'Medium', 'High'], 100),
        'Category3': np.random.choice(['Red', 'Blue', 'Green', 'Yellow'], 100)
    }
    
    return pd.DataFrame(data1), pd.DataFrame(data2)

# App title and description
st.title("DataFrame Comparison Tool")
st.write("Compare values across two DataFrames based on ID and selected column")

# File upload section
with st.expander("Upload DataFrames", expanded=True):
    st.write("Upload your two DataFrames (CSV format)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("First DataFrame")
        file1 = st.file_uploader("Upload first CSV file", type=['csv'])
        
    with col2:
        st.write("Second DataFrame")
        file2 = st.file_uploader("Upload second CSV file", type=['csv'])

# Load data
if file1 is not None and file2 is not None:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    st.success("Files uploaded successfully!")
else:
    st.write("Using sample data for demonstration. Please upload your files to use your own data.")
    df1, df2 = generate_sample_data()

# Get ID column name and all categorical columns
id_column = 'ID'  # Default ID column
if 'ID' not in df1.columns:
    id_column = df1.columns[0]  # Use first column as ID if 'ID' not found

# Get all columns except ID
all_columns = [col for col in df1.columns if col != id_column]

# Identify categorical columns
categorical_columns = []
for col in all_columns:
    if pd.api.types.is_object_dtype(df1[col]) or df1[col].nunique() < 10:
        categorical_columns.append(col)

# Sidebar for selections
st.sidebar.header("Select Options")

# ID selector
id_values = sorted(df1[id_column].unique())
selected_id = st.sidebar.selectbox("Select ID", id_values)

# Column selector
selected_column = st.sidebar.selectbox("Select Column to Compare", categorical_columns)

# Display results
st.header(f"Comparison for ID: {selected_id}")

# Filter the dataframes for the selected ID
row1 = df1[df1[id_column] == selected_id].iloc[0]
row2 = df2[df2[id_column] == selected_id].iloc[0]

# Create display columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("DataFrame 1")
    for column in df1.columns:
        st.write(f"**{column}:** {row1[column]}")
    
    # Highlight the selected column
    st.info(f"Selected column '{selected_column}' value: **{row1[selected_column]}**")

with col2:
    st.subheader("DataFrame 2")
    for column in df2.columns:
        st.write(f"**{column}:** {row2[column]}")
    
    # Highlight the selected column
    st.info(f"Selected column '{selected_column}' value: **{row2[selected_column]}**")

# Show comparison summary
st.header("Comparison Summary")

# Check if values match
if row1[selected_column] == row2[selected_column]:
    st.success(f"The values for '{selected_column}' match: {row1[selected_column]}")
else:
    st.error(f"The values for '{selected_column}' do not match: {row1[selected_column]} vs {row2[selected_column]}")

# Show a section with the full dataframes
with st.expander("View Full DataFrames"):
    st.subheader("DataFrame 1")
    st.dataframe(df1)
    
    st.subheader("DataFrame 2")
    st.dataframe(df2)
