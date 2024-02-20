import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
DEFAULT_LIMIT = 5

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts.
    rows = [dict(row) for row in rows_raw]
    return rows

def flight_status(df):
    flight_status_codes = {
    'SCH' : 'Scheduled',
    'DEL' : 'Delayed',
    'WIL' : 'Wait in Lounge',
    'GTO' : 'Gate Open',
    'BRD' : 'Boarding',
    'GCL' : 'Gate Closing',
    'GTD' : 'Gate Closed',
    'DEP' : 'Departed',
    'CNX' : 'Cancelled',
    'GCH' : 'Gate Change',
    'TOM' : 'Tomorrow',
    'AIR' : 'Airborne',
    'EXP' : 'Expected Landing',
    'FIR' : 'Flight in Dutch Airspace',
    'LND' : 'Landed',
    'FIB' : 'FIBAG',
    'ARR' : 'Arrived',
    'DIV' : 'Diverted'
 
    }
    for i in (df['Status']):
        for j in range(len(i)):
            if i[j] in flight_status_codes:
                # st.write(i[j])
                i[j] = flight_status_codes.get(i[j])
    return df

@st.cache_resource
def get_departure_df() -> pd.DataFrame:
    departure_df = pd.DataFrame.from_records(run_query(f"""SELECT a.flightname as Flight, a.publicflightstate_flightstates as Status,
                                                            a.scheduledate as Date, 
                                                            a.scheduletime as Time,  
                                                            b.airport as Origin,
                                                            b.latitude as Latitude,
                                                            b.longitude as Longitude 
                                                            FROM `stellar-cipher-409706.schipol_data.flights` a
                                                            join stellar-cipher-409706.schipol_data.airport_iata b
                                                            on b.iata = a.route_destinations[0]
                                                            where flightdirection = 'D'
                                                            order by Time
                                                            
                                                       """))
    departure_df = flight_status(departure_df)
    return departure_df

@st.cache_resource
def get_arrival_df() -> pd.DataFrame:
    arrival_df = pd.DataFrame.from_records(run_query("""SELECT a.flightname as Flight, a.publicflightstate_flightstates as Status,
                                                        a.scheduledate as Date, 
                                                        a.scheduletime as Time,  
                                                        b.airport as Origin,
                                                        b.latitude as Latitude,
                                                        b.longitude as Longitude                                                         
                                                        FROM `stellar-cipher-409706.schipol_data.flights` a
                                                        join stellar-cipher-409706.schipol_data.airport_iata b
                                                        on b.iata = a.route_destinations[0]
                                                        where flightdirection = 'A'
                                                        order by Time
                                                        
                            """
                        ))
    arrival_df = flight_status(arrival_df)
    return arrival_df

@st.cache_resource
def busiest_airlines(limit=DEFAULT_LIMIT):
    airlines_codes_df = pd.DataFrame.from_records(run_query(f"""select b.logo as Logo, b.name as Carrier, count(a.id) as Count
                                                                from stellar-cipher-409706.schipol_data.airlines b
                                                                join stellar-cipher-409706.schipol_data.flights a
                                                                on b.code = substring(UPPER(a.flightname),1,2)
                                                                group by b.name,b.logo
                                                                order by count(a.id) desc
                                                                limit {limit};
                                                            """))
    return airlines_codes_df

@st.cache_resource
def flight_categories(limit=DEFAULT_LIMIT):
    service_df = pd.DataFrame.from_records(run_query(f"""SELECT servicetype as Type, count(flightname) as Count
                           from stellar-cipher-409706.schipol_data.flights
                           group by servicetype
                           order by Count desc
                           limit {limit};"""))
    
    
    codes = {
            'J'   : 'Passenger Airlines',
            'F'   : 'Freight Airlines' ,
            'C'   : 'Passenger Charter', 
            'H'   : 'Freight Charter' ,
            'P'   : 'Non Revenue'
        }
    
    for i in range(len(service_df['Type'])):
        if service_df['Type'].iloc[i] in codes:
            service_df['Type'].iloc[i] = codes.get(service_df['Type'].iloc[i])
    
    
    return service_df

@st.cache_resource
def popular_routes(limit=DEFAULT_LIMIT):
    popular_routes_df = pd.DataFrame.from_records(run_query(f"""select airports.airport as Destinations, count(flights.id) as Count, airports.latitude as Latitude, airports.longitude as Longitude
                                                            from stellar-cipher-409706.schipol_data.airport_iata airports
                                                            join stellar-cipher-409706.schipol_data.flights flights
                                                            on airports.iata = flights.route_destinations[offset(0)]
                                                            group by Destinations, airports.latitude, airports.longitude
                                                            order by Count desc 
                                                            limit {limit};
                                                            """))
   
    return popular_routes_df

@st.cache_resource
def get_count_arr():
    arr_count = run_query("""select count(mainflight) as arr_count
                            from stellar-cipher-409706.schipol_data.flights
                            where flightdirection = 'A'""")
    return arr_count.pop()['arr_count']

@st.cache_resource
def get_count_dept():
    dept_count = run_query("""select count(mainflight) as dept_count
                            from stellar-cipher-409706.schipol_data.flights
                            where flightdirection = 'D'""")
    return dept_count.pop()['dept_count']

@st.cache_resource
def top_arriving_airlines(limit=DEFAULT_LIMIT):
    top_arriving_airlines_df = pd.DataFrame.from_records(run_query(f"""select airlines.logo as Logo, airlines.name as Airlines, count(flights.id) as Count
                                                                        from stellar-cipher-409706.schipol_data.flights flights
                                                                        join stellar-cipher-409706.schipol_data.airlines airlines
                                                                        on airlines.code = substring(flights.flightname,1,2)

                                                                        where flightdirection = 'A'
                                                                        group by Airlines, Logo
                                                                        order by Count desc
                                                                        limit {limit};
                                                                        """))
    return top_arriving_airlines_df

@st.cache_resource
def top_departing_airlines(limit=DEFAULT_LIMIT):
   top_departing_airlines_df = pd.DataFrame.from_records(run_query(f"""select airlines.logo as Logo, airlines.name as Airlines, count(flights.id) as Count
                                                                        from stellar-cipher-409706.schipol_data.flights flights
                                                                        join stellar-cipher-409706.schipol_data.airlines airlines
                                                                        on airlines.code = substring(flights.flightname,1,2)

                                                                        where flightdirection = 'D'
                                                                        group by Airlines, Logo
                                                                        order by Count desc
                                                                        limit {limit};
                                                                        """))
   return top_departing_airlines_df

def get_aircrafts(limit=DEFAULT_LIMIT):
    common_aircrafts = pd.DataFrame.from_records(run_query(f"""select aircrafts.name as Aircraft, count(flights.id) as Count
                                                                from stellar-cipher-409706.schipol_data.aircrafts aircrafts
                                                                join stellar-cipher-409706.schipol_data.flights flights
                                                                on aircrafts.iata_code = flights.aircrafttype_iatasub
                                                                group by Aircraft
                                                                order by Count desc
                                                                limit {limit};
                                                            """))
    return common_aircrafts
    
    
    
    
    
def my_links():
    github_logo = "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png"
    github_link = "https://github.com/suleman1412"
    image_size = 60
    linkedin_logo = "https://png2.cleanpng.com/sh/adbbe142ae9bdf273c4d7f1744c321ef/L0KzQYm3VcE5N6FBipH0aYP2gLBuTfNwdaF6jNd7LXnmf7B6TfxqdpxqfNt3LUXkdre3Usg0bWY5Uag9LkG6QIW5Usc5OWY3TqgBMUe5Q4q6WcIveJ9s/kisspng-computer-icons-linkedin-5aff0283e54964.1704227815266617639392.png"
    linkedin_url = "https://www.linkedin.com/in/sulemankarigar/"
    return st.markdown(f'<a href="{github_link}"><img src="{github_logo}" alt="Github" width="{image_size}px"> <a href="{linkedin_url}"><img src="{linkedin_logo}" alt="LinkedIn" width="{image_size}px">', unsafe_allow_html=True)
