from dataclasses import dataclass

import pandas as pd

from data_loader import load_data
from tasks.task1_category_sales import compute as compute_category_sales
from tasks.task2_subcategories import compute as compute_subcategories
from tasks.task3_average_check import compute as compute_average_check
from tasks.task4_promo_share import compute as compute_promo_share
from tasks.task5_margin import compute as compute_margin
from tasks.task6_abc_analysis import compute as compute_abc


@dataclass
class DashboardData:
    cat_qty: pd.DataFrame
    subcat: pd.DataFrame
    avg_check: float
    check_count: int
    promo: pd.DataFrame
    promo_share: float
    margin: pd.DataFrame
    abc: pd.DataFrame
    categories: list[str]


def load_dashboard_data() -> DashboardData:
    bundle = load_data()

    cat_qty = compute_category_sales(bundle.merged)
    subcat = compute_subcategories(bundle.merged)
    check = compute_average_check(bundle.orders)
    promo, promo_share = compute_promo_share(bundle.merged)
    margin = compute_margin(bundle.merged)
    abc = compute_abc(bundle.merged)

    return DashboardData(
        cat_qty=cat_qty,
        subcat=subcat,
        avg_check=check["avg_check"],
        check_count=check["check_count"],
        promo=promo,
        promo_share=promo_share,
        margin=margin,
        abc=abc,
        categories=sorted(subcat["Категория"].unique()),
    )
