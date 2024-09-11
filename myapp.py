import streamlit as st
import pandas as pd
from nearby_search import nearby_search

# set layout of pay to be wide as possible
st.set_page_config(layout="wide")
               
# intro written in markdown
st.write("""
# Meet Hot Pharmacists in your Area!
#### The website putting ***YOU*** in touch with hot, available pharmacists in your area!!

""")

# build form with 2 input boxes, one for postcode and one for search radius
with st.form("my_form"):
    col1, col2 = st.columns(2)
    with col1:
        postcode = st.text_input(label="Enter Postcode")
    with col2:
        search_radius = st.text_input(label="Enter Search Radius")
        
    submitted = st.form_submit_button("Search")
    
    # if the boxes are populated, run the nearby search for the postcode and search radius, then display the dataframe in a table
    if submitted:
        if postcode:
            if search_radius: 
                data = nearby_search(postcode, radius=search_radius, 
                            API_KEY="AIzaSyCipnwTT73UZGNvt5nGNIfHgTggEaEkKPw",
                            COUNTRY="UK")
                st.dataframe(data, hide_index=True, use_container_width=True, column_config={"Number": st.column_config.LinkColumn()})
            else:
                nearby_search(postcode, radius=0, 
                            API_KEY="AIzaSyCipnwTT73UZGNvt5nGNIfHgTggEaEkKPw",
                            COUNTRY="UK")

