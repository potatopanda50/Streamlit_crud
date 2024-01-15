import streamlit as st
import pandas as pd
from datetime import date
from st_pages import add_page_title


add_page_title()
st.divider()


# Function to read and process the uploaded file
# @st.cache_data
def loader(filename):
    dataframe = pd.read_csv(filename)
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])
    dataframe['Name'] = dataframe['Name'].astype(str)
    dataframe['Amount'] = pd.to_numeric(dataframe['Amount'])
    dataframe = dataframe.dropna()
    return dataframe

def save(dataframe):
    dataframe.to_csv('./data/loans.csv', index=False)
    # st.session_state["cashsales"] = [loader('./pages/cashsales/cash_sales.csv')]

st.session_state["loans_toggle"] = st.toggle('New Records')
st.caption('Always Click Save to Retain Changes')

df = loader('./data/loans.csv')

config = {
    'Date' : st.column_config.DateColumn('Date',min_value=date(2019, 1, 1),format="MM.DD.YYYY",width="medium",step=1,required=True),
    'Name' : st.column_config.TextColumn('Name',required=True),
    'Amount' : st.column_config.NumberColumn('Amount', min_value=0,step=1,format="₱%d",required=True),
}



if st.session_state["loans_toggle"] == True:
    edited_df = st.data_editor(df,column_config=config,num_rows="dynamic",width=900,hide_index=True)


if st.session_state["loans_toggle"] == False:
    edited_df = st.data_editor(df,column_config=config,num_rows="fixed",width=900,hide_index=True)

btn, total = st.columns([8,2])
with btn:
    btn_save = st.button("Save",type="primary")
with total:
    st.write(f"Total: {edited_df['Amount'].sum():,}")

# btn_save = st.button("Save",type="primary")
if btn_save:
    save(edited_df)
