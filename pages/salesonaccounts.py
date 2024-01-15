import streamlit as st
import pandas as pd
from datetime import date
from st_pages import add_page_title


add_page_title()
st.divider()

def loader(filename):
    dataframe = pd.read_csv(filename)
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])
    dataframe['Customer'] = dataframe['Description'].astype(str)
    dataframe['Description'] = dataframe['Description'].astype(str)
    dataframe['OR'] = pd.to_numeric(dataframe['OR'])
    dataframe['Amount'] = pd.to_numeric(dataframe['Amount'])
    dataframe = dataframe.dropna()
    return dataframe

def save(dataframe):
    dataframe.to_csv('./data/sales_on_accounts.csv', index=False)

st.session_state["salesonaccounts_toggle"] = st.toggle('New Records')
st.caption('Always Click Save to Retain Changes')

df = loader('./data/sales_on_accounts.csv')

config = {
    'Date' : st.column_config.DateColumn('Date',min_value=date(2019, 1, 1),format="MM.DD.YYYY",width="medium",step=1,required=True),
    'Customer' : st.column_config.TextColumn('Customer',required=True),
    'Description' : st.column_config.TextColumn('Description',required=True),
    'OR' : st.column_config.NumberColumn('Offical Receipt', min_value=0,step=1,required=True),
    'Amount' : st.column_config.NumberColumn('Amount', min_value=0,step=1,format="₱%d",required=True),
}

if st.session_state["salesonaccounts_toggle"] == True:
    edited_df = st.data_editor(df,column_config=config,num_rows="dynamic",width=900,hide_index=True)

if st.session_state["salesonaccounts_toggle"] == False:
    edited_df = st.data_editor(df,column_config=config,num_rows="fixed",width=900,hide_index=True)

btn, total = st.columns([8,2])
with btn:
    btn_save = st.button("Save",type="primary")
with total:
    st.write(f"Total: {edited_df['Amount'].sum():,}")
    
if btn_save:
    save(edited_df)