import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

from dashboard.data import DashboardData
from dashboard.figures import (
    category_sales_figure,
    margin_pct_figure,
    margin_rub_figure,
    promo_pie_figure,
    subcategory_figure,
)


def _kpi_card(title: str, value: str, subtitle: str) -> dbc.Col:
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.P(title, className="text-muted mb-1 small"),
                    html.H4(value, className="mb-1"),
                    html.P(subtitle, className="text-muted mb-0 small"),
                ]
            ),
            className="h-100 shadow-sm",
        ),
        md=4,
        xs=12,
    )


def _table(df, page_size: int = 10) -> dash_table.DataTable:
    return dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": col, "id": col} for col in df.columns],
        page_size=page_size,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "8px", "fontSize": 13},
        style_header={"fontWeight": "600", "backgroundColor": "#f8f9fa"},
    )


def build_layout(data: DashboardData) -> dbc.Container:
    default_category = data.cat_qty.iloc[0]["Категория"]

    return dbc.Container(
        [
            html.H2("Аналитика продаж", className="mt-4 mb-1"),
            html.P(
                "Данные за 13.01.2022 · orders.xlsx + products.xlsx",
                className="text-muted mb-4",
            ),
            dbc.Row(
                [
                    _kpi_card(
                        "Лидер по штукам",
                        data.cat_qty.iloc[0]["Категория"],
                        f"{data.cat_qty.iloc[0]['Продано, шт.']} проданных единиц",
                    ),
                    _kpi_card(
                        "Средний чек",
                        f"{data.avg_check:,.2f} ₽".replace(",", " "),
                        f"{data.check_count} чеков за день",
                    ),
                    _kpi_card(
                        "Промо в «Сыры»",
                        f"{data.promo_share:.1f}%",
                        f"{int(data.promo.loc[0, 'Продано, шт.'])} из {int(data.promo['Продано, шт.'].sum())} шт.",
                    ),
                ],
                className="g-3 mb-4",
            ),
            dbc.Card(
                [
                    dbc.CardHeader("1. Продажи по категориям"),
                    dbc.CardBody(
                        [
                            dcc.Graph(figure=category_sales_figure(data.cat_qty)),
                            html.H6("Таблица", className="mt-3 mb-2"),
                            _table(data.cat_qty, page_size=15),
                        ]
                    ),
                ],
                className="mb-4 shadow-sm",
            ),
            dbc.Card(
                [
                    dbc.CardHeader("2. Распределение по подкатегориям"),
                    dbc.CardBody(
                        [
                            html.Label("Выберите категорию (level1):", className="mb-2"),
                            dcc.Dropdown(
                                id="category-dropdown",
                                options=[{"label": c, "value": c} for c in data.categories],
                                value=default_category,
                                clearable=False,
                            ),
                            dcc.Graph(id="subcategory-chart"),
                            html.H6("Таблица", className="mt-3 mb-2"),
                            html.Div(id="subcategory-table"),
                        ]
                    ),
                ],
                className="mb-4 shadow-sm",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("4. Доля промо в категории «Сыры»"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(figure=promo_pie_figure(data.promo)),
                                        _table(data.promo, page_size=5),
                                    ]
                                ),
                            ],
                            className="shadow-sm h-100",
                        ),
                        md=5,
                        xs=12,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("5. Маржа по категориям"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(figure=margin_rub_figure(data.margin)),
                                        dcc.Graph(figure=margin_pct_figure(data.margin)),
                                    ]
                                ),
                            ],
                            className="shadow-sm h-100",
                        ),
                        md=7,
                        xs=12,
                    ),
                ],
                className="g-3 mb-4",
            ),
            dbc.Card(
                [
                    dbc.CardHeader("6. ABC-анализ по подкатегориям"),
                    dbc.CardBody(
                        [
                            html.P(
                                "Границы: A — до 80% накопленной доли, B — 80–95%, C — остальное. "
                                "Итоговая группа: ABC по количеству + ABC по выручке.",
                                className="text-muted small",
                            ),
                            _table(
                                data.abc[
                                    [
                                        "Подкатегория",
                                        "Продано_шт",
                                        "Выручка_руб",
                                        "ABC_по_количеству",
                                        "ABC_по_выручке",
                                        "Итоговая_группа",
                                    ]
                                ].rename(
                                    columns={
                                        "Продано_шт": "Продано, шт.",
                                        "Выручка_руб": "Выручка, ₽",
                                        "ABC_по_количеству": "ABC (шт.)",
                                        "ABC_по_выручке": "ABC (₽)",
                                        "Итоговая_группа": "Группа",
                                    }
                                ),
                                page_size=15,
                            ),
                        ]
                    ),
                ],
                className="mb-5 shadow-sm",
            ),
        ],
        fluid=True,
    )
