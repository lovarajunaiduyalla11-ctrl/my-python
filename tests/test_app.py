from app import app

def test_index_status_code():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"My Example Site" in resp.data or b"Hello" in resp.data
