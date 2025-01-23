import dotenv
import pandas as pd
from joblib import load
import numpy as np
from evidently.ui.workspace.cloud import CloudWorkspace
from evidently.report import Report
from evidently.metric_preset import DataQualityPreset
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import *
from evidently.test_suite import TestSuite
from evidently.tests import *
from evidently.test_preset import DataDriftTestPreset
from evidently.tests.base_test import TestResult, TestStatus
import os
import warnings
from io import BytesIO
from logs import init_log, logging_msg



# warnings.filterwarnings("ignore", category=UserWarning) # ras le bol des warnings de scikit-learn
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

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
        PATH_MODEL = os.getenv('PATH_MODEL')
        model = load(f'{PATH_MODEL}model_model.pkl')
        scaler = load(f'{PATH_MODEL}model_scaler.pkl')
        
        # DATA FOR EVIDENTLY IA
        reference = pd.read_csv(f'{PATH_MODEL}penguins.csv')

        # DATA FOR PREDICT
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
        data_report = Report(
                metrics=[
                    DataDriftPreset(stattest='psi', stattest_threshold='0.3'),
                    DataQualityPreset(),
                ],
            )

        data_report.run(reference_data=X, current_data=X.iloc[0 : 100, :])
        print(data_report.metrics)


        return y_pred_sample[0]
    
    except Exception as e:
        logging_msg(f"{log_prefix} {e}", 'ERROR')
        return None