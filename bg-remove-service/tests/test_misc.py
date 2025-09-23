from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def func(num: int = 2) -> int:
    return 4/num

def test_func():
    assert func() == 2
    assert func(3) != 2
    assert func(2) == 2
    try:
        func(0)
    except ZeroDivisionError:
        assert True
    else:
        assert False

