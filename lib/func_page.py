import streamlit as st
import pandas as pd
import numpy as np

from lib.inference import inference_prob_17, inference_prob_6
from lib.map_classification import maps_class, maps_class_long, map_symptoms



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
            'SINTOMO', 'DATA']

    columns1 = ['SESSO', 'ETA', 'TIPO', 'PF', 'PO2_T', 'P50_ACT', 'TO2', 'AG_K', 'THB2',
            'GLU', 'LAC', 'PO2', 'HCO3', 'PCO2_T' ]
    
    columns2 = [ 'MOSM', 'KP', 'NA', 'CL',
            'CBASE', 'METHB', 'PH', 'O2HB', 'COHB', 'B', 'TC', 'FIO2',
            'SINTOMO', 'DATA' ]

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

    data['MOSM'] = st_col2.number_input(f"Inserisci MOSM", min_value=123.6, max_value=694.0,step=0.1, value=288.00)
    data['KP'] = st_col2.number_input(f"Inserisci KP", min_value=0.9, max_value=22.4,step=0.1, value=4.0)
    data['NA'] = st_col2.number_input(f"Inserisci NA", min_value=59.0, max_value=344.0, step=0.1, value=140.0)
    data['CL'] = st_col2.number_input(f"Inserisci CL", min_value=23.00, max_value=317.00 ,step=0.1, value=107.00)
    data['CBASE'] = st_col2.number_input(f"Inserisci CBASE", min_value=-30.2, max_value=34.60,step=0.1, value=-0.60)
    data['METHB'] = st_col2.number_input(f"Inserisci METHB", min_value=0.00, max_value=4.9,step=0.1, value=0.8)
    data['PH'] = st_col2.number_input(f"Inserisci PH", min_value=6.43, max_value=7.79,step=0.1, value=7.39)
    data['O2HB'] = st_col2.number_input(f"Inserisci O2HB", min_value=4.10,max_value=100.00, step=0.1, value=88.60)
    data['COHB'] = st_col2.number_input(f"Inserisci COHB", min_value=0.00, max_value=38.40, step=0.1, value=1.0)
    data['B'] = st_col2.number_input(f"Inserisci B", min_value=733.00, max_value=777.00, step=0.1, value=755.00)
    data['TC'] = st_col2.number_input(f"Inserisci TC", min_value=33.0, max_value=41.50, step=0.1, value=36.00)
    data['FIO2'] = st_col2.number_input(f"Inserisci FIO2", min_value=21.00, max_value=100.00, step=0.1, value=21.00)
    data["SINTOMO"] = st_col2.selectbox(f"Seleziona SINTOMO", options=['DOLORE TORACICO', 'CARDIOPALMO', 'TRAUMA GRAVE', 'TRAUMA',
                                                                'DISTURBI PSICHICI', 'DISPNEA', 'DISTURBI NEUROLOGICI', 'CEFALEA',
                                                                'EMORRAGIE', 'PERDITA DI CONOSCENZA (SINCOPE)',
                                                                'SEGNI / SINTOMI MINORI', 'INTOSSICAZIONE',
                                                                'DOLORE ADDOMINALE', 'FEBBRE-PROTOCOLLO SEPSI',
                                                                'TRAUMA MINORE', 'ALTERAZIONE PARAMETRI VITALI', 'ALTRO'])
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

    df["class_symptom"] = df.SINTOMO.apply(map_symptoms)

    df = df.drop(columns=[ "DATA", "day_of_year", "SINTOMO" ])

    df = df[['SESSO', 'ETA', 'TIPO', 'PF', 'PO2_T', 'P50_ACT', 'TO2', 'AG_K', 'THB2',
            'GLU', 'LAC', 'PO2', 'HCO3', 'PCO2_T', 'MOSM', 'KP', 'NA', 'CL',
            'CBASE', 'METHB', 'PH', 'O2HB', 'COHB', 'B', 'TC', 'FIO2',
            'class_symptom', 'sin_day', 'cos_day']]

    st_col1, st_col2, st_col3, _ = st.columns(4)

    # Pulsante per avviare il calcolo
    if st_col1.button("Inferenza - 17 classi"):
        class_int, list_prob = inference_prob_17( df )  # Chiamata alla funzione importata
        class_str = maps_class(class_int)
        class_str_long = maps_class_long(class_int)
        confidence = list_prob[class_int]

        D = {}
        for i in range(len(list_prob)):
            D[i] = list_prob[i]

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

        sorted_D = dict(sorted(D.items(), key=lambda item: item[1], reverse=True)[1:5])

        # Crea due colonne
        st_col21, st_col22 = st.columns(2)

        # Mostra i primi due elementi nella prima colonna e i successivi due nella seconda
        for i, (key, value) in enumerate(sorted_D.items()):
            if i < 2:
                st_col21.markdown(f"""
                    <div style="background-color: lightgray; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{maps_class(key)}</strong> : {value}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st_col22.markdown(f"""
                    <div style="background-color: lightgray; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{maps_class(key)}</strong> : {value}
                    </div>
                """, unsafe_allow_html=True)


    # Pulsante per avviare il calcolo
    if st_col2.button("Inferenza - 6 classi"):
        class_int, list_prob = inference_prob_6( df )  # Chiamata alla funzione importata
        class_str = maps_class(class_int)
        class_str_long = maps_class_long(class_int)
        confidence = list_prob[class_int]

        D = {}
        for i in range(len(list_prob)):
            D[i] = list_prob[i]

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

        sorted_D = dict(sorted(D.items(), key=lambda item: item[1], reverse=True)[1:3])

        # Crea due colonne
        st_col21, st_col22 = st.columns(2)

        # Mostra i primi due elementi nella prima colonna e i successivi due nella seconda
        for i, (key, value) in enumerate(sorted_D.items()):
            if i ==1:
                st_col21.markdown(f"""
                    <div style="background-color: lightgray; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{maps_class(key)}</strong> : {value}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st_col22.markdown(f"""
                    <div style="background-color: lightgray; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{maps_class(key)}</strong> : {value}
                    </div>
                """, unsafe_allow_html=True)



    if st_col3.button("Performance"):
        st.session_state.page = "page_performance"


def page_performance():
    st.markdown("""## Versione 17 classi
***Descrizione classi:***

Le Diagnosi dei pazienti vengono raggruppate secondo la classificazione ICD-9 nei diciassette capitoli di appartenenza, qui sotto elencati:
- 0 - TRM - Traumatismi e avvelenamenti
- 1 - INF - Malattie infettive e parassitarie
- 2 - NEOP - Tumori
- 3 - EN/IM - Malattie delle ghiandole endocrine, della nutrizione e del metabolismo, e disturbi immunitari
- 4 - EMO - Malattie del sangue e organi emopoietici
- 5 - MENT - Disturbi mentali
- 6 - NERV - Malattie del sistema nervoso e degli organi di senso
- 7 - CARD - Malattie del sistema circolatorio
- 8 - RESP - Malattie dell’apparato respiratorio
- 9 - DIG - Malattie dell’apparato digerente
- 10 - GEN - Malattie dell’apparato genitourinario
- 11 - GRAV - Complicazioni della gravidanza, del parto e del puerperio
- 12 - CT/CNN - Malattie della pelle e del tessuto sottocutaneo
- 13 - LOC - Malattie del sistema osteomuscolare e del tessuto connettivo
- 14 - MALF - Malformazioni congenite
- 15 - P.NAT - Alcune condizioni morbose di origine perinatale
- 16 - MAL - Sintomi, segni, e stati morbosi maldefiniti    
    """)

    st.image("images/confusion_matrix_17_v1.jpeg", caption="Matrice di confusione del modello a 17 classi")
    st.image("images/confusion_matrix_17_vth_65.jpeg", caption="Matrice di confusione del modello a 17 classi, fissata la threshold sulla confidenza a 0.65")







    if st.button("Back to Inference"):
        st.session_state.page = "page_inference"