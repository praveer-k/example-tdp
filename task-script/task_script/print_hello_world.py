from ts_sdk.task.__task_script_runner import Context

# The actual function we are using and testing
def print_hello_world(input: dict, context: Context):
    print("Hello World!")
    return "Hello World!"

