import dotenv
import pandas as pd
from joblib import load
import numpy as np
from evidently import ColumnMapping
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.metric_preset import TextEvals
from evidently.descriptors import *
from evidently.metrics import *
from evidently.tests import *
from evidently.features.llm_judge import BinaryClassificationPromptTemplate
import os
import warnings
import requests
from io import BytesIO
from logs import init_log, logging_msg



warnings.filterwarnings("ignore", category=UserWarning) # ras le bol des warnings de scikit-learn

####################################################################################################
####################################################################################################
####################################################################################################

############
### INIT ###
############
def init()->bool:
    try:
        dotenv.load_dotenv(override=True)
        if init_log() == False:
            raise Exception("Error in utils.py init(): init_log() failed")
        return True
    
    except Exception as e:
        print(e)
        return False
    

####################################################################################################
####################################################################################################
####################################################################################################

def predict(
        island: str,
        bill_length_mm: float,
        bill_depth_mm: float,
        flipper_length_mm: float,
        body_mass_g: float,
        sex: str)->str:
    log_prefix = '[utils | predict]'
    try:
        if init() == False:
            raise Exception("Error in utils.py predict(): init() failed")

        # MODEL
        DOCKER = os.getenv("DOCKER")
        if DOCKER == '1':
            model = load('model_model.pkl')
            scaler = load('model_scaler.pkl')
        else:
            model = load('./app/model_model.pkl')
            scaler = load('./app/model_scaler.pkl')

        # DATA
        data = {
            'island': ['Biscoe', 'Dream', 'Torgersen', island],
            'bill_length_mm': [0, 1, 2, bill_length_mm],
            'bill_depth_mm': [3, 4, 5, bill_depth_mm],
            'flipper_length_mm': [6, 7, 8, flipper_length_mm],
            'body_mass_g': [9, 10, 11, body_mass_g],
            'sex': ['Female', 'Male', 'Female', sex]
        }
        X = pd.DataFrame(data)
        
        # PREDICTION
        X_dummies = pd.get_dummies(X)
        X_valid_sample_transformed = scaler.transform([X_dummies.iloc[3]])
        y_pred_sample = model.predict(X_valid_sample_transformed)

        # DASHBOARD EVIDENTLY
        # dashboard = Dashboard(tabs=[DataDriftTab(), RegressionPerformanceTab()])
        # dashboard.calculate(X, y_pred_sample)
        # dashboard.show()
        # response = requests.get("https://raw.githubusercontent.com/evidentlyai/evidently/main/examples/how_to_questions/chat_df.csv")
        # csv_content = BytesIO(response.content)


        return y_pred_sample[0]
    
    except Exception as e:
        logging_msg(f"{log_prefix} {e}", 'ERROR')
        return None