import pytest
from httpx import AsyncClient, ASGITransport

def func():
    return "test is working"

def test_func():
    assert func() == "test is working"
