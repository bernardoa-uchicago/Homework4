import streamlit as st
from PIL import Image

st.set_page_config(page_title="Homework 4", layout="wide")

st.title("Homework 4")
st.write(Image.open('images/UChicago-logo.jpg'))
st.write("Exploring a Data Story from the analysis done in Homework 3\n")
