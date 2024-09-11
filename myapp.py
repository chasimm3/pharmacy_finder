import streamlit as st
import pandas as pd
from nearby_search import nearby_search

               
st.write("""
# Meet Hot Pharmacists in your Area!
#### The website putting ***YOU*** in touch with hot, available pharmacists in your area!!

""")

col1, col2 = st.columns(2)

with col1:
    postcode = st.text_input(label="Enter postcode")
    
with col2:
    search_radius = st.text_input(label="Enter Search Radius")

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
