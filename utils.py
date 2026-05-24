from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import MPL_CONFIG, OUTPUT_DIR


def setup_matplotlib() -> None:
    plt.rcParams.update(MPL_CONFIG)


def abc_classify(values: pd.Series, a_threshold: float = 80, b_threshold: float = 95) -> pd.Series:
    ordered = values.sort_values(ascending=False)
    cumulative_pct = ordered.cumsum() / ordered.sum() * 100
    classes = pd.Series(index=ordered.index, dtype=str)
    classes[cumulative_pct <= a_threshold] = "A"
    classes[(cumulative_pct > a_threshold) & (cumulative_pct <= b_threshold)] = "B"
    classes[cumulative_pct > b_threshold] = "C"
    return classes


def save_csv(df: pd.DataFrame, filename: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    df.to_csv(path, index=False)
    return path


def save_figure(fig: plt.Figure, filename: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path
