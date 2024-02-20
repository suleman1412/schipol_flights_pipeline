import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import datetime
import pandas as pd
from components.top_airlines_section import TopAirlinesSection
from components.top_aircrafts_section import TopAircraftsSection    
from components.connections import (
    get_departure_df,
    get_arrival_df,
    flight_categories,
    busiest_airlines,
    popular_routes,
    top_arriving_airlines,
    top_departing_airlines,
    get_aircrafts,
    my_links
)

st.set_page_config(page_title="Schipol Airport Stats", layout="wide")
with st.container():
		st.markdown(
			'<img height="350" width="500" src="https://cdn.worldvectorlogo.com/logos/schiphol.svg"/>',
			unsafe_allow_html=True
		)
  
formatted_date = datetime.now().strftime('%d %b, %Y')
st.subheader(f"Today's date: {formatted_date}")
st.title('Airport Statistics')

tab1, tab2, tab3= st.tabs(["Overview","Arrivals", "Departures"])

# Overview Tab
with tab1:
    
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.subheader("Busiest Airlines")
        st.dataframe(busiest_airlines(),
                    column_config={
                        "Logo": st.column_config.ImageColumn("Icon")
                    },hide_index=True,width=400)    
        
    with col2:
        st.subheader("Flight Categories")
        st.dataframe(flight_categories(),hide_index=True,width=400)
        
    with col3:
        st.subheader("Popular Routes")
        popular_routes_df = popular_routes()
        st.dataframe(popular_routes_df,hide_index=True,width=400,column_order=['Destinations','Count'])
         
    with col4:
        st.subheader("Frequent Aircrafts")
        st.dataframe(get_aircrafts(),hide_index=True,width=400)
    
    
    
    st.subheader("Location of the Airports")
    st.map(popular_routes_df, latitude='Latitude', longitude='Longitude', zoom= 3.5, size=[x**2 for x in popular_routes_df['Count']], color='#D22B2B')

# Arrivals
with tab2:
    
    top_arr_airlines_section = TopAirlinesSection(top_arriving_airlines())
    with st.container():
        st.subheader("Top 5 Arriving Airlines")
        top_arr_airlines_section.display()
        st.divider()
        st.subheader("Location of Origin Airports")
        st.map(get_arrival_df(), latitude='Latitude', longitude='Longitude', zoom=1)
        st.divider()
        st.subheader("All Arriving Flights")
        st.dataframe(get_arrival_df(),hide_index=True,use_container_width=True,column_order=['Flight', 'Status', 'Time', 'Origin'])
        # with st.expander("Read more"):
        #     st.subheader("Bar Chart")
        #     st.bar_chart(get_arrival_df().groupby('Origin')['Origin'].value_counts().sort_values(ascending=False))

# Departures     
with tab3:
    
    top_dept_airlines_section = TopAirlinesSection(top_departing_airlines())
    with st.container():
        st.subheader("Top 5 Departing Airlines")
        top_dept_airlines_section.display()
        st.divider()
        st.subheader("Location of Destination Airports")
        st.map(get_departure_df(), latitude='Latitude', longitude='Longitude', zoom=1)
        st.divider()
        st.subheader("All Departing Flights")
        st.dataframe(get_departure_df(),hide_index=True,use_container_width=True,column_order=['Flight', 'Status', 'Time', 'Origin'])


st.divider()
st.subheader("Socials")
my_links() 

# st.markdown(f'', unsafe_allow_html=True)

   










