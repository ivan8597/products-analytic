import pandas as pd

from data_loader import DataBundle
from utils import abc_classify, save_csv


def compute(df: pd.DataFrame) -> pd.DataFrame:
    abc = (
        df.groupby(["level1", "level2"])
        .agg(
            Продано_шт=("quantity", "sum"),
            Выручка_руб=("revenue", "sum"),
        )
        .reset_index()
    )
    abc["Подкатегория"] = abc["level1"] + " / " + abc["level2"]
    abc["ABC_по_количеству"] = abc_classify(abc["Продано_шт"]).values
    abc["ABC_по_выручке"] = abc_classify(abc["Выручка_руб"]).values
    abc["Итоговая_группа"] = abc["ABC_по_количеству"] + " " + abc["ABC_по_выручке"]
    abc = abc.sort_values("Выручка_руб", ascending=False)
    return abc[
        [
            "level1",
            "level2",
            "Подкатегория",
            "Продано_шт",
            "Выручка_руб",
            "ABC_по_количеству",
            "ABC_по_выручке",
            "Итоговая_группа",
        ]
    ].rename(columns={"level1": "Категория", "level2": "Подкатегория (level2)"})


def run(bundle: DataBundle) -> dict:
    abc = compute(bundle.merged)
    save_csv(abc, "6_abc_subcategories.csv")
    return {"table": abc}
