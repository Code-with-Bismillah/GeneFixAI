from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_detect_mutations():
    response = client.post("/mutation_detection/detect", json={"sequence": "ATCGATCGATCGATCGATCGATCGATCGATCG"})
    assert response.status_code == 200
    assert "mutations" in response.json()

def test_design_guides():
    seq = "A"*20 + "TGG" + "C"*10
    response = client.post("/design_guides", json={"target_sequence": seq})
    assert response.status_code == 200
    assert "guides" in response.json()
