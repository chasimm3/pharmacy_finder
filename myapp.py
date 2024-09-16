import streamlit as st
import pandas as pd
from nearby_search import nearby_search

API_KEY = "AIzaSyCipnwTT73UZGNvt5nGNIfHgTggEaEkKPw"
COUNTRY = "UK"

# set layout of pay to be wide as possible
st.set_page_config(layout="wide")
               
# intro written in markdown
st.write("""
# Pharmacies Finder!
#### Enter a postcode and a search area to identify pharmacies within the area.

""")

# build form with 2 input boxes, one for postcode and one for search radius
with st.form("my_form"):
    col1, col2 = st.columns(2)
    with col1:
        postcode = st.text_input(label="Enter Postcode")
    with col2:
        search_radius = st.text_input(label="Enter Search Radius in meters (minimum 1000)")
        
    submitted = st.form_submit_button("Search")
    
    # if the boxes are populated, run the nearby search for the postcode and search radius, then display the dataframe in a table
    if submitted:
        if postcode:
            if search_radius: 
                data = nearby_search(postcode, radius=search_radius, 
                            API_KEY=API_KEY,
                            COUNTRY=COUNTRY)
                if not data.empty:
                    # data.insert(4, "", st.button("Copy"))
                    st.dataframe(data, hide_index=True, use_container_width=True, selection_mode="single-row")#, column_config={"Number": st.column_config.LinkColumn()})
                else:
                    st.text(f"No pharmacies within {search_radius} meters of {postcode.upper()}.")
            else:
                nearby_search(postcode, radius=0, 
                            API_KEY=API_KEY,
                            COUNTRY=COUNTRY)
                
    
st.write("""
Data is collected from Google's ***Nearby Search*** API where the business type includes ***pharmacy***. 
There may be errors such as vetrinary clinics being labelled as pharmacies.

The phone numbers are populated by scraping google search results for each pharamcy in the results. 
Given this isn't an official search method or API, please reframe from abusing this tool.

If you have any issues, please raise them on [Link text Here](https://github.com/chasimm3/pharmacy_finder/issues) .
         """)

