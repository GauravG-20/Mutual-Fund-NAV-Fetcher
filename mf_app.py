import streamlit as st
from datetime import datetime
import requests
from decimal import Decimal

@st.cache_data(ttl="7d")
def getMFList():
    api_link = 'https://api.mfapi.in/mf'
    data = requests.get(api_link).json()
    mutual_funds = [e['schemeName'] for e in data]

    return mutual_funds,data

def getLink(selected_fund,data):
    link = 'https://api.mfapi.in/mf/100027'

    for e in data:
        if selected_fund == e['schemeName']:
            link = f'https://api.mfapi.in/mf/{e["schemeCode"]}'

    return link

def getData(link):

    mfData = requests.get(link).json()['data']

    for i in mfData:
        if i['date'] == selected_date.strftime('%d-%m-%Y'):
            return 1,i
        elif i['date'] < selected_date.strftime('%d-%m-%Y'):
            return 0,i


mutual_funds,data = getMFList()

# Create a Streamlit app
st.title("Mutual Fund Analyzer")

# Dropdown for Mutual Fund Name
selected_fund = st.selectbox("Mutual Fund Name", mutual_funds)

# Date selector with default as current date
selected_date = st.date_input("Select Date", datetime.now(), min_value=datetime(1990, 1, 1), format="DD-MM-YYYY")


# Submit button
if st.button("Submit"):
    with st.spinner("Finding the results...."):
        link = getLink(selected_fund,data)
        error_code,e = getData(link)

    if error_code == 0:
        st.warning(f"Sorry, No Data Found for the date {selected_date.strftime('%d-%m-%Y')}! ☹️")
        st.info(f"Last updated data is on {e['date']}, NAV: {round(Decimal(e['nav']),3)}")
    else:
        st.success(f"NAV of {selected_fund} on {selected_date.strftime('%d-%m-%Y')} is {round(Decimal(e['nav']),3)}")
