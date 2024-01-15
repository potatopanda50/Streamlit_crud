import streamlit as st
import pandas as pd
from datetime import date
from st_pages import add_page_title

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

add_page_title()
st.divider()

#load data sales on accounts - collections
sales_on_accounts = pd.read_csv('./data/sales_on_accounts.csv')
collections = pd.read_csv('./data/collections.csv')

groupped_sales_on_accounts = sales_on_accounts.groupby('Customer')['Amount'].sum().reset_index().set_index('Customer')
groupped_collections = collections.groupby('Customer')['Amount'].sum().reset_index().set_index('Customer')

groupped_sales_on_accounts['Sales on Accounts'] = groupped_sales_on_accounts['Amount']
groupped_collections['Collections'] = groupped_collections['Amount']

groupped_sales_on_accounts = groupped_sales_on_accounts.drop('Amount',axis=1)
groupped_collections = groupped_collections.drop('Amount',axis=1)

collectibles_df = pd.concat([groupped_sales_on_accounts,groupped_collections])
collectibles_df = collectibles_df.fillna(0)
collectibles_df['Collectibles'] = collectibles_df['Sales on Accounts'] - collectibles_df['Collections']

config = {
    'Customer' : st.column_config.TextColumn('Customer'),
    'Sales on Accounts' : st.column_config.NumberColumn('Sales on Accounts',format="₱%d"),
    'Collections' : st.column_config.NumberColumn('Collections',format="₱%d"),
    'Collectibles' : st.column_config.NumberColumn('Collectibles',format="₱%d"),
}

st.dataframe(collectibles_df,column_config=config,width=900)

btn, total = st.columns([8,2])

with btn:
    csv = convert_df(collectibles_df)
    st.download_button(
        label="Download",
        data=csv,
        file_name='Collectibles.csv',
        mime='text/csv'
        )

with total:
    st.write(f"Total: ₱{collectibles_df['Collectibles'].sum():,}")



