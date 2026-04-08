import os
import pandas as pd
import matplotlib.pyplot as plt


def main():
    os.makedirs("outputs", exist_ok=True)

    df = pd.read_csv("data/processed/pupeyes_samples.csv")

    print(df.head())
    print("\nshape:", df.shape)
    print("pp missing:", df["pp"].isna().sum())
    print("x missing :", df["x"].isna().sum())
    print("y missing :", df["y"].isna().sum())

    plt.figure(figsize=(10, 4))
    plt.plot(df["trialtime"], df["pp"])
    plt.xlabel("time")
    plt.ylabel("pupil size")
    plt.title("Raw pupil trace")
    plt.tight_layout()

    out_path = "outputs/pupil_raw.png"
    plt.savefig(out_path, dpi=150)
    print(f"saved figure to {out_path}")


if __name__ == "__main__":
    main()
