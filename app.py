# app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Excel to MySQL ETL", layout="wide")

st.title("📊 Excel to MySQL ETL Automation")

# Step 1: Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Step 2: Read Excel into DataFrame
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("Preview of Excel Data")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
    
    # Step 3: Get MySQL details
    st.subheader("Database Connection")
    host = st.text_input("Host", value="localhost")
    user = st.text_input("User", value="root")
    password = st.text_input("Password", type="password")
    database = st.text_input("Database")
    table_name = st.text_input("Table Name", value="uploaded_data")

    if st.button("Upload to MySQL"):
        try:
            # Create connection
            engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
            
            # Load data into MySQL
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            st.success(f"✅ Data successfully uploaded to `{table_name}` table in `{database}` database!")
        except Exception as e:
            st.error(f"❌ Failed to upload data: {e}")
