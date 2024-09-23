import pandas as pd
import pickle
import numpy as np
import os
import sys

def inference_prob_17( df_inference ):

    model_name = "20240914_pycaret_class_macropat_letteremappate.pkl"

    with open(f"models/{model_name}", "rb") as file:
        model_loaded = pickle.load(file)

    class_int = model_loaded.predict( df_inference )[0]

    list_prob = list(model_loaded.predict_proba(df_inference)[0])

    return class_int, list_prob

def inference_prob_6( df_inference ):

    model_name = "20240921_pycaret_6class_macropat_letteremappate_schiantato.pkl"

    with open(f"models/{model_name}", "rb") as file:
        model_loaded = pickle.load(file)

    class_int = model_loaded.predict( df_inference )[0]

    list_prob = list(model_loaded.predict_proba(df_inference)[0])

    return class_int, list_prob