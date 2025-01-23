import dotenv
import pandas as pd
from joblib import load
# import numpy as np
# from evidently.ui.workspace.cloud import CloudWorkspace
from evidently.report import Report
# from evidently.metric_preset import DataQualityPreset
from evidently.metric_preset import DataDriftPreset
# from evidently.metrics import *
# from evidently.test_suite import TestSuite
# from evidently.tests import * 
# from evidently.test_preset import DataDriftTestPreset
# from evidently.tests.base_test import TestResult, TestStatus
import os
import warnings
# from io import BytesIO
from logs import init_log, logging_msg



# warnings.filterwarnings("ignore", category=UserWarning) # ras le bol des warnings de scikit-learn
# warnings.filterwarnings('ignore')
# warnings.simplefilter('ignore')

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
        
        PATH_MODEL = os.getenv('PATH_MODEL')

        pred_penguins_path = os.path.join(PATH_MODEL, 'pred_penguins.csv')
        if not os.path.exists(pred_penguins_path):
            reference_data = pd.read_csv(os.path.join(PATH_MODEL, 'model_penguins.csv'))
            reference_data.head(0).to_csv(pred_penguins_path, index=False)
            logging_msg("pred_penguins.csv created")
        else:
            logging_msg("pred_penguins.csv already exists", 'DEBUG')

        metrics_path = os.path.join(PATH_MODEL, 'metrics.json')
        if not os.path.exists(metrics_path):
            with open(metrics_path, 'w') as f:
                f.write('{}')
            logging_msg("metrics.json created")
        else:
            logging_msg("metrics.json already exists", 'DEBUG')

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
        logging_msg(f"{log_prefix} model and scaler loaded", 'DEBUG')

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
        logging_msg(f"{log_prefix} data for prediction loaded", 'DEBUG')
        
        # PREDICTION
        logging_msg(f"{log_prefix} START prediction")
        X_dummies = pd.get_dummies(X)
        X_valid_sample_transformed = scaler.transform([X_dummies.iloc[3]])
        y_pred_sample = model.predict(X_valid_sample_transformed)

        # SAVE PREDICTION
        pred_penguins_path = os.path.join(PATH_MODEL, 'pred_penguins.csv')
        X_pred = X.iloc[3]
        X_pred['species'] = y_pred_sample[0]
        X_pred = pd.DataFrame([X_pred])
        cols = X_pred.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        X_pred = X_pred[cols]
        X_pred.to_csv(pred_penguins_path, mode='a', header=False, index=False)
        logging_msg(f"{log_prefix} prediction saved in pred_penguins.csv", 'DEBUG')

        # DATA FOR EVIDENTLY IA
        reference = pd.read_csv(f'{PATH_MODEL}model_penguins.csv')
        current = pd.read_csv(pred_penguins_path)
        logging_msg(f"{log_prefix} reference and current data for evidently ia loaded", 'DEBUG')

        # DASHBOARD EVIDENTLY
        logging_msg(f"{log_prefix} START evidently ia dashboard")
        report = Report(
                metrics=[
                    DataDriftPreset(),
                    # DataQualityPreset(),
                ],
            )

        report.run(reference_data=reference, current_data=current)
        report.save_html(f'{PATH_MODEL}report.html')

        return y_pred_sample[0]
    
    except Exception as e:
        logging_msg(f"{log_prefix} {e}", 'ERROR')
        return None