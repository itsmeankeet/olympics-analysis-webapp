import streamlit as st
import pandas as pd 

st.sidebar.title("Olympics Data Analysis")
st.sidebar.radio("Select the Analysis", ["Medals", "Athletes", "Countries"])