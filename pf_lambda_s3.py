import boto3
import json
import pandas as pd
import numpy as np
from io import BytesIO
from grid_feedback_optimizer.engine.powerflow import PowerFlowSolver
from grid_feedback_optimizer.models.network import Network

# S3 setup
s3 = boto3.client('s3')
BUCKET_NAME = "aws-powerflow-data"

# Helper functions
def read_json_from_s3(key):
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    return json.loads(obj['Body'].read().decode('utf-8'))

def read_csv_from_s3(key):
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    return pd.read_csv(BytesIO(obj['Body'].read()))

def write_json_to_s3(data, key):
    s3.put_object(Bucket=BUCKET_NAME, Key=key,
                  Body=json.dumps(data, indent=4).encode('utf-8'))

def run_powerflow(scenario_key):
    network_data = read_json_from_s3("grid.json")
    network = Network(**network_data)
    solver = PowerFlowSolver(network)

    gen_base = np.column_stack([np.array([g.p_norm for g in network.renew_gens]),
                                np.array([g.q_norm for g in network.renew_gens])])
    load_base = np.column_stack([np.array([l.p_norm for l in network.loads]),
                                 np.array([l.q_norm for l in network.loads])])

    scenario = read_csv_from_s3(scenario_key)
    is_congested = {}

    for i, s in enumerate(scenario.scenario_id):
        output = solver.run(gen_update=scenario.gen_scale[i] * gen_base,
                            load_update=scenario.load_scale[i] * load_base)
        is_congested[int(s)] = solver.is_congested(output)

    write_json_to_s3(is_congested, "is_congested.json")
    print("✅ Results saved to s3://{}/is_congested.json".format(BUCKET_NAME))

# Lambda handler
def lambda_handler(event, context):
    # Get the key of the uploaded object
    for record in event['Records']:
        s3_key = record['s3']['object']['key']
        if s3_key.endswith("scenario.csv"):
            run_powerflow(s3_key)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Power flow completed!')
    }
