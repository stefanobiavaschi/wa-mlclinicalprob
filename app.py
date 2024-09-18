import streamlit as st
import pandas as pd
import numpy as np

from lib.inference import inference_prob
from lib.map_classification import maps_class, maps_class_long

from lib.func_page import page_inference, page_performance


def main():
    st.set_page_config(
        page_title="ML - Clinical Probability",
        page_icon=":microscope:"
        )
    

    # Definizione delle pagine
    pages = {
        "page_inference": page_inference,
        "page_performance": page_performance
        }

    # Inizializzazione della sessione
    if "page" not in st.session_state:
        st.session_state.page = "page_inference"

    # Esegui la pagina corrispondente
    pages[st.session_state.page]()



if __name__ == "__main__":
    main()