import dotenv

import os
from datetime import datetime
import json

from logs import init_log, logging_msg



####################################################################################################
####################################################################################################
####################################################################################################

############
### INIT ###
############
def init(metrics_path: str)->bool:
    try:
        dotenv.load_dotenv(override=True)

        if init_log() == False:
            raise Exception("Error in utils.py init(): init_log() failed")
        
        if not os.path.exists(metrics_path):
            with open(metrics_path, 'w') as f:
                f.write('[]')
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

def generate_metrics(concept_drift: bool, data_drift: bool)->bool:
    log_prefix = '[drift_metrics | generate_metrics]'
    try:
        PATH_MODEL = os.getenv('PATH_MODEL')
        metrics_path = os.path.join(PATH_MODEL, 'metrics.json')
        
        if init(metrics_path) == False:
            raise Exception("Error in drift_metrics.py generate_metrics(): init() failed")
        logging_msg(f"{log_prefix} generate_metrics() called")

        with open(metrics_path, 'r') as f:
            metrics_data = json.load(f)
        logging_msg(f"{log_prefix} metrics_data loaded", 'DEBUG')

        if concept_drift:
            concept_drift = 1
        else:
            concept_drift = 0
        if data_drift:
            data_drift = 1
        else:
            data_drift = 0
        timestamp = datetime.utcnow().isoformat()
        metrics_data.append({
            "timestamp": timestamp,
            "concept_drift": concept_drift,
            "data_drift": data_drift
        })
        logging_msg(f"{log_prefix} new record added", 'DEBUG')

        with open(metrics_path, 'w') as f:
            json.dump(metrics_data, f)
        logging_msg(f"{log_prefix} metrics_data saved", 'DEBUG')
        
        return True
        
    except Exception as e:
        logging_msg(f"{log_prefix} {e}", 'ERROR')
        return False


def get_metrics_by_json()->list:
    log_prefix = '[drift_metrics | get_metrics]'
    try:
        PATH_MODEL = os.getenv('PATH_MODEL')
        metrics_path = os.path.join(PATH_MODEL, 'metrics.json')

        if init(metrics_path) == False:
            raise Exception("Error in drift_metrics.py get_metrics(): init() failed")
        logging_msg(f"{log_prefix} get_metrics() called")
        
        if not os.path.exists(metrics_path):
            raise Exception("metrics.json does not exist")
        
        with open(metrics_path, 'r') as f:
            metrics_data = json.load(f)
        logging_msg(f"{log_prefix} metrics_data loaded", 'DEBUG')
        
        return metrics_data
    
    except Exception as e:
        logging_msg(f"{log_prefix} {e}", 'ERROR')
        return []
    

def remove_old_entries():
    log_prefix = '[drift_metrics | remove_old_entries]'
    try:
        PATH_MODEL = os.getenv('PATH_MODEL')
        metrics_path = os.path.join(PATH_MODEL, 'metrics.json')

        if init(metrics_path) == False:
            raise Exception("Error in drift_metrics.py remove_old_entries(): init() failed")
        logging_msg(f"{log_prefix} remove_old_entries() called")
        
        if not os.path.exists(metrics_path):
            raise Exception("metrics.json does not exist")
        
        with open(metrics_path, 'r') as f:
            metrics_data = json.load(f)
        logging_msg(f"{log_prefix} metrics_data loaded", 'DEBUG')

        x_minutes_ago = datetime.utcnow().timestamp() - 10
        metrics_data = [entry for entry in metrics_data if datetime.fromisoformat(entry["timestamp"]).timestamp() > x_minutes_ago]
        logging_msg(f"{log_prefix} old records removed", 'DEBUG')

        with open(metrics_path, 'w') as f:
            json.dump(metrics_data, f)
        logging_msg(f"{log_prefix} metrics_data saved", 'DEBUG')
        
    except Exception as e:
        logging_msg(f"{log_prefix} {e}", 'ERROR')