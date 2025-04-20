# src/pipeline.py
import pandas as pd
from loader import prepare_dataframe
from scraper_cfm import fetch_from_cfm


# → chaves que vêm do scraper  |  → nome da coluna na planilha
MAP = {
    "Official Name":       "FullName",
    "Medical specialty":   "Medical specialty",
    "City A1":             "City A1",
    "State A1":            "State A1",
    "Phone A1":            "Phone A1",
}


def enrich() -> None:
    df = prepare_dataframe()

    # garante que todas as colunas‑destino existam
    for col in MAP.values():
        if col not in df.columns:
            df[col] = ""

    # percorre cada médico
    for idx, row in df.iterrows():
        crm, uf = row["CRM"], row["UF"]

        try:
            result = fetch_from_cfm(crm, uf)        # dict vindo do scraper

            # grava no DataFrame somente se vier valor
            for src_key, dst_col in MAP.items():
                value = result.get(src_key, "").strip()
                if value:
                    df.at[idx, dst_col] = value

        except Exception as e:
            print(f"[ERRO] CRM={crm} UF={uf}: {e}")

    # salva
    df.to_csv("data/Lote_HP001_enriquecido.csv", index=False)
    print("Enriquecimento CFM concluído – arquivo salvo em data/.")


if __name__ == "__main__":
    enrich()
