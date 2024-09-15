import streamlit as st
import pandas as pd
import numpy as np

from lib.inference import inference_prob
from lib.map_classification import maps_class

# Page Title
st.title("Classificatore Emogas/Patologie - Versione beta")

# Columns input
columns = ['SESSO', 'ETA', 'TIPO', 'PF', 'PO2_T', 'P50_ACT', 'TO2', 'AG_K', 'THB2',
           'GLU', 'LAC', 'PO2', 'HCO3', 'PCO2_T', 'MOSM', 'KP', 'NA', 'CL',
           'CBASE', 'METHB', 'PH', 'O2HB', 'COHB', 'B', 'TC', 'FIO2',
           'class_symptom', 'DATA']


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
        data[col] = st_col1.number_input(f"Inserisci {col}")

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
    elif col == "class_symptom":
        data[col] = st_col2.selectbox(f"Seleziona {col}", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    else:
        data[col] = st_col2.number_input(f"Inserisci {col}")



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

# Pulsante per avviare il calcolo
if st.button("Calcola"):
    class_int, list_prob = inference_prob( df )  # Chiamata alla funzione importata
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