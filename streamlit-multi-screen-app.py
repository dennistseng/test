import streamlit as st
import os
import time

def main():
    # Set page configuration
    st.set_page_config(page_title="Multi-Screen File Processor", layout="wide")
    
    # Initialize session state variables if they don't exist
    if 'screen' not in st.session_state:
        st.session_state.screen = 'file_selection'
    if 'selected_files' not in st.session_state:
        st.session_state.selected_files = []
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    
    # Navigation function
    def navigate_to(screen):
        st.session_state.screen = screen
    
    # Display the current screen
    if st.session_state.screen == 'file_selection':
        file_selection_screen()
    elif st.session_state.screen == 'results':
        results_screen()

def file_selection_screen():
    st.title("File Selection")
    
    # Get files from the directory
    # In a real app, you'd specify your directory path
    directory_path = "."  # Current directory for example purposes
    available_files = get_files_in_directory(directory_path)
    
    st.write("Select two files for processing:")
    
    # Create multiselect for file selection
    selected_files = st.multiselect(
        "Available Files",
        options=available_files,
        default=st.session_state.selected_files
    )
    
    # Update session state
    st.session_state.selected_files = selected_files
    
    # Process button
    if st.button("Process Files", disabled=len(selected_files) != 2):
        if len(selected_files) == 2:
            with st.spinner("Processing files..."):
                # Simulate processing time
                process_files(selected_files)
                st.session_state.processing_complete = True
                st.session_state.screen = 'results'
                st.experimental_rerun()
        else:
            st.error("Please select exactly two files.")
    
    # Display selection information
    if selected_files:
        st.write(f"You have selected {len(selected_files)} file(s):")
        for file in selected_files:
            st.write(f"- {file}")
        
        if len(selected_files) != 2:
            st.info("Please select exactly 2 files to enable processing.")

def results_screen():
    st.title("Results")
    
    if not st.session_state.processing_complete:
        st.warning("No processed data available. Please select and process files first.")
        if st.button("Go back to file selection"):
            st.session_state.screen = 'file_selection'
            st.experimental_rerun()
        return
    
    st.success("Files processed successfully!")
    st.write(f"Processed files: {', '.join(st.session_state.selected_files)}")
    
    # Display dummy results
    st.header("Processing Results")
    st.write("Here are your processing results:")
    
    # Create some dummy data visualization
    import pandas as pd
    import numpy as np
    
    # Create dummy data based on filenames
    data = {
        "Values": np.random.randn(20),
        "Categories": [f"Category {i}" for i in range(1, 21)]
    }
    df = pd.DataFrame(data)
    
    st.dataframe(df)
    st.bar_chart(df.set_index("Categories"))
    
    # Button to go back to file selection
    if st.button("Process different files"):
        st.session_state.selected_files = []
        st.session_state.processing_complete = False
        st.session_state.screen = 'file_selection'
        st.experimental_rerun()

def get_files_in_directory(directory_path):
    """Get list of files in the specified directory."""
    try:
        # List files in the directory
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        return files
    except Exception as e:
        st.error(f"Error accessing directory: {e}")
        return []

def process_files(files):
    """Dummy function to process the selected files."""
    # In a real application, this is where you would process your files
    # For demonstration, we'll just simulate processing time
    time.sleep(2)
    return True

if __name__ == "__main__":
    main()
