import os
import numpy as np
import pandas as pd


def main():
    os.makedirs("data/raw_generic", exist_ok=True)

    rng = np.random.default_rng(42)
    n = 2000
    t = np.arange(n)

    x = 640 + np.cumsum(rng.normal(0, 0.8, n))
    y = 360 + np.cumsum(rng.normal(0, 0.5, n))
    pupil = 3.5 + 0.05 * rng.normal(size=n)
    confidence = np.clip(0.95 + 0.03 * rng.normal(size=n), 0.0, 1.0)

    missing_idx = rng.choice(n, size=50, replace=False)
    x[missing_idx] = np.nan
    y[missing_idx] = np.nan
    pupil[missing_idx] = 0.0
    confidence[missing_idx] = 0.1

    df = pd.DataFrame({
        "timestamp": t,
        "x": x,
        "y": y,
        "pupil": pupil,
        "confidence": confidence,
        "trial": 1,
    })

    out_path = "data/raw_generic/samples.csv"
    df.to_csv(out_path, index=False)
    print(f"saved to {out_path}")
    print(df.head())
    print(df.isna().sum())


if __name__ == "__main__":
    main()
