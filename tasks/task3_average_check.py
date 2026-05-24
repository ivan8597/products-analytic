import pandas as pd

from config import ANALYSIS_DATE, ANALYSIS_DATE_LABEL
from data_loader import DataBundle
from utils import save_csv


def compute(orders: pd.DataFrame) -> dict:
    target_date = pd.Timestamp(ANALYSIS_DATE).date()
    day_orders = orders[orders["accepted_at"].dt.date == target_date]
    check_totals = day_orders.groupby("order_id")["line_total"].sum()
    return {
        "avg_check": float(check_totals.mean()),
        "check_count": len(check_totals),
    }


def run(bundle: DataBundle) -> dict:
    result = compute(bundle.orders)
    table = pd.DataFrame(
        {
            "Дата": [ANALYSIS_DATE_LABEL],
            "Количество чеков": [result["check_count"]],
            "Средний чек, руб.": [round(result["avg_check"], 2)],
        }
    )
    save_csv(table, "3_average_check.csv")
    return {"table": table, **result}
