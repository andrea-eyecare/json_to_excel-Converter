import streamlit as st
import pandas as pd
import json

# Function to process JSON and convert to Excel
def process_json_to_excel(json_data):
    """
    Convert JSON data into structured Excel format.
    """
    
    # Define the sections to process
    data_sections = ["oneYearRoadExpenses", "roadMiles", "eightYearBridgeAverage",
                     "eightYearRoadAverage", "longTermRoads", "longTermBridges",
                     "oneYearBridgeExpenses", "bridgeAreas"]

    # Dictionary to store DataFrames
    excel_data = {}

    for section in data_sections:
        if section in json_data['data']:
            section_data = json_data['data'][section]
            
            # Convert dictionary to DataFrame
            if isinstance(section_data, dict):
                df = pd.DataFrame.from_dict(section_data, orient='index').reset_index()
                df.rename(columns={'index': 'Category'}, inplace=True)
            else:
                df = pd.DataFrame([section_data])
            
            excel_data[section] = df

    # Process multipliers separately
    multipliers_df = pd.DataFrame(list(json_data['multipliers'].items()), columns=['Multiplier Type', 'Value'])
    excel_data['Multipliers'] = multipliers_df

    return excel_data

# Streamlit UI
st.title("📂 JSON to Excel Converter")

st.markdown("### Upload your JSON file below:")

uploaded_file = st.file_uploader("Upload JSON File", type="json")

if uploaded_file is not None:
    # Load JSON data
    json_data = json.load(uploaded_file)

    # Process JSON into DataFrames
    dataframes = process_json_to_excel(json_data)

    # Save to Excel
    excel_filename = "Converted_Data.xlsx"
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Provide download button
    with open(excel_filename, "rb") as f:
        st.download_button("📥 Download Excel File", f, file_name=excel_filename)
    
    st.success("✅ Excel file is ready! Click above to download.")

