import pandas as pd

from data_loader import DataBundle
from utils import save_csv


def compute(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["level1", "level2"])["quantity"]
        .sum()
        .reset_index()
        .rename(columns={"level1": "Категория", "level2": "Подкатегория", "quantity": "Продано, шт."})
        .sort_values(["Категория", "Продано, шт."], ascending=[True, False])
    )


def run(bundle: DataBundle) -> dict:
    subcat = compute(bundle.merged)
    save_csv(subcat, "2_sales_by_subcategory.csv")
    return {"table": subcat}
