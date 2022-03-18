# Modules Import
import streamlit as st
st.set_page_config(layout = "wide")
from CR_Predict_Page import show_predict_page # Import Prediction Page
from CR_Explore_Page import show_explore_page # Import Exploration Page
from PIL import Image

# Header and Subheader
st.markdown('<style>.header{font-family:Verdana; color:Black; font-size: 30px;}</style>', unsafe_allow_html = True)
st.markdown('<style>.subheader{font-family:Verdana; color:Green; font-size: 20px;}</style>', unsafe_allow_html = True)

image = Image.open('APU Logo.png') # APU Logo
col1, mid, col2 = st.columns([5, 1, 20])
with col1:
    st.image(image, width=200)
with col2:
    st.markdown('<p class = "header">Machine Learning and Explainable Artificial Intelligence (XAI) in Credit Risk Modelling</p>', unsafe_allow_html = True)
    st.markdown('<p class = "subheader">Developed by: Heng Yi Sheng (TP048930) <br>Supervised by: Dr. Preethi Subramanian</p>', unsafe_allow_html = True)

# Create sidebar menu selection 
menu = st.sidebar.selectbox('Predict or Explore', ('Explore', 'Predict'))

# Change between prediction page or exploration page
if menu == 'Predict':
    st.sidebar.info('**Credit Risk Prediction Page**') # Prediction Page
    show_predict_page() 
else:
    st.sidebar.info('**Credit Risk Exploration Page**') # Exploration Page
    show_explore_page()
    
