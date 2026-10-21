# home page content

import streamlit as st


def render_home_page() -> None:
    
    # page title
    
    with st.container(key="title_home_page"):
        st.header("Welcome to my Streamlit App 👋")
        st.subheader("")
        st.caption("")

        
    # introduction section
    
    st.divider()
    st.caption("")

    
    with st.container(key="home_intro"):
        
        st.markdown("On this home page, you will find answers to some of the key questions you may have about this application and the technology behind it.")

    
    st.caption("")
    st.divider()
    st.subheader("")


    # q&a
    
    with st.container(key="qa_home_page"):

        st.caption("")

        st.subheader("1 - What is a Streamlit App ?")

        st.caption("")

        st.markdown("An interactive web application.")
        
        st.caption("")

        st.subheader("2 - What will you find in this application ?")

        st.caption("")

        st.markdown("**Different projects** that can be built with Streamlit.")

        st.caption("")

        st.subheader("3 - Why use Streamlit ?")

        st.caption("")

        st.markdown("A simple way to **turn data into interactive visualizations**.")

        st.caption("")

        st.subheader("4 - How is a Streamlit App built ?")

        st.caption("")

        st.markdown("Primarily with **Python**, but other technologies can also be used to further customize the app.")
