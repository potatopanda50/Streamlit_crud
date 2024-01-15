import streamlit as st
import pandas as pd
from st_pages import Page,Section, show_pages, add_page_title

add_page_title()

st.write("# Welcome to Home Page! 👋")

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("main.py", "Home page", "🏠"),
        Section(name="Data Entry"),
        Page("pages/cashsales.py", "Cash Sales", ":ice_cream:"),
        Page("pages/salesonaccounts.py", "Sales on Accounts", ":ledger:"),
        Page("pages/collections.py", "Collections", ":moneybag:"),
        Page("pages/directcost.py", "Direct Cost", ":meat_on_bone:"),
        Page("pages/administrativecost.py", "Administrative Cost", ":male-technologist:"),
        Page("pages/cashadvances.py", "Cash Advances", ":money_with_wings:"),
        Page("pages/otherincome.py", "Other Income", ":seedling:"),
        Page("pages/savings.py", "Savings", ":old_key:"),
        Page("pages/capitalbuildup.py", "Capital Build-up", ":muscle:"),
        Page("pages/accountspayable.py", "Accounts Payable",":bookmark:"),
        Page("pages/expensepayable.py", "Expense Payable",":bell:"),
        Page("pages/loanspayable.py", "Loans Payable",":scroll:"),
        Page("pages/inventory.py", "Inventory", ":snowflake:"),
        Page("pages/assets.py", "Assets", ":cityscape:"),
        Page("pages/cashonhand.py", "Cash on Hand", ":credit_card:"),
        Section(name="Loans"),
        Page("pages/loans.py", "Loans Approved", ":hourglass:"),
        Page("pages/loanpayments.py", "Loan Payments", ":fax:"),
        Section(name="Data Query"),
        Page("pages/collectibles.py", "Collectibles", ":package:"),
        Section(name="Reports"),
        Page("pages/reports/statement_of_operations.py", "Statement of Operations", ":card_index:"),
        Page("pages/reports/statement_of_cashflow.py", "Statement of Cash Flow", ":currency_exchange:"),
        Page("pages/reports/statement_of_financial_condition.py", "Statement of Financial Condition",":chart_with_upwards_trend:"),
        Section(name="Data Tools"),
        Page("pages/analysis_tool/data_analysis_tool.py", "Data Analysis Tool", ":mag:"),



    ]
)

