import streamlit as st
import pandas as pd
import numpy as np

from lib.inference import inference_prob
from lib.map_classification import maps_class, maps_class_long



def page_inference():
    # Page Title
    st.title("Classificatore Emogas/Patologie - Versione beta")

    st.markdown("""
    ***Funzionamento dell'applicativo:***
    Inserire i dati del paziente di test, dopodichè cliccare sul bottone "***Inferenza***".

    Uscirà come risultato la ***patologia*** individuata dal modello per il paziente di test e la relativa ***confidenza***.

    Per valutare l'attendibilità del dato con una certa confidenza, consultare la sezione "***Performance***".

    Inoltre, verranno mostrate anche le successive 4 patologie (se esistono) che il modello identifica con una confidenza maggiore.


    ***N.B:*** 
    - Questa web-app ha lo scopo di illustrare il funzionamento del modello di AI costruito durante lo sviluppo, ed in particolare di illustrare la struttura di input e di output.
    - Inoltre, il modello è stato addestrato sui dati degli Emogas condotti in pronto soccorso, quindi su dei pazienti con DETERMINATI SINTOMI.
    - Di conseguenza, questa web app non ha lo scopo (ne la capacità) di diagnosticare alcun tipo di patologia a dei pazienti che inseriscono in autonomia i propri dati.
    """)

    # Columns input
    columns = ['SESSO', 'ETA', 'TIPO', 'PF', 'PO2_T', 'P50_ACT', 'TO2', 'AG_K', 'THB2',
            'GLU', 'LAC', 'PO2', 'HCO3', 'PCO2_T', 'MOSM', 'KP', 'NA', 'CL',
            'CBASE', 'METHB', 'PH', 'O2HB', 'COHB', 'B', 'TC', 'FIO2',
            'class_symptom', 'DATA']

    columns1 = ['SESSO', 'ETA', 'TIPO', 'PF', 'PO2_T', 'P50_ACT', 'TO2', 'AG_K', 'THB2',
            'GLU', 'LAC', 'PO2', 'HCO3', 'PCO2_T' ]
    
    columns2 = [ 'MOSM', 'KP', 'NA', 'CL',
            'CBASE', 'METHB', 'PH', 'O2HB', 'COHB', 'B', 'TC', 'FIO2',
            'class_symptom', 'DATA' ]

    # ----------------  INSERT VALUES ---------------- #
    # Creazione di una singola riga vuota
    data = {col: '' for col in columns}


    st_col1, st_col2 = st.columns(2)

    data['SESSO'] = st_col1.selectbox(f"Seleziona Sesso", options=["M", "F"])  # Dropdown per SESSO
    data['ETA'] = st_col1.number_input(f"Inserisci Età", min_value=0, step=1, value=69)
    data['TIPO'] = st_col1.selectbox(f"Seleziona TIPO", options=['Venoso', 'Arterioso'])  # Dropdown per TIPO
    data['PF'] = st_col1.number_input(f"Inserisci PF", min_value=8.8, max_value=3004.8,step=0.1, value=250.95)
    data['PO2_T'] = st_col1.number_input(f"Inserisci PO2_T", min_value=6.90, max_value=631.00, step=0.1, value=59.20)
    data['P50_ACT'] = st_col1.number_input(f"Inserisci P50_ACT", min_value=11.80, max_value=191.21 ,step=0.1, value=27.45)
    data['TO2'] = st_col1.number_input(f"Inserisci TO2", min_value=0.7, max_value=32.40,step=0.1, value=15.10)
    data['AG_K'] = st_col1.number_input(f"Inserisci AG_K", min_value=-318.00, max_value=324.40,step=0.1, value=14.10)
    data['THB2'] = st_col1.number_input(f"Inserisci THB2", min_value=3.00, max_value=23.80,step=0.1, value=13.5)
    data['GLU'] = st_col1.number_input(f"Inserisci GLU", min_value=8.00,max_value=1070.00, step=0.1, value=118.00)
    data['LAC'] = st_col1.number_input(f"Inserisci LAC", min_value=0.00, max_value=28.00, step=0.1, value=1.2)
    data['PO2'] = st_col1.number_input(f"Inserisci PO2", min_value=7.4, max_value=83.20, step=0.1, value=61.40)
    data['HCO3'] = st_col1.number_input(f"Inserisci HCO3", min_value=1.7, max_value=61.60, step=0.1, value=23.50)
    data['PCO2_T'] = st_col1.number_input(f"Inserisci PCO2_T", min_value=10.10, max_value=216.00, step=0.1, value=37.6)


    for col in columns2:            
        if col == "class_symptom":
            data[col] = st_col2.selectbox(f"Seleziona {col}", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        elif col != "DATA":
            data[col] = st_col2.number_input(f"Inserisci {col}")

    data['DATA'] = st_col2.date_input(f"Inserisci DATA")


    # Creazione del DataFrame per visualizzare la tabella
    df = pd.DataFrame([data])

    # Mostra la tabella
    st.write("Riepilogo valori inseriti:")
    st.dataframe(df)


    # Estrae il giorno dell'anno
    df['day_of_year'] = df['DATA'].apply(lambda x: x.timetuple().tm_yday)

    # Calcola le nuove colonne "sin_day" e "cos_day"
    df['sin_day'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
    df['cos_day'] = np.cos(2 * np.pi * df['day_of_year'] / 365)

    df = df.drop(columns=[ "DATA", "day_of_year" ])

    st_col1, st_col2, _, _ = st.columns(4)

    # Pulsante per avviare il calcolo
    if st_col1.button("Inferenza"):
        class_int, list_prob = inference_prob( df )  # Chiamata alla funzione importata
        class_str = maps_class(class_int)
        class_str_long = maps_class_long(class_int)
        confidence = list_prob[class_int]

        # Determina il colore del riquadro in base a 'probability'
        if confidence < 0.3:
            box_color = "#ffcccc"  # Rosso chiaro
        elif confidence < 0.7:
            box_color = "#ffffcc"  # Giallo chiaro
        else:
            box_color = "#ccffcc"  # Verde chiaro

        # Mostra il risultato in un riquadro colorato
        st.markdown(f"""
            <div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">
                <h4>Output del modello:</h4>
                <p>{class_str} - {class_str_long}</p>
                <p><strong>Confidenza: {confidence:.2f}</strong></p>
            </div>
        """, unsafe_allow_html=True)

    if st_col2.button("Performance"):
        st.session_state.page = "page_performance"


def page_performance():
    st.markdown("Pagina delle performance")


    if st.button("Back to Inference"):
        st.session_state.page = "page_inference"