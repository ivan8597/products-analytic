import matplotlib.pyplot as plt
import pandas as pd

from config import ANALYSIS_DATE_LABEL, CHART_COLORS
from data_loader import DataBundle
from utils import save_csv, save_figure, setup_matplotlib


def compute(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("level1")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"level1": "Категория", "quantity": "Продано, шт."})
    )


def plot(cat_qty: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 7))
    plot_df = cat_qty.sort_values("Продано, шт.")
    bars = ax.barh(plot_df["Категория"], plot_df["Продано, шт."], color=CHART_COLORS["blue"])
    ax.set_xlabel("Количество проданных единиц, шт.")
    ax.set_ylabel("Товарная категория (level1)")
    ax.set_title(f"Продажи по товарным категориям, {ANALYSIS_DATE_LABEL}")
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 3, bar.get_y() + bar.get_height() / 2, f"{int(width)}", va="center", fontsize=8)
    fig.tight_layout()
    return fig


def run(bundle: DataBundle) -> dict:
    setup_matplotlib()
    cat_qty = compute(bundle.merged)
    save_csv(cat_qty, "1_sales_by_category.csv")
    save_figure(plot(cat_qty), "1_sales_by_category.png")
    return {
        "table": cat_qty,
        "leader": cat_qty.iloc[0]["Категория"],
        "leader_qty": int(cat_qty.iloc[0]["Продано, шт."]),
    }
