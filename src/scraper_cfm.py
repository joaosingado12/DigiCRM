# src/scraper_cfm.py
"""
Scraper baseado nos endpoints internos do portal.cfm.org.br
Etapas:
1. POST /buscar_medicos   -> retorna lista (id, CRM, UF, nome resumido…)
2. POST /buscar_medico    -> retorna detalhe completo a partir do ID_PESSOA
"""

import requests
from typing import Dict

URL_SEARCH  = "https://portal.cfm.org.br/api_rest_php/api/v1/medicos/buscar_medicos"
URL_DETAIL  = "https://portal.cfm.org.br/api_rest_php/api/v1/medicos/buscar_medico"

HEADERS: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://portal.cfm.org.br",
    "Referer": "https://portal.cfm.org.br/busca-medicos",
}

def _payload_search(crm: str, uf: str) -> Dict[str, str]:
    """Payload igual ao do formulário (campos vazios onde não usamos)."""
    return {
        "captcha": "",
        "medico[nome]": "",
        "medico[ufMedico]": uf,
        "medico[crmMedico]": crm,
        "medico[municipioMedico]": "",
        "medico[tipoInscricaoMedico]": "",
        "medico[situacaoMedico]": "",
        "medico[detalheSituacaoMedico]": "",
        "medico[especialidadeMedico]": "",
        "medico[areaAtuacaoMedico]": "",
        "page": 1,
        "pageNumber": 1,
        "pageSize": 10,
    }

def fetch_from_cfm(crm: str, uf: str) -> Dict[str, str]:
    """
    Retorna um dict padronizado com dados vindos do portal CFM.
    Pode devolver {} se não encontrar ou em caso de bloqueio.
    """
    # 1) busca mínima
    r = requests.post(URL_SEARCH, headers=HEADERS, data=_payload_search(crm, uf), timeout=15)
    r.raise_for_status()
    js = r.json()
    dados = js.get("dados", [])
    if not dados:
        return {}

    id_pessoa = dados[0].get("ID_PESSOA")
    if not id_pessoa:
        return {}

    # 2) detalhe completo
    r2 = requests.post(URL_DETAIL, headers=HEADERS, data={"idPessoa": id_pessoa}, timeout=15)
    r2.raise_for_status()
    det = r2.json().get("dados", {})
    if not det:
        return {}

    # 3) normaliza ⇢ sempre caixa‑alta no portal → uso .title() p/ nome
    return {
        "Official Name":      det.get("NM_MEDICO", "").title(),
        "Medical specialty":  det.get("DS_ESPECIALIDADE", ""),
        "City A1":            det.get("NM_MUNICIPIO", ""),
        "State A1":           det.get("SG_UF", ""),
        "Phone A1":           det.get("NR_TELEFONE", ""),      # raramente preenchido
    }

if __name__ == "__main__":
    print(fetch_from_cfm("97502", "SP"))   # teste
