import pytest
from src.backend.services.gis_service import normalize_text

def test_normalize_text():
    # Verifica que quite tildes y lo ponga en mayúscula
    assert normalize_text("Tuluá") == "TULUA"
    assert normalize_text("BUGÁ") == "BUGA"
    
    # Verifica que no afecte texto normal salvo mayúscula
    assert normalize_text("Palmira") == "PALMIRA"
    
    # Verifica que quite eñes o caracteres raros y los convierta
    assert normalize_text("Caña") == "CANA"
    
    # Verifica que limpie espacios innecesarios
    assert normalize_text(" Buenaventura  ") == "BUENAVENTURA"
