import os
import pandas as pd


def main():
    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_csv("data/raw_generic/samples.csv")

    out = pd.DataFrame({
        "participant": 1,
        "block": 1,
        "trial": df["trial"],
        "event": "task",
        "trialtime": df["timestamp"],
        "x": df["x"],
        "y": df["y"],
        "pp": df["pupil"],
    })

    out_path = "data/processed/pupeyes_samples.csv"
    out.to_csv(out_path, index=False)

    print(f"saved to {out_path}")
    print(out.head())
    print("\nmissing values:")
    print(out.isna().sum())


if __name__ == "__main__":
    main()
