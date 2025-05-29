# Run the tests with: pytest tests/test_app.py
def add_numbers(x: int, y: int):
    return x + y

def test_add_numbers():
    assert 3 == add_numbers(1,2)
