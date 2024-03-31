from task_script.print_hello_world import print_hello_world

def test_hello_world():
    output = print_hello_world(input={}, context={})
    assert output == "Hello World!"