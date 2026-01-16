import streamlit as st
import pandas as pd
from scraper import run_scraper
from io import BytesIO

st.set_page_config(page_title="Myntra Reviews Scraper", layout="centered")

st.title("🛍 Myntra Ratings & Reviews Scraper")

st.markdown("""
Upload an **Excel or CSV** file containing a column named **Myntra ID**
""")

uploaded_file = st.file_uploader(
    "Upload File",
    type=["xlsx", "csv"]
)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        if "Myntra ID" not in df.columns:
            st.error("Input file must contain 'Myntra ID' column")
            st.stop()

        st.success(f"{len(df)} products uploaded")

        if st.button("▶ Start Scraping"):
            with st.spinner("Scraping Myntra data..."):
                output_df = run_scraper(df)

            st.success("Scraping completed!")

            buffer = BytesIO()
            output_df.to_excel(buffer, index=False)
            buffer.seek(0)

            st.download_button(
                label="⬇ Download Output Excel",
                data=buffer,
                file_name="myntra_scrape_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error: {e}")
