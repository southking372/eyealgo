import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    in_path = "data/processed/pupeyes_samples.csv"
    out_csv = "data/processed/pupeyes_samples_clean.csv"
    out_fig = "outputs/pupil_clean.png"

    df = pd.read_csv(in_path).copy()

    # 1) 原始瞳孔列
    raw_pp = df["pp"].astype(float).copy()

    # 2) 把 <= 0 的值视为无效
    invalid_mask = raw_pp <= 0
    raw_pp[invalid_mask] = np.nan

    # 3) 按时间插值
    # 先做线性插值，再补头尾
    interp_pp = raw_pp.interpolate(method="linear", limit_direction="both")

    # 4) 轻量平滑：滚动中值 + 滚动均值
    smooth_pp = (
        interp_pp
        .rolling(window=5, center=True, min_periods=1).median()
        .rolling(window=5, center=True, min_periods=1).mean()
    )

    # 5) 保存结果
    df["pp_raw"] = df["pp"]
    df["pp_invalid"] = invalid_mask.astype(int)
    df["pp_interp"] = interp_pp
    df["pp_clean"] = smooth_pp

    df.to_csv(out_csv, index=False)

    # 6) 画图
    plt.figure(figsize=(10, 4))
    plt.plot(df["trialtime"], df["pp_raw"], label="raw", alpha=0.6)
    plt.plot(df["trialtime"], df["pp_clean"], label="clean")
    plt.xlabel("time")
    plt.ylabel("pupil size")
    plt.title("Pupil cleaning result")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_fig, dpi=150)

    # 7) 打印摘要
    print(f"input : {in_path}")
    print(f"csv   : {out_csv}")
    print(f"fig   : {out_fig}")
    print()
    print("summary:")
    print("total samples      :", len(df))
    print("invalid pp count   :", int(invalid_mask.sum()))
    print("raw nan count      :", int(pd.isna(raw_pp).sum()))
    print("interp nan count   :", int(pd.isna(interp_pp).sum()))
    print("clean nan count    :", int(pd.isna(smooth_pp).sum()))
    print()
    print(df[["trialtime", "pp_raw", "pp_interp", "pp_clean", "pp_invalid"]].head(10))


if __name__ == "__main__":
    main()
