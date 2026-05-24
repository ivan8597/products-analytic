from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "output"

PRODUCTS_FILE = DATA_DIR / "products.xlsx"
ORDERS_FILE = DATA_DIR / "orders.xlsx"

ANALYSIS_DATE = "2022-01-13"
ANALYSIS_DATE_LABEL = "13.01.2022"
PROMO_CATEGORY = "Сыры"

ABC_THRESHOLDS = {"A": 80, "B": 95}

MPL_CONFIG = {
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 150,
}

CHART_COLORS = {
    "blue": "#4C78A8",
    "green": "#54A24B",
    "purple": "#B279A2",
    "promo": "#E45756",
    "regular": "#72B7B2",
}
