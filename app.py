import streamlit as st
import pandas as pd
import openpyxl  # optional
import json
from io import BytesIO

st.set_page_config(page_title="JSON to Excel Converter", layout="centered")
st.title("🧰 JSON to Excel Converter for Power BI")

uploaded_file = st.file_uploader("Upload a JSON file", type="json")

def flatten_json_to_df(data):
    rows = []
    for category, actions in data.get("data", {}).items():
        if isinstance(actions, dict):
            for action, surfaces in actions.items():
                if isinstance(surfaces, dict):
                    for surface, value in surfaces.items():
                        rows.append({
                            "Category": category,
                            "Action": action,
                            "Surface": surface,
                            "Value": value
                        })
                else:
                    rows.append({
                        "Category": category,
                        "Action": None,
                        "Surface": action,
                        "Value": surfaces
                    })
        else:
            rows.append({
                "Category": category,
                "Action": None,
                "Surface": None,
                "Value": actions
            })
    return pd.DataFrame(rows)

if uploaded_file:
    try:
        json_data = json.load(uploaded_file)
        df = flatten_json_to_df(json_data)
        st.dataframe(df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Formatted Data')
        st.download_button("📥 Download Excel File", output.getvalue(), file_name="formatted_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Error processing file: {e}")
