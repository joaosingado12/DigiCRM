# src/loader.py
import pandas as pd

INPUT = "data/Lote_HP001.csv"
OUTPUT = "data/Lote_HP001_enriquecido.csv"

def prepare_dataframe():
    df = pd.read_csv(INPUT, dtype=str)
    # garante que as colunas já existam
    new_cols = [
      "Medical specialty","Address A1","Complement A1","postal code A1",
      "City A1","State A1","Phone A1","Phone A2",
      "Cell phone A1","Cell phone A2","E-mail A1","E-mail A2"
    ]
    for col in new_cols:
        if col not in df.columns:
            df[col] = ""
    return df

if __name__ == "__main__":
    df = prepare_dataframe()
    print(df.head(3))
    df.to_csv(OUTPUT, index=False)
    print(f"Planilha preparada em: {OUTPUT}")

vai tomar no cuzinho, pode ser?
