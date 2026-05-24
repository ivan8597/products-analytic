import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dash_table

from dashboard.data import load_dashboard_data
from dashboard.figures import subcategory_figure
from dashboard.layout import build_layout


def create_app() -> dash.Dash:
    data = load_dashboard_data()

    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.FLATLY],
        title="Products Analytics",
        suppress_callback_exceptions=True,
    )
    app.layout = build_layout(data)

    @app.callback(
        Output("subcategory-chart", "figure"),
        Output("subcategory-table", "children"),
        Input("category-dropdown", "value"),
    )
    def update_subcategory(category: str):
        subset = data.subcat[data.subcat["Категория"] == category]
        fig = subcategory_figure(data.subcat, category)
        table = dash_table.DataTable(
            data=subset.to_dict("records"),
            columns=[{"name": col, "id": col} for col in subset.columns],
            page_size=10,
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "8px", "fontSize": 13},
            style_header={"fontWeight": "600", "backgroundColor": "#f8f9fa"},
        )
        return fig, table

    return app


def run(host: str = "127.0.0.1", port: int = 8050, debug: bool = True) -> None:
    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run()
