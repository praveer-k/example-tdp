from ts_sdk.task.__task_script_runner import Context
from task_script.print_hello_world import print_hello_world
from task_script.decorate_input_file import decorate_input_file
from task_script.push_data import push_data

def print_message(input: dict, context: Context):
    print_hello_world(input, context) 

def decorate(input: dict, context: Context):
    decorate_input_file(input, context)

def push(input: dict, context: Context):
    push_data(input, context)