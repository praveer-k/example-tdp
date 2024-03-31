# Add new import statement
import os, json
import pandas as pd
from ts_sdk.task.__task_script_runner import Context

def csv_to_json(input: dict, context: Context) -> tuple[str, dict]:
    print("Process file data")
    print(f"Input: {input}")
    input_file_pointer = input["input_file_pointer"]
    print(f"Input file meta: {json.dumps(input_file_pointer['meta'], indent=2)}")

    print(f"Input file type: {input_file_pointer['type']}")
    print(f"Input file bucket: {input_file_pointer['bucket']}")
    print(f"Input file Key: {input_file_pointer['fileKey']}")
    print(f"Input file Id: {input_file_pointer['fileId']}")
    print(f"Input file Version: {input_file_pointer['version']}")
    
    f = context.read_file(input_file_pointer, form='file_obj')
    df = pd.read_csv(f['file_obj'])
    label_mapping = context.get_labels(input_file_pointer)
    column_new_names = {label['name']: label['value'] for label in label_mapping}
    df.rename(columns=column_new_names, inplace=True)
    file_name = context.get_file_name(input_file_pointer)
    data = df.to_dict(orient='records')
    print(f"File name: {file_name}")
    return file_name, data

# Add this new function
def push_data(input: dict, context: Context) -> dict:

    print("Starting push to 3rd party")

    # Pull out the arguments to the function
    kaggle_username = input["kaggle_username"]
    kaggle_api_key_secret = input["kaggle_api_key"]
    kaggle_api_key = context.resolve_secret(kaggle_api_key_secret)

    print("Start Kaggle content")
    # Kaggle Specific
    # Add username and API Key to OS environment
    os.environ['KAGGLE_USERNAME'] = kaggle_username
    os.environ['KAGGLE_KEY'] = kaggle_api_key

    # Kaggle Specific
    # Pull out the data from the PROCESSED file and save as a temporary file
    file_name, data = csv_to_json(input, context)
    formatted_data = {}
    formatted_data["data"] = data

    with open('data.json', 'w') as outfile:
        json.dump(formatted_data, outfile)

    # Kaggle Specific
    # Create dataset metadata and save as a temporary file
    dataset_name: str = file_name
    dataset_name = dataset_name.replace("_", "-").replace(".csv", "")
    dataset_metadata = {
                        "title": dataset_name,
                        "id": kaggle_username+"/"+dataset_name,
                        "licenses": [
                                {
                                "name": "CC0-1.0"
                                }
                            ]
                        }
    with open('dataset-metadata.json', 'w') as outfile:
        json.dump(dataset_metadata, outfile)

    # Kaggle Specific
    # Upload data to Kaggle. Uses OS environment variables
    os.system("kaggle datasets create -p .")