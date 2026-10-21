# home page content

import streamlit as st


def render_home_page() -> None:

    # page title
    
    with st.container(key="home_page"):
        st.header("Welcome to my Streamlit App 👋")

    # introduction section
    
    st.divider()

    with st.container(key="home_intro"):
        
        st.markdown("On this home page, you will find answers to some of the key questions you may have about this application and the technology behind it.")

    st.divider()

    # q&a
    
    with st.container(key="home_page"):
        
        st.subheader("1 - What is a Streamlit App ?")
        
        st.markdown("An interactive web application.")

        st.subheader("2 - What will you find in this application ?")
        
        st.markdown("**Different projects** that can be built with Streamlit.")

        st.subheader("3 - Why use Streamlit ?")
        
        st.markdown("A simple way to **turn data into interactive visualizations**.")

        st.subheader("4 - How is a Streamlit App built ?")
        
        st.markdown("Primarily with **Python**, but other technologies can also be used to further customize the app.")
