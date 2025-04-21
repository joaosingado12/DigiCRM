# src/scraper_cfm.py
from typing import Dict
import cloudscraper

API     = "https://www.consultacrm.com.br/api/index.php"
API_KEY = "9601599027"            # sua chave

scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "linux", "mobile": False}
)

def fetch_from_cfm(crm: str, uf: str) -> Dict[str, str]:
    """Busca (crm, uf) na API ConsultaCRM e devolve dict padronizado."""
    params = {
        "tipo":    "crm",
        "q":       crm,          # campo correto
        "uf":      uf,
        "destino": "json",
        "chave":   API_KEY,
    }

    try:
        r = scraper.get(API, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()                         # sempre parsear
    except Exception:
        return {}

    # data = {"url":..., "total":..., "status":"true/false", "item":[ {...} ]}
    itens = data.get("item")
    if not itens:
        return {}

    d = itens[0]                               # primeiro resultado

    return {
        "Official Name":     d.get("nome", "").title(),
        "Medical specialty": d.get("profissao", ""),
        "City A1":           "",                # API não traz cidade
        "State A1":          d.get("uf", ""),
        "Phone A1":          "",
    }

if __name__ == "__main__":
    print(fetch_from_cfm("97502", "SP"))
