# src/scraper_cfm.py
import requests

# 1) busca rápida p/ pegar o código interno do médico
URL_SEARCH = "https://portal.cfm.org.br/api_rest_php/api/v1/medicos/buscar_medicos"
# 2) detalhe do médico (usa o idCodMedico retornado no passo 1)
URL_DETAIL = "https://portal.cfm.org.br/api_rest_php/api/v1/medicos/buscar_medico"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

def _payload(crm: str, uf: str) -> dict:
    """Form‑data que o portal envia. Campos vazios podem ficar em branco."""
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

def fetch_from_cfm(crm: str, uf: str) -> dict:
    # ---------- 1) busca mínima ----------
    r = requests.post(URL_SEARCH, data=_payload(crm, uf), headers=HEADERS, timeout=15)
    r.raise_for_status()
    resp = r.json()
    if not resp.get("dados"):
        return {}                         # CRM inexistente
    codigo = resp["dados"][0]["ID_PESSOA"]

    # ---------- 2) detalhe ----------
    r_det = requests.post(URL_DETAIL, data={"idPessoa": codigo}, headers=HEADERS, timeout=15)
    r_det.raise_for_status()
    det = r_det.json().get("dados", {})
    if not det:
        return {}

    # ---------- 3) padroniza campos ----------
    return {
        "Official Name":  det.get("NM_MEDICO", "").title(),
        "Medical specialty": det.get("DS_ESPECIALIDADE", ""),
        "City A1":  det.get("NM_MUNICIPIO", ""),
        "State A1": det.get("SG_UF", ""),
        # telefone/endereço costumam vir vazios, mas deixamos a chave
        "Phone A1": det.get("NR_TELEFONE", ""),
    }

if __name__ == "__main__":
    print(fetch_from_cfm("97502", "SP"))
