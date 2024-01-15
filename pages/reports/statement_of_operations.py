import streamlit as st
import pandas as pd
from datetime import date
from st_pages import add_page_title


add_page_title()
st.divider()

periods , start , end = st.columns(3)

with periods:
    st.session_state['statement_of_operations'] = st.selectbox("Periods",['Monthly', 'Quarterly', 'Annual'])
with start:
    default_start_date = pd.to_datetime('2022-01-01')
    st.session_state['start_date'] = pd.to_datetime(st.date_input("Start Date",format="YYYY-MM-DD",value=default_start_date))
with end:
    st.session_state['end_date'] = pd.to_datetime(st.date_input("End Date",format="YYYY-MM-DD",value="today"))


#Load cash sales and sales on accounts
cashsales = pd.read_csv('data/cash_sales.csv')
sales_on_accounts = pd.read_csv('data/sales_on_accounts.csv')
direct_cost = pd.read_csv('data/direct_cost.csv')
other_income = pd.read_csv('data/other_income.csv')
administrative_cost = pd.read_csv('data/administrative_cost.csv')


#aggregate
cashsales['Date'] = pd.to_datetime(cashsales['Date'])
sales_on_accounts['Date'] = pd.to_datetime(sales_on_accounts['Date'])
direct_cost['Date'] = pd.to_datetime(direct_cost['Date'])
other_income['Date'] = pd.to_datetime(other_income['Date'])
administrative_cost['Date'] = pd.to_datetime(administrative_cost['Date'])

cashsales = cashsales[(cashsales['Date'] >= st.session_state['start_date']) & (cashsales['Date'] <= st.session_state['end_date'])]
sales_on_accounts = sales_on_accounts[(sales_on_accounts['Date'] >= st.session_state['start_date']) & (sales_on_accounts['Date'] <= st.session_state['end_date'])]
direct_cost = direct_cost[(direct_cost['Date'] >= st.session_state['start_date']) & (direct_cost['Date'] <= st.session_state['end_date'])]
other_income = other_income[(other_income['Date'] >= st.session_state['start_date']) & (other_income['Date'] <= st.session_state['end_date'])]
administrative_cost = administrative_cost[(administrative_cost['Date'] >= st.session_state['start_date']) & (administrative_cost['Date'] <= st.session_state['end_date'])]


cashsales.set_index('Date', inplace=True)
sales_on_accounts.set_index('Date', inplace=True)
direct_cost.set_index('Date', inplace=True)
other_income.set_index('Date', inplace=True)
administrative_cost.set_index('Date', inplace=True)

if st.session_state['statement_of_operations'] == 'Monthly':
    # Resample the DataFrame to monthly frequency
    cashsales = cashsales.resample('M').sum()
    sales_on_accounts = sales_on_accounts.resample('M').sum()
elif st.session_state['statement_of_operations'] == 'Quarterly':
    # Resample the DataFrame to quarterly frequency
    cashsales = cashsales.resample('Q').sum()
    sales_on_accounts = sales_on_accounts.resample('Q').sum()
elif st.session_state['statement_of_operations'] == 'Annual':
    # Resample the DataFrame to annual frequency
    cashsales = cashsales.resample('A').sum()
    sales_on_accounts = sales_on_accounts.resample('A').sum()
    

cashsales['Cash Sales'] = cashsales['Amount']
sales_on_accounts['Sales on Accounts'] = sales_on_accounts['Amount']


main_df = pd.concat([cashsales['Cash Sales'],sales_on_accounts['Sales on Accounts']],axis=1)
main_df.fillna(0, inplace=True)
main_df.index = main_df.index.strftime('%Y-%m-%d')

main_df["Total"] = main_df['Cash Sales'] + main_df['Sales on Accounts']


st.markdown("#### Revenue")
main_df.T
##################################################################################################################

if st.session_state['statement_of_operations'] == 'Monthly':
    direct_cost = direct_cost.groupby(['Description', pd.Grouper(freq='M')])['Amount'].sum().unstack()
elif st.session_state['statement_of_operations'] == 'Quarterly':
    direct_cost = direct_cost.groupby(['Description', pd.Grouper(freq='Q')])['Amount'].sum().unstack()
elif st.session_state['statement_of_operations'] == 'Annual':
    direct_cost = direct_cost.groupby(['Description', pd.Grouper(freq='A')])['Amount'].sum().unstack()

direct_cost = direct_cost.T
direct_cost.index = direct_cost.index.strftime('%Y-%m-%d')
direct_cost = direct_cost.T

direct_cost.fillna(0, inplace=True)
direct_cost['Total'] = direct_cost.sum(axis=1)

st.markdown("#### Direct Cost")
direct_cost

###################################################################################################################

st.markdown("#### Gross Profit")
direct_cost = direct_cost.drop('Total',axis=1)
direct_cost = direct_cost.T
direct_cost['Direct Cost'] = direct_cost.sum(axis=1)

cashsales.index = cashsales.index.strftime('%Y-%m-%d')
sales_on_accounts.index = sales_on_accounts.index.strftime('%Y-%m-%d')

gross_profit_df = pd.concat([cashsales['Cash Sales'],sales_on_accounts['Sales on Accounts'],direct_cost['Direct Cost'] ],axis=1)
gross_profit = pd.DataFrame()
gross_profit['Gross Profit'] = gross_profit_df.sum(axis=1)
gross_profit.T

####################################################################################################################
st.markdown("#### Other Income")

if st.session_state['statement_of_operations'] == 'Monthly':
    other_income = other_income.groupby(['Description', pd.Grouper(freq='M')])['Amount'].sum().unstack()
elif st.session_state['statement_of_operations'] == 'Quarterly':
    other_income = other_income.groupby(['Description', pd.Grouper(freq='Q')])['Amount'].sum().unstack()
elif st.session_state['statement_of_operations'] == 'Annual':
    other_income = other_income.groupby(['Description', pd.Grouper(freq='A')])['Amount'].sum().unstack()

other_income = other_income.T
other_income.index = other_income.index.strftime('%Y-%m-%d')
other_income = other_income.T

other_income.fillna(0, inplace=True)
other_income['Total'] = other_income.sum(axis=1)
other_income

####################################################################################################################
st.markdown("#### Total Gross Income")

other_income = other_income.drop('Total',axis=1)

total_gross_income_df = pd.concat([other_income.T,gross_profit],axis=1)
total_gross_income = pd.DataFrame()
total_gross_income['Total Gross Income'] = total_gross_income_df.sum(axis=1)
total_gross_income.T

####################################################################################################################
st.markdown("#### Operating Expense")

if st.session_state['statement_of_operations'] == 'Monthly':
    administrative_cost = administrative_cost.groupby(['Description', pd.Grouper(freq='M')])['Amount'].sum().unstack()
elif st.session_state['statement_of_operations'] == 'Quarterly':
    administrative_cost = administrative_cost.groupby(['Description', pd.Grouper(freq='Q')])['Amount'].sum().unstack()
elif st.session_state['statement_of_operations'] == 'Annual':
    administrative_cost = administrative_cost.groupby(['Description', pd.Grouper(freq='A')])['Amount'].sum().unstack()

administrative_cost = administrative_cost.T
administrative_cost.index = administrative_cost.index.strftime('%Y-%m-%d')
administrative_cost = administrative_cost.T

administrative_cost.fillna(0, inplace=True)
administrative_cost['Total'] = administrative_cost.sum(axis=1)
administrative_cost

#####################################################################################################################
st.markdown("#### Net Surplus")

administrative_cost = administrative_cost.drop('Total',axis=1)
net_surplus = pd.concat([administrative_cost.T,total_gross_income],axis=1)
net_surplus['Net Surplus'] =  net_surplus.sum(axis=1)
net_surplus = pd.DataFrame(net_surplus['Net Surplus'])
net_surplus.T