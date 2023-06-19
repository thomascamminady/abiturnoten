import glob
import os
import numpy as np

import pandas as pd

if __name__ == "__main__":
    df_list = []
    files = glob.glob("data/*.xls") + glob.glob("data/*.xlsx")

    for file in files:
        df = pd.read_excel(
            file, sheet_name="Noten", skiprows=[1, 2, 3, 5, 6, 7, 8, 9, 10]
        )
        new_header = df.iloc[0]  # grab the first row for the header
        df = df[1:]  # take the data less the header row
        df.columns = new_header  # set the header row as the df header
        df.rename(columns={"Land": "Note"}, inplace=True)
        year = int(os.path.basename(file).split(".")[0].split("_")[-1])
        df["Jahr"] = year

        # For some reason, the 2013 results of SN are parsed as floats??
        if year == 2013:
            df["SN"] = df["SN"].astype(float).round().astype(int)

        if year == 2022:
            df = df[:-1]  # Drop footer in 2022 data.

        df_list.append(df)

    df = pd.concat(df_list)
    df = pd.melt(
        df,
        id_vars=["Jahr", "Note"],
        value_vars=[c for c in df.columns if c != "Jahr" and c != "Note"],
        value_name="Anzahl",
        var_name="Bundesland",
    ).sort_values(["Jahr", "Bundesland", "Note"])

    df.to_csv("data/Abiturnoten.csv", index=False)
