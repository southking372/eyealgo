# 👁️eyealgo

> 一个逐步搭建的眼动处理与瞳孔检测实验仓库。  
> 当前已经跑通两条主线：**数值层眼动处理链**与**图像层真实瞳孔检测链**。

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Platform](https://img.shields.io/badge/Platform-HPC-green)
![Status](https://img.shields.io/badge/Status-Running-success)
![Scope](https://img.shields.io/badge/Scope-Eye%20Tracking%20%26%20Pupil%20Detection-purple)

---

## ✨项目简介

这个仓库用于管理一套从**原始eye camera视频**到**瞳孔检测结果**，以及从**眼动数值数据**到**事件检测与瞳孔预处理**的实验流程。

目前已经完成：

- ✅`pymovements`公开数据读取、预处理与基础事件检测
- ✅`REMoDNaV`规则法事件检测
- ✅瞳孔时间序列基础清洗与可视化
- ✅`LPW`真实眼区视频读取
- ✅`EllSeg`推理与真实瞳孔overlay视频生成

仓库已经覆盖了两类任务：

### 1. 数值层处理链

```text
ToyDataset / generic CSV
-> gaze preprocessing
-> event detection
-> pupil preprocessing
```

### 2. 图像层处理链

```text
raw eye video
-> pupil segmentation / ellipse fitting
-> overlay video
```

---

## 🧭仓库结构

```text
eyealgo/
├── scripts/                     # 主要脚本
├── notebooks/                   # 交互式分析notebook
├── external/
│   └── EllSeg/                  # 引入的瞳孔分割模型代码
├── data/
│   ├── raw_public/              # 公开示例数据
│   ├── raw_generic/             # 自定义统一格式示例数据
│   ├── raw_eye_videos/          # 原始眼区视频
│   ├── processed/               # 中间处理结果
│   └── events/                  # 事件检测输出
├── outputs/                     # 图像与可视化输出
├── environment_eye_hpc.yml      # conda环境导出
├── requirements_eye_hpc.txt     # pip依赖快照
└── README.md
```

> 注：大体积数据、视频、输出图等默认不纳入Git版本管理。

---

## 🔬当前已跑通的流程

### A. `pymovements`公开数据链

```text
ToyDataset
-> pix2deg
-> pos2vel
-> IVT事件检测
```

### B. `REMoDNaV`事件检测链

```text
generic samples.csv
-> 导出x,y
-> remodnav
-> events.tsv
```

### C. 瞳孔时间序列链

```text
generic samples.csv
-> 原始瞳孔曲线
-> 无效值处理
-> 插值
-> 平滑
-> clean pupil trace
```

### D. 真实瞳孔图像链

```text
LPW eye video
-> ffmpeg转码
-> EllSeg推理
-> 生成eye0_ellseg.mp4
```

---

## ⚙️环境配置

推荐使用独立conda环境：

```bash
conda create -n eye-hpc python=3.10 -y
source ~/miniconda3/etc/profile.d/conda.sh
conda activate eye-hpc
export PYTHONNOUSERSITE=1
```

安装基础依赖：

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install pymovements remodnav pupeyes pandas pyarrow matplotlib jupyter
python -m pip install opencv-python torch torchvision scipy h5py scikit-image tqdm
```

---

## 🚀快速开始

### 1. 跑通`pymovements`

```bash
python -u scripts/01_run_pymovements.py
```

### 2. 生成统一格式示例数据

```bash
python -u scripts/02_make_generic_csv.py
```

### 3. 导出并运行`REMoDNaV`

```bash
python -u scripts/03_export_for_remodnav.py
remodnav data/processed/remodnav_input.tsv data/events/remodnav_events.tsv 0.03 1000
```

### 4. 生成原始瞳孔曲线与清洗结果

```bash
python -u scripts/04_prepare_pupeyes_csv.py
python -u scripts/05_plot_pupil_basic.py
python -u scripts/06_clean_pupil_basic.py
```

### 5. 运行EllSeg生成真实瞳孔检测视频

```bash
cd external/EllSeg
export CUDA_VISIBLE_DEVICES=""

python -u evaluate_ellseg.py \
  --path2data "$HOME/eyealgo/data/ellseg_demo" \
  --save_overlay 1 \
  --ellseg_ellipses 0 \
  --eval_on_cpu 1
```

---

## 🖼️当前主要输出

### 数值层输出

- `data/events/remodnav_events.tsv`
- `outputs/pupil_raw.png`
- `outputs/pupil_clean.png`
- `data/processed/pupeyes_samples_clean.csv`

### 图像层输出

- `data/ellseg_demo/exp0/eye0.mp4`
- `data/ellseg_demo/exp0/eye0_ellseg.mp4`

---

## 🧪关键脚本说明

| 脚本 | 作用 |
|---|---|
| `scripts/01_run_pymovements.py` | 跑通ToyDataset与基础事件检测 |
| `scripts/02_make_generic_csv.py` | 构造统一格式的示例眼动数据 |
| `scripts/03_export_for_remodnav.py` | 导出REMoDNaV输入格式 |
| `scripts/04_prepare_pupeyes_csv.py` | 整理瞳孔数据表 |
| `scripts/05_plot_pupil_basic.py` | 绘制原始瞳孔曲线 |
| `scripts/06_clean_pupil_basic.py` | 基础瞳孔清洗与平滑 |
| `external/EllSeg/evaluate_ellseg.py` | EllSeg推理入口 |

---


## 📍后续施工方向

- 更稳健的真实瞳孔检测与椭圆拟合
- 眼动事件深度学习模型，如U'n'Eye
- 眼动+瞳孔+IMU联合建模
- 对真实眼镜设备数据编写转换脚本
- 增加更多可视化，如scanpath、heatmap、局部瞳孔片段分析

---

## 🤝备注

该仓库当前以研究开发为主，侧重：

- 快速复现实验
- 分层打通软件链
- 便于后续接入真实硬件数据

如果你正在做类似的眼动或瞳孔检测实验，这个仓库可以作为一个轻量级起点。
