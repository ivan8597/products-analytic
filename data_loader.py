from dataclasses import dataclass

import pandas as pd

from config import ORDERS_FILE, PRODUCTS_FILE


@dataclass
class DataBundle:
    products: pd.DataFrame
    orders: pd.DataFrame
    merged: pd.DataFrame


def load_products() -> pd.DataFrame:
    return pd.read_excel(PRODUCTS_FILE)


def load_orders() -> pd.DataFrame:
    return pd.read_excel(ORDERS_FILE)


def enrich_orders(orders: pd.DataFrame) -> pd.DataFrame:
    enriched = orders.copy()
    enriched["line_total"] = enriched["price"] * enriched["quantity"]
    return enriched


def enrich_merged(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["revenue"] = enriched["price"] * enriched["quantity"]
    enriched["cost"] = enriched["cost_price"] * enriched["quantity"]
    enriched["margin_rub"] = enriched["revenue"] - enriched["cost"]
    return enriched


def load_data() -> DataBundle:
    products = load_products()
    orders = enrich_orders(load_orders())
    merged = enrich_merged(orders.merge(products, on="product_id", how="inner"))
    return DataBundle(products=products, orders=orders, merged=merged)
