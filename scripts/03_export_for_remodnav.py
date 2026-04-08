import os
import pandas as pd


def main():
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/events", exist_ok=True)

    df = pd.read_csv("data/raw_generic/samples.csv")
    xy = df[["x", "y"]].copy()

    out_path = "data/processed/remodnav_input.tsv"
    xy.to_csv(out_path, sep="\t", header=False, index=False)

    print(f"saved to {out_path}")
    print(xy.head())


if __name__ == "__main__":
    main()
