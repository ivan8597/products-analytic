import matplotlib.pyplot as plt
import pandas as pd

from config import CHART_COLORS, PROMO_CATEGORY
from data_loader import DataBundle
from utils import save_csv, save_figure, setup_matplotlib


def compute(df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    cheese = df[df["level1"] == PROMO_CATEGORY].copy()
    cheese["is_promo"] = cheese["regular_price"] != cheese["price"]
    promo_qty = int(cheese.loc[cheese["is_promo"], "quantity"].sum())
    regular_qty = int(cheese.loc[~cheese["is_promo"], "quantity"].sum())
    total = promo_qty + regular_qty
    promo_share = promo_qty / total * 100 if total else 0.0

    table = pd.DataFrame(
        {
            "Тип продажи": ["Промо", "Регулярная цена"],
            "Продано, шт.": [promo_qty, regular_qty],
            "Доля, %": [round(promo_share, 2), round(100 - promo_share, 2)],
        }
    )
    return table, promo_share


def plot(promo_qty: int, regular_qty: int, promo_share: float) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 6))
    labels = [
        f"Промо\n{promo_qty} шт. ({promo_share:.1f}%)",
        f"Регулярная цена\n{regular_qty} шт. ({100 - promo_share:.1f}%)",
    ]
    ax.pie(
        [promo_qty, regular_qty],
        labels=labels,
        colors=[CHART_COLORS["promo"], CHART_COLORS["regular"]],
        autopct="",
        startangle=90,
        textprops={"fontsize": 11},
    )
    ax.set_title(f"Доля промо-продаж в категории «{PROMO_CATEGORY}» (в штуках)")
    fig.tight_layout()
    return fig


def run(bundle: DataBundle) -> dict:
    setup_matplotlib()
    table, promo_share = compute(bundle.merged)
    promo_qty = int(table.loc[table["Тип продажи"] == "Промо", "Продано, шт."].iloc[0])
    regular_qty = int(table.loc[table["Тип продажи"] == "Регулярная цена", "Продано, шт."].iloc[0])
    save_csv(table, "4_cheese_promo_share.csv")
    save_figure(plot(promo_qty, regular_qty, promo_share), "4_cheese_promo_pie.png")
    return {
        "table": table,
        "promo_share": promo_share,
        "promo_qty": promo_qty,
        "total_qty": promo_qty + regular_qty,
    }
