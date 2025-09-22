from src.auth import auth


def test_auth():
    result = auth(end_user_ip="0.0.0.0", personal_number="197801010000")
    assert result
