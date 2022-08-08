import pytest

from client.client_utils import generate_verification_msg, verify_username

verify_username_test_data = [
    ("normal", 0),
    ("no", 1),
    ("normalooooooooooooooo", 2),
    ("1normal", 3),
    ("nor~", 4),
]

generate_verification_msg_test_data = [
    (0, "Username OK"),
    (1, "Username too short"),
    (2, "Username too long"),
    (3, "Username has to start with letter"),
    (4, "Username contains restricted characters"),
]


@pytest.mark.parametrize("input, expected", verify_username_test_data)
def test_verify_username_uname(input, expected):
    assert verify_username(input) == expected


@pytest.mark.parametrize("input, expected", generate_verification_msg_test_data)
def test_generate_verification_msg(input, expected):
    assert generate_verification_msg(input) == expected
