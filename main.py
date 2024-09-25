#C:\Minicinda\conda\Project\Project
import streamlit as st
import os
from tavily import TavilyClient

os.environ["TAVILY_API_KEY"] = "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"
api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    raise ValueError("Please set the TAVILY_API_KEY environment variable.")
tavily = TavilyClient(api_key=api_key)

@st.cache_data
def get_disease_symptoms(disease_name):
    try:
        response = tavily.search(query=disease_name)
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
if 'history' not in st.session_state:
    st.session_state['history'] = []

st.sidebar.title("Search History")
if st.session_state['history']:
    st.sidebar.write("You searched for:")
    for item in st.session_state['history']:
        st.sidebar.write(f"- {item}")
else:
    st.sidebar.write("No search history yet.")


if st.sidebar.button("Clear Search History"):
    st.session_state['history'] = []
    st.sidebar.write("Search history cleared.")


st.title("Disease Symptom Checker")


disease_name = st.text_input("Enter a disease name to get its symptoms:")


if disease_name and not disease_name.strip():
    st.error("Please enter a valid disease name.")
else:
    if disease_name:
        
        disease_name = disease_name.capitalize()

        if disease_name not in st.session_state['history']:
            st.session_state['history'].append(disease_name)

        st.write(f"### Symptoms of {disease_name}:")
        with st.spinner("Fetching symptoms..."):
            symptoms = get_disease_symptoms(disease_name)

       
        if symptoms:
            if 'results' in symptoms:
           
                for item in symptoms['results']:
                    if 'content' in item:
                        st.write(f"- {item['content']}")
                    else:
                        st.write("No 'content' key found in the response item.")
            else:
                st.write("No results found in the API response.")
        else:
            st.write("No symptoms found.")

       
        if symptoms and 'results' in symptoms:
            download_data = "\n".join([item['content'] for item in symptoms['results'] if 'content' in item])
            st.download_button(
                label="Download Results as Text",
                data=download_data,
                file_name=f"{disease_name}_symptoms.txt",
                mime="text/plain"
            )

