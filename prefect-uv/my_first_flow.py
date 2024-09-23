from prefect import task, flow

@task
def say_hello(name):
    print(f"Hello, {name}!")

@task
def add_numbers(x, y):
    return x + y

@task
def display_result(result):
    print(f"The result is {result}")

@flow
def my_parameterized_flow(name: str = "World", x: int = 5, y: int = 7):
    say_hello(name)
    result = add_numbers(x, y)
    display_result(result)

if __name__ == "__main__":
    my_parameterized_flow(name="Oliver", x=10, y=20)