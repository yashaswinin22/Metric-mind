import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import yaml

BASE_DIR = Path(__file__).parent

st.set_page_config(
    page_title="MetricMind",
    page_icon="📊",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv(BASE_DIR / "data.csv")
    df["Profit"] = df["Revenue"] - df["Cost"]
    df["Margin"] = (df["Profit"] / df["Revenue"]) * 100
    return df

@st.cache_data
def load_semantic_layer():
    with open(BASE_DIR / "semantic_layer.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

df = load_data()
semantic_layer = load_semantic_layer()

METRICS = {
    "revenue": "Revenue",
    "cost": "Cost",
    "profit": "Profit",
    "margin": "Margin",
}

def detect_metric(question):
    question = question.lower()

    for keyword, column in METRICS.items():
        if keyword in question:
            return column

    return "Revenue"

def detect_region(question):
    question = question.lower()

    for region in df["Region"].unique():
        if region.lower() in question:
            return region

    return None

def metric_definition(metric):
    return semantic_layer["metrics"][metric.lower()]["definition"]

def build_analysis(question, filtered):
    q = question.lower()
    metric = detect_metric(question)
    region = detect_region(question)

    if region:
        filtered = filtered[filtered["Region"] == region]

    if "by region" in q or "region" in q:
        result = filtered.groupby("Region")[metric].sum().reset_index()
        return "region", metric, result, region

    if any(word in q for word in [
        "quarter",
        "quarterly",
        "q1",
        "q2",
        "q3",
        "q4"
    ]):
        result = filtered.groupby("Quarter")[metric].sum().reset_index()
        return "quarter", metric, result, region

    if any(word in q for word in [
        "why",
        "decrease",
        "drop",
        "decline"
    ]):
        result = filtered.groupby("Quarter")[metric].sum().reset_index()
        result["Change %"] = result[metric].pct_change() * 100
        return "trend", metric, result, region

    result = pd.DataFrame({
        "Metric": [metric],
        "Value": [filtered[metric].sum()]
    })

    return "summary", metric, result, region

st.title("📊 MetricMind")
st.subheader("Agentic Semantic BI Engine")

st.write(
    "Governed conversational analytics for enterprise business metrics."
)

st.sidebar.header("Filters")

selected_regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique()),
)

selected_quarters = st.sidebar.multiselect(
    "Quarter",
    sorted(df["Quarter"].unique()),
    default=sorted(df["Quarter"].unique()),
)

filtered_df = df[
    df["Region"].isin(selected_regions)
    & df["Quarter"].isin(selected_quarters)
].copy()

st.sidebar.markdown("---")
st.sidebar.caption("Governed Metrics")
st.sidebar.write("Revenue = Sum of Revenue")
st.sidebar.write("Cost = Sum of Cost")
st.sidebar.write("Profit = Revenue - Cost")
st.sidebar.write("Margin = Profit / Revenue × 100")

st.markdown("### Executive Metrics")

revenue = filtered_df["Revenue"].sum()
cost = filtered_df["Cost"].sum()
profit = filtered_df["Profit"].sum()

margin = (
    profit / revenue * 100
    if revenue
    else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Revenue", f"${revenue:,.0f}")
c2.metric("Cost", f"${cost:,.0f}")
c3.metric("Profit", f"${profit:,.0f}")
c4.metric("Margin", f"{margin:.2f}%")

st.markdown("---")

st.header("💬 Ask MetricMind")

question = st.text_input(
    "Business question",
    placeholder=(
        "Show quarterly revenue / "
        "Show revenue by region / "
        "Why did European revenue decrease?"
    )
)

if question:

    view, metric, result, detected_region = build_analysis(
        question,
        filtered_df
    )

    st.success(
        f"MetricMind analyzed {metric} "
        "using the governed semantic definition."
    )

    st.caption(
        f"Definition: {metric_definition(metric)}"
    )

    if view == "region":

        fig = px.bar(
            result,
            x="Region",
            y=metric,
            title=f"{metric} by Region"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    elif view == "quarter":

        fig = px.line(
            result,
            x="Quarter",
            y=metric,
            markers=True,
            title=f"Quarterly {metric}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    elif view == "trend":

        fig = px.line(
            result,
            x="Quarter",
            y=metric,
            markers=True,
            title=f"Quarterly {metric} Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        if len(result) >= 2:

            latest_change = result["Change %"].iloc[-1]

            if pd.notna(latest_change):

                if latest_change < 0:

                    st.warning(
                        f"{metric} decreased by "
                        f"{abs(latest_change):.2f}% "
                        "compared with the previous quarter."
                    )

                else:

                    st.info(
                        f"{metric} increased by "
                        f"{latest_change:.2f}% "
                        "compared with the previous quarter."
                    )

                if metric in [
                    "Revenue",
                    "Profit",
                    "Margin"
                ]:

                    cost_trend = (
                        filtered_df
                        .groupby("Quarter")["Cost"]
                        .sum()
                        .reset_index()
                    )

                    cost_change = (
                        cost_trend["Cost"]
                        .pct_change()
                        .iloc[-1] * 100
                    )

                    st.subheader("Secondary Breakdown")

                    st.write(
                        f"Latest Cost Change: "
                        f"{cost_change:.2f}%"
                    )

                    if cost_change > 0:

                        st.info(
                            "The latest period shows increased "
                            "cost pressure, which can contribute "
                            "to the metric decline."
                        )

                    else:

                        st.info(
                            "Cost did not increase in the latest "
                            "period. Further dimensional analysis "
                            "is required."
                        )

    st.dataframe(
        result,
        use_container_width=True
    )

    with st.expander("View API / Semantic Query"):

        query_payload = {
            "metric": metric,
            "definition": metric_definition(metric),
            "region": detected_region,
            "quarters": selected_quarters,
            "operation": view,
        }

        st.code(
            json.dumps(
                query_payload,
                indent=2
            ),
            language="json"
        )

st.markdown("---")

st.header("📋 Analytics Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

with st.expander("View Semantic Layer"):
    st.json(semantic_layer)

st.caption(
    "MetricMind | Governed Semantic BI & Conversational Analytics"
)
