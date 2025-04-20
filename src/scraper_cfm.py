# src/scraper_cfm.py
import requests

API = "https://www.consultacrm.com.br/api/index.php"

def fetch_from_cfm(crm: str, uf: str) -> dict:
    """Retorna nome, especialidade, cidade e UF a partir de CRM+UF."""
    r = requests.get(API, params={
        "tipo": "crm",
        "crm": crm,
        "uf": uf,
        "destino": "json"
    }, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data or data[0]["situacao"] == "INEXISTENTE":
        return {}

    row = data[0]
    return {
        "Official Name":      row.get("nome", "").title(),
        "Medical specialty":  row.get("especialidade", ""),
        "City A1":            row.get("cidade", ""),
        "State A1":           row.get("uf", ""),
        # telefone não vem; deixa vazio
    }

if __name__ == "__main__":
    print(fetch_from_cfm("97502", "SP"))
