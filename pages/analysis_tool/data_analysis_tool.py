import streamlit as st
import pandas as pd
from datetime import date
from st_pages import add_page_title
import streamlit.components.v1 as components
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html



add_page_title(layout="wide")
st.divider()

# Initialize pygwalker communication
init_streamlit_comm()

# When using `use_kernel_calc=True`, you should cache your pygwalker html, if you don't want your memory to explode
@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    # When you need to publish your application, you need set `debug=False`,
    # to prevent other users from writing your config file.
    # If you want to use the feature of saving chart config, set `debug=True`
    html = get_streamlit_html(df, spec="./config.json", use_kernel_calc=True, debug=False)
    return html

# 1st is to upload files
# with st.sidebar:
uploaded_files  = st.file_uploader("Choose a Excel/CSV file", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(uploaded_file.name)
        if uploaded_file.name.lower().endswith(('.xlsx', '.xls', '.xlsb')):
            dataframe = pd.read_excel(uploaded_file, sheet_name='Sheet1')
            dataframe['Date'] = dataframe['Date'].astype(str)
            # print(dataframe.dtypes)
            components.html(get_pyg_html(dataframe), width=1300, height=1000, scrolling=True)
        elif uploaded_file.name.lower().endswith('.csv'):
            dataframe = pd.read_csv(uploaded_file)
            # print(dataframe.dtypes)
            components.html(get_pyg_html(dataframe), width=1300, height=1000, scrolling=True)
        # st.write(dataframe)
        st.divider()