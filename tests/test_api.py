def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Motor de IA Agrícola Operativo"}

def test_predict_from_coords(client):
    # Simulamos coordenadas dentro de Palmira
    payload = {
        "cultivo": "cafe",
        "lat": 3.51,
        "lon": -76.25
    }
    response = client.post("/api/predict_from_coords", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["cultivo"] == "cafe"
    assert "final_score" in data
    assert "aptitud_label" in data
    assert data["municipio_detectado"] == "Palmira"
