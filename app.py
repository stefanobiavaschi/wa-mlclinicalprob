import streamlit as st
import pandas as pd

from lib.inference import inference_prob
from lib.map_classification import maps_class

# Page Title
st.title("Classificatore Emogas/Patologie - Versione beta")

# Columns input
columns = ['SESSO', 'ETA', 'TIPO', 'PF', 'PO2_T', 'P50_ACT', 'TO2', 'AG_K', 'THB2',
           'GLU', 'LAC', 'PO2', 'HCO3', 'PCO2_T', 'MOSM', 'KP', 'NA', 'CL',
           'CBASE', 'METHB', 'PH', 'O2HB', 'COHB', 'B', 'TC', 'FIO2',
           'CODICE_SINTOMO', 'DATA']


# ----------------  INSERT VALUES ---------------- #
# Creazione di una singola riga vuota
data = {col: '' for col in columns}


half = len(columns) // 2
columns1 = columns[:half]
columns2 = columns[half:]

st_col1, st_col2 = st.columns(2)

for col in columns1:
    if col == 'SESSO':
        # st_col1.markdown(col)
        data[col] = st_col1.selectbox(f"Seleziona {col}", options=["M", "F"])  # Dropdown per SESSO
    elif col == 'TIPO':
        # st_col1.markdown(col)
        data[col] = st_col1.selectbox(f"Seleziona {col}", options=['Venoso', 'Arterioso'])  # Dropdown per TIPO
    elif col == 'ETA':
        data[col] = st_col1.number_input(f"Inserisci {col}", min_value=0, step=1, value=50)
    elif col == 'DATA':
        data[col] = st_col1.date_input(f"Inserisci {col}")
    else:
        data[col] = st_col1.text_input(f"Inserisci {col}")

for col in columns2:
    if col == 'SESSO':
        data[col] = st_col2.selectbox(f"Seleziona {col}", options=["M", "F"])  # Dropdown per SESSO
    elif col == 'TIPO':
        # st_col1.markdown(col)
        data[col] = st_col1.selectbox(f"Seleziona {col}", options=['Venoso', 'Arterioso'])  # Dropdown per TIPO
    elif col == 'ETA':
        data[col] = st_col2.number_input(f"Inserisci {col}", min_value=0, step=1, value=50)
    elif col == 'DATA':
        data[col] = st_col2.date_input(f"Inserisci {col}")
    else:
        data[col] = st_col2.text_input(f"Inserisci {col}")



# Creazione del DataFrame per visualizzare la tabella
df = pd.DataFrame([data])

# Mostra la tabella
st.write("Riepilogo valori inseriti:")
st.dataframe(df)


values = ['F', 79, 'Venoso', 89.04761904761904, 18.7, 33.27, 4.1, 12.3, 13.7, 108.0, 0.7, 20.1, 25.8, 44.4, 290.9, 4.4,
            142.0, 109.0, 1.0, 0.7, 7.362, 21.4, 0.3, 754.0, 36.0, 21.0, 10, -0.8958392907349089, -0.4443781781046134 ]

columns = ['SESSO', 'ETA', 'TIPO', 'PF', 'PO2_T', 'P50_ACT', 'TO2', 'AG_K', 'THB2',
       'GLU', 'LAC', 'PO2', 'HCO3', 'PCO2_T', 'MOSM', 'KP', 'NA', 'CL',
       'CBASE', 'METHB', 'PH', 'O2HB', 'COHB', 'B', 'TC', 'FIO2',
       'class_symptom', 'sin_day', 'cos_day' ]

# Pulsante per avviare il calcolo
if st.button("Calcola"):
    class_int, list_prob = inference_prob(columns, values)  # Chiamata alla funzione importata
    class_str = maps_class(class_int)
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
            <h4>Risultato più probabile:</h4>
            <p>{class_str}</p>
            <p><strong>Confidenza: {confidence:.2f}</strong></p>
        </div>
    """, unsafe_allow_html=True)