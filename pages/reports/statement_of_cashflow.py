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
cashadvances = pd.read_csv('data/cash_advances.csv')
inventory = pd.read_csv('data/inventory.csv')
sales_on_accounts = pd.read_csv('data/sales_on_accounts.csv')
collections = pd.read_csv('data/collections.csv')
savings = pd.read_csv('data/savings.csv')
accountspayable = pd.read_csv('data/accounts_payable.csv')
expensepayable = pd.read_csv('data/expense_payable.csv')
assets = pd.read_csv('data/assets.csv')
loans_payable = pd.read_csv('data/loans_payable.csv')
capital_buildup = pd.read_csv('data/capital_buildup.csv')


#aggregate
cashadvances['Date'] = pd.to_datetime(cashadvances['Date'])
inventory['Date'] = pd.to_datetime(inventory['Date'])
sales_on_accounts['Date'] = pd.to_datetime(sales_on_accounts['Date'])
collections['Date'] = pd.to_datetime(collections['Date'])
savings['Date'] = pd.to_datetime(savings['Date'])
accountspayable['Date'] = pd.to_datetime(accountspayable['Date'])
expensepayable['Date'] = pd.to_datetime(expensepayable['Date'])
assets['Date'] = pd.to_datetime(assets['Date'])
loans_payable['Date'] = pd.to_datetime(loans_payable['Date'])
capital_buildup['Date'] = pd.to_datetime(capital_buildup['Date'])

cashadvances = cashadvances[(cashadvances['Date'] >= st.session_state['start_date']) & (cashadvances['Date'] <= st.session_state['end_date'])]
inventory = inventory[(inventory['Date'] >= st.session_state['start_date']) & (inventory['Date'] <= st.session_state['end_date'])]
sales_on_accounts = sales_on_accounts[(sales_on_accounts['Date'] >= st.session_state['start_date']) & (sales_on_accounts['Date'] <= st.session_state['end_date'])]
collections = collections[(collections['Date'] >= st.session_state['start_date']) & (collections['Date'] <= st.session_state['end_date'])]
savings = savings[(savings['Date'] >= st.session_state['start_date']) & (savings['Date'] <= st.session_state['end_date'])]
accountspayable = accountspayable[(accountspayable['Date'] >= st.session_state['start_date']) & (accountspayable['Date'] <= st.session_state['end_date'])]
expensepayable = expensepayable[(expensepayable['Date'] >= st.session_state['start_date']) & (expensepayable['Date'] <= st.session_state['end_date'])]
assets = assets[(assets['Date'] >= st.session_state['start_date']) & (assets['Date'] <= st.session_state['end_date'])]
loans_payable = loans_payable[(loans_payable['Date'] >= st.session_state['start_date']) & (loans_payable['Date'] <= st.session_state['end_date'])]
capital_buildup = capital_buildup[(capital_buildup['Date'] >= st.session_state['start_date']) & (capital_buildup['Date'] <= st.session_state['end_date'])]



cashadvances.set_index('Date', inplace=True)
inventory.set_index('Date', inplace=True)
sales_on_accounts.set_index('Date', inplace=True)
collections.set_index('Date', inplace=True)
savings.set_index('Date', inplace=True)
accountspayable.set_index('Date', inplace=True)
expensepayable.set_index('Date', inplace=True)
assets.set_index('Date', inplace=True)
loans_payable.set_index('Date', inplace=True)
capital_buildup.set_index('Date', inplace=True)


if st.session_state['statement_of_operations'] == 'Monthly':
    # Resample the DataFrame to monthly frequency
    cashadvances = cashadvances.resample('M').sum().cumsum()
    inventory = inventory.resample('M').sum()
    sales_on_accounts = sales_on_accounts.resample('M').sum()
    collections = collections.resample('M').sum()
    savings = savings.resample('M').sum()
    accountspayable = accountspayable.resample('M').sum()
    expensepayable = expensepayable.resample('M').sum()
    assets = assets.resample('M').sum()
    loans_payable = loans_payable.resample('M').sum()
    capital_buildup = capital_buildup.resample('M').sum()

elif st.session_state['statement_of_operations'] == 'Quarterly':
    # Resample the DataFrame to quarterly frequency
    cashadvances = cashadvances.resample('Q').sum().cumsum()
    inventory = inventory.resample('Q').sum()
    sales_on_accounts = sales_on_accounts.resample('Q').sum()
    collections = collections.resample('Q').sum()
    savings = savings.resample('Q').sum()
    accountspayable = accountspayable.resample('Q').sum()
    expensepayable = expensepayable.resample('Q').sum()
    assets = assets.resample('Q').sum()
    loans_payable = loans_payable.resample('Q').sum()
    capital_buildup = capital_buildup.resample('Q').sum()

elif st.session_state['statement_of_operations'] == 'Annual':
    # Resample the DataFrame to annual frequency
    cashadvances = cashadvances.resample('A').sum().cumsum()
    inventory = inventory.resample('A').sum()
    sales_on_accounts = sales_on_accounts.resample('A').sum()
    collections = collections.resample('A').sum()
    savings = savings.resample('A').sum()
    accountspayable = accountspayable.resample('A').sum()
    expensepayable = expensepayable.resample('A').sum()
    assets = assets.resample('A').sum()
    loans_payable = loans_payable.resample('A').sum()
    capital_buildup = capital_buildup.resample('A').sum()


cashadvances['Change in Cash Advances'] = cashadvances['Amount']
inventory['Change in Inventory'] = inventory['Amount']
sales_on_accounts['Sales on Accounts'] = sales_on_accounts['Amount']
collections['Collections'] = collections['Amount']

collectibles = pd.concat([sales_on_accounts['Sales on Accounts'],collections['Collections']],axis=1)
collectibles = collectibles.fillna(0)
collectibles['Collectibles'] = collectibles['Sales on Accounts'] - collectibles['Collections']
collectibles['Change in Accounts Receivables'] = collectibles['Collectibles'].cumsum()
savings['Change in Savings Deposit'] = savings['Amount'].cumsum()
accountspayable['Change in Accounts Payable'] = accountspayable['Amount'].cumsum()
expensepayable['Change in Expense Payable'] = expensepayable['Amount'].cumsum()

cashflow = pd.DataFrame()
cashflow = pd.concat([cashadvances['Change in Cash Advances'],inventory['Change in Inventory'],collectibles['Change in Accounts Receivables'],savings['Change in Savings Deposit'],accountspayable['Change in Accounts Payable'],expensepayable['Change in Expense Payable']],axis=1)
cashflow['Net Operating Activities'] = cashflow.sum(axis=1)
cashflow.index = cashflow.index.strftime('%Y-%m-%d')

st.markdown("#### Cash Flow from Operating Activities")
cashflow.T


st.markdown("#### Cash Flow from Investing Activities")
assets['Change in Property Equipment'] = assets['Amount'].cumsum()
assets = pd.DataFrame(assets['Change in Property Equipment'])
assets.index = assets.index.strftime('%Y-%m-%d')
assets.T

st.markdown("#### Cash Flow from Financing Activities")
loans_payable['Change in Loans Payable'] = loans_payable['Amount'].cumsum()
capital_buildup['Change in Paid-up Share Capital'] = capital_buildup['Amount'].cumsum()
financing_activities = pd.DataFrame()
financing_activities = pd.concat([loans_payable['Change in Loans Payable'],capital_buildup['Change in Paid-up Share Capital']],axis=1)
financing_activities = financing_activities.fillna(0)
financing_activities['Net Financing Activities'] = financing_activities.sum(axis=1)
financing_activities.index = financing_activities.index.strftime('%Y-%m-%d')
financing_activities.T

st.markdown("#### Net Increase in Cash")
net_increase = pd.DataFrame()
net_increase = pd.concat([cashflow['Net Operating Activities'],assets['Change in Property Equipment'],financing_activities['Net Financing Activities']],axis=1)
net_increase = net_increase.fillna(0)
net_increase['Net Increase in Cash'] = net_increase.sum(axis=1)
net_increase = pd.DataFrame(net_increase['Net Increase in Cash'])
net_increase.T
# net_increase.index = pd.to_datetime(net_increase.index)
# net_increase.index = net_increase.index.strftime('%Y-%m-%d')
# net_increase.T