import matplotlib.pyplot as plt
import pandas as pd

from config import ANALYSIS_DATE_LABEL, CHART_COLORS
from data_loader import DataBundle
from utils import save_csv, save_figure, setup_matplotlib


def compute(df: pd.DataFrame) -> pd.DataFrame:
    margin = (
        df.groupby("level1")
        .agg(
            Выручка=("revenue", "sum"),
            Себестоимость=("cost", "sum"),
            Маржа_руб=("margin_rub", "sum"),
        )
        .reset_index()
        .rename(columns={"level1": "Категория"})
    )
    margin["Маржа_%"] = (margin["Маржа_руб"] / margin["Выручка"] * 100).round(2)
    return margin.sort_values("Маржа_руб", ascending=False)


def plot_rub(margin: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 8))
    plot_df = margin.sort_values("Маржа_руб")
    bars = ax.barh(plot_df["Категория"], plot_df["Маржа_руб"], color=CHART_COLORS["green"])
    ax.set_xlabel("Маржа, руб.")
    ax.set_ylabel("Товарная категория (level1)")
    ax.set_title(f"Маржа по категориям, руб., {ANALYSIS_DATE_LABEL}")
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 150,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,}".replace(",", " "),
            va="center",
            fontsize=7,
        )
    fig.tight_layout()
    return fig


def plot_pct(margin: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 8))
    plot_df = margin.sort_values("Маржа_%")
    bars = ax.barh(plot_df["Категория"], plot_df["Маржа_%"], color=CHART_COLORS["purple"])
    ax.set_xlabel("Маржа, % от выручки")
    ax.set_ylabel("Товарная категория (level1)")
    ax.set_title(f"Маржа по категориям, %, {ANALYSIS_DATE_LABEL}")
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height() / 2, f"{width:.1f}%", va="center", fontsize=7)
    fig.tight_layout()
    return fig


def run(bundle: DataBundle) -> dict:
    setup_matplotlib()
    margin = compute(bundle.merged)
    save_csv(margin, "5_margin_by_category.csv")
    save_figure(plot_rub(margin), "5_margin_rub.png")
    save_figure(plot_pct(margin), "5_margin_pct.png")
    return {"table": margin}
