# src/pipeline.py
import pandas as pd
from loader import prepare_dataframe
from scraper_cfm import fetch_from_cfm

def enrich():
    df = prepare_dataframe()
    for idx, row in df.iterrows():
        crm, uf = row["CRM"], row["UF"]
        try:
            result = fetch_from_cfm(crm, uf)
            for k, v in result.items():
                if k in df.columns:
                    df.at[idx, k] = v
        except Exception as e:
            print(f"[ERRO] CRM={crm} UF={uf}: {e}")
    df.to_csv("../data/Lote_HP001_enriquecido.csv", index=False)

if __name__ == "__main__":
    enrich()
    print("Enriquecimento CFM concluído.")
ww