from ts_sdk.task.__task_script_runner import Context

def decorate_input_file(input: dict, context: Context) -> dict:
    print("Start 'decorate_input_file' function...")
    print(f"Input: {input}")
    input_file_pointer = input["input_file_pointer"]

    labels_json = input["labels_json"]
    
    added_labels = context.add_labels(
        file=input_file_pointer,
        labels=labels_json,
    )
    print(f"Added labels: {added_labels}")

    print("'decorate_input_file' completed")
    return input_file_pointer