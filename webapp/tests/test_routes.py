
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import createApp


def getClient():
    app = createApp()
    app.testing = True
    return app.test_client()


def test_home_page_loads():
    client = getClient()
    res = client.get("/")
    assert res.status_code == 200


def test_dashboard_page_loads():
    client = getClient()
    res = client.get("/dashboard")
    assert res.status_code == 200


def test_predict_endpoint_rejects_empty_prompt():
    client = getClient()
    res = client.post("/api/predict", json={"prompt": ""})
    assert res.status_code == 400
