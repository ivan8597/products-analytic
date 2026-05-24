import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CHART_LAYOUT = dict(
    template="plotly_white",
    margin=dict(l=40, r=20, t=60, b=40),
    font=dict(size=12),
    title_font_size=15,
)


def category_sales_figure(df: pd.DataFrame) -> go.Figure:
    plot_df = df.sort_values("Продано, шт.")
    fig = px.bar(
        plot_df,
        x="Продано, шт.",
        y="Категория",
        orientation="h",
        text="Продано, шт.",
        color="Продано, шт.",
        color_continuous_scale="Blues",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(
        **CHART_LAYOUT,
        title="Продажи по товарным категориям (level1), шт.",
        xaxis_title="Количество проданных единиц, шт.",
        yaxis_title="Категория",
        coloraxis_showscale=False,
        height=max(420, len(plot_df) * 22),
    )
    return fig


def subcategory_figure(subcat: pd.DataFrame, category: str) -> go.Figure:
    plot_df = subcat[subcat["Категория"] == category].sort_values("Продано, шт.")
    fig = px.bar(
        plot_df,
        x="Продано, шт.",
        y="Подкатегория",
        orientation="h",
        text="Продано, шт.",
        color="Продано, шт.",
        color_continuous_scale="Teal",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(
        **CHART_LAYOUT,
        title=f"Распределение продаж по подкатегориям: {category}",
        xaxis_title="Количество проданных единиц, шт.",
        yaxis_title="Подкатегория (level2)",
        coloraxis_showscale=False,
        height=max(320, len(plot_df) * 36),
    )
    return fig


def promo_pie_figure(promo: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        promo,
        names="Тип продажи",
        values="Продано, шт.",
        hole=0.35,
        color="Тип продажи",
        color_discrete_map={"Промо": "#E45756", "Регулярная цена": "#72B7B2"},
    )
    fig.update_traces(textposition="inside", textinfo="label+percent+value")
    fig.update_layout(
        **CHART_LAYOUT,
        title="Доля промо-продаж в категории «Сыры» (в штуках)",
        height=420,
    )
    return fig


def margin_rub_figure(margin: pd.DataFrame) -> go.Figure:
    plot_df = margin.sort_values("Маржа_руб")
    fig = px.bar(
        plot_df,
        x="Маржа_руб",
        y="Категория",
        orientation="h",
        text="Маржа_руб",
        color="Маржа_руб",
        color_continuous_scale="Greens",
    )
    fig.update_traces(texttemplate="%{text:,.0f} ₽", textposition="outside")
    fig.update_layout(
        **CHART_LAYOUT,
        title="Маржа по категориям, руб.",
        xaxis_title="Маржа, руб.",
        yaxis_title="Категория",
        coloraxis_showscale=False,
        height=max(520, len(plot_df) * 22),
    )
    return fig


def margin_pct_figure(margin: pd.DataFrame) -> go.Figure:
    plot_df = margin.sort_values("Маржа_%")
    fig = px.bar(
        plot_df,
        x="Маржа_%",
        y="Категория",
        orientation="h",
        text="Маржа_%",
        color="Маржа_%",
        color_continuous_scale="Purples",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(
        **CHART_LAYOUT,
        title="Маржа по категориям, % от выручки",
        xaxis_title="Маржа, %",
        yaxis_title="Категория",
        coloraxis_showscale=False,
        height=max(520, len(plot_df) * 22),
    )
    return fig
