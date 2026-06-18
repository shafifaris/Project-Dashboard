import streamlit as st

st.set_page_config(
    page_title="Bank XYZ | Customer Experience",
    layout="wide",
    initial_sidebar_state="expanded"
)

pg = st.navigation(
    [
        st.Page("pages/1_Overview.py",            title="Overview"),
        st.Page("pages/2_Branch_Intelligence.py", title="Branch Intelligence"),
        st.Page("pages/3_Touchpoint.py",          title="Touchpoint"),
        st.Page("pages/4_Customer_Behaviour.py",  title="Customer Behaviour"),
        st.Page("pages/5_Competitor.py",          title="Competitor"),
    ],
    position="hidden",
)
pg.run()