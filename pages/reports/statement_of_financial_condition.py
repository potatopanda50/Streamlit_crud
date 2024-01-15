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
cash_on_hand = pd.read_csv('data/cash_on_hand.csv')
cash_sales = pd.read_csv('data/cash_sales.csv')
sales_on_accounts = pd.read_csv('data/sales_on_accounts.csv')
collections = pd.read_csv('data/collections.csv')
cash_advances = pd.read_csv('data/cash_advances.csv')
loans = pd.read_csv('data/loans.csv')
loan_payments = pd.read_csv('data/loan_payments.csv')
savings = pd.read_csv('data/savings.csv')
capital_buildup = pd.read_csv('data/capital_buildup.csv')
other_income = pd.read_csv('data/other_income.csv')
inventory = pd.read_csv('data/inventory.csv')
assets = pd.read_csv('data/assets.csv')

#aggregate
cash_on_hand['Date'] = pd.to_datetime(cash_on_hand['Date'])
cash_sales['Date'] = pd.to_datetime(cash_sales['Date'])
sales_on_accounts['Date'] = pd.to_datetime(sales_on_accounts['Date'])
collections['Date'] = pd.to_datetime(collections['Date'])
cash_advances['Date'] = pd.to_datetime(cash_advances['Date'])
loans['Date'] = pd.to_datetime(loans['Date'])
loan_payments['Date'] = pd.to_datetime(loan_payments['Date'])
savings['Date'] = pd.to_datetime(savings['Date'])
capital_buildup['Date'] = pd.to_datetime(capital_buildup['Date'])
other_income['Date'] = pd.to_datetime(other_income['Date'])
inventory['Date'] = pd.to_datetime(inventory['Date'])
assets['Date'] = pd.to_datetime(assets['Date'])



cash_on_hand = cash_on_hand[(cash_on_hand['Date'] >= st.session_state['start_date']) & (cash_on_hand['Date'] <= st.session_state['end_date'])]
cash_sales = cash_sales[(cash_sales['Date'] >= st.session_state['start_date']) & (cash_sales['Date'] <= st.session_state['end_date'])]
sales_on_accounts = sales_on_accounts[(sales_on_accounts['Date'] >= st.session_state['start_date']) & (sales_on_accounts['Date'] <= st.session_state['end_date'])]
collections = collections[(collections['Date'] >= st.session_state['start_date']) & (collections['Date'] <= st.session_state['end_date'])]
cash_advances = cash_advances[(cash_advances['Date'] >= st.session_state['start_date']) & (cash_advances['Date'] <= st.session_state['end_date'])]
loans = loans[(loans['Date'] >= st.session_state['start_date']) & (loans['Date'] <= st.session_state['end_date'])]
loan_payments = loan_payments[(loan_payments['Date'] >= st.session_state['start_date']) & (loan_payments['Date'] <= st.session_state['end_date'])]
savings = savings[(savings['Date'] >= st.session_state['start_date']) & (savings['Date'] <= st.session_state['end_date'])]
capital_buildup = capital_buildup[(capital_buildup['Date'] >= st.session_state['start_date']) & (capital_buildup['Date'] <= st.session_state['end_date'])]
other_income = other_income[(other_income['Date'] >= st.session_state['start_date']) & (other_income['Date'] <= st.session_state['end_date'])]
inventory = inventory[(inventory['Date'] >= st.session_state['start_date']) & (inventory['Date'] <= st.session_state['end_date'])]
assets = assets[(assets['Date'] >= st.session_state['start_date']) & (assets['Date'] <= st.session_state['end_date'])]


cash_on_hand.set_index('Date', inplace=True)
cash_sales.set_index('Date', inplace=True)
sales_on_accounts.set_index('Date', inplace=True)
collections.set_index('Date', inplace=True)
cash_advances.set_index('Date', inplace=True)
loans.set_index('Date', inplace=True)
loan_payments.set_index('Date', inplace=True)
savings.set_index('Date', inplace=True)
capital_buildup.set_index('Date', inplace=True)
other_income.set_index('Date', inplace=True)
inventory.set_index('Date', inplace=True)
assets.set_index('Date', inplace=True)

if st.session_state['statement_of_operations'] == 'Monthly':
    # Resample the DataFrame to monthly frequency
    cash_on_hand = cash_on_hand.resample('M').sum()
    cash_sales = cash_sales.resample('M').sum()
    sales_on_accounts = sales_on_accounts.resample('M').sum()
    collections = collections.resample('M').sum()
    cash_advances = cash_advances.resample('M').sum()
    loans = loans.resample('M').sum()
    loan_payments = loan_payments.resample('M').sum()
    savings = savings.resample('M').sum()
    capital_buildup = capital_buildup.resample('M').sum()
    other_income = other_income.resample('M').sum()
    inventory = inventory.resample('M').sum()
    # assets = assets.resample('M').sum()
    assets = assets.groupby(['Description', pd.Grouper(freq='M')])['Amount'].sum().unstack()

elif st.session_state['statement_of_operations'] == 'Quarterly':
    # Resample the DataFrame to quarterly frequency
    cash_on_hand = cash_on_hand.resample('Q').sum()
    cash_sales = cash_sales.resample('Q').sum()
    sales_on_accounts = sales_on_accounts.resample('Q').sum()
    collections = collections.resample('Q').sum()
    cash_advances = cash_advances.resample('Q').sum()
    loans = loans.resample('Q').sum()
    loan_payments = loan_payments.resample('M').sum()
    savings = savings.resample('Q').sum()
    capital_buildup = capital_buildup.resample('Q').sum()
    other_income = other_income.resample('Q').sum()
    inventory = inventory.resample('Q').sum()
    # assets = assets.resample('Q').sum()
    assets = assets.groupby(['Description', pd.Grouper(freq='Q')])['Amount'].sum().unstack()



elif st.session_state['statement_of_operations'] == 'Annual':
    # Resample the DataFrame to annual frequency
    cash_on_hand = cash_on_hand.resample('A').sum()
    cash_sales = cash_sales.resample('A').sum()
    sales_on_accounts = sales_on_accounts.resample('A').sum()
    collections = collections.resample('A').sum()
    cash_advances = cash_advances.resample('A').sum()
    loans = loans.resample('A').sum()
    loan_payments = loan_payments.resample('A').sum()
    savings = savings.resample('A').sum()
    capital_buildup = capital_buildup.resample('A').sum()
    other_income = other_income.resample('A').sum()
    inventory = inventory.resample('A').sum()
    # assets = assets.resample('A').sum()
    assets = assets.groupby(['Description', pd.Grouper(freq='A')])['Amount'].sum().unstack()



st.markdown("#### Current Assets")
current_assets = pd.DataFrame()
cash_on_hand['Beginning Balance'] = cash_on_hand['Amount']
cash_sales['Cash Sales'] = cash_sales['Amount']
collections['Collections'] = collections['Amount']
sales_on_accounts['Sales on Accounts'] = sales_on_accounts['Amount']
collectibles = pd.concat([sales_on_accounts['Sales on Accounts'],collections['Collections']],axis=1)
collectibles['Collectibles'] = collectibles['Sales on Accounts'] - collectibles['Collections']
cash_advances['Cash Advances'] = cash_advances['Amount']
savings['Savings'] = savings['Amount']
inventory['Inventory'] = inventory['Amount']

current_assets = pd.concat([cash_on_hand['Beginning Balance'],cash_sales['Cash Sales'],collections['Collections'],collectibles['Collectibles'],cash_advances['Cash Advances'],savings['Savings'],inventory['Inventory']],axis=1)
current_assets = current_assets.fillna(0)
current_assets['Total Current Asset'] = current_assets.sum(axis=1)
current_assets.index = current_assets.index.strftime('%Y-%m-%d')
current_assets.T

st.markdown("#### Non Current Assets")
# assets['Property Equipment'] = assets['Amount']
# assets = pd.DataFrame(assets['Property Equipment'])
# assets = assets.fillna(0)
# assets.index = assets.index.strftime('%Y-%m-%d')
assets = assets.T
assets.index = assets.index.strftime('%Y-%m-%d')
assets['Total Non Current Assets'] = assets.sum(axis=1)
assets .T

st.markdown("#### Total Assets")
total_assets = pd.concat([current_assets,assets],axis=1)
total_assets['Total Assets'] = total_assets.sum(axis=1)
total_assets = pd.DataFrame(total_assets['Total Assets'])
total_assets.T