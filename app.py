from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_FILE = Path(__file__).with_name("healthcare.csv")


st.set_page_config(page_title="Healthcare KPI Dashboard", layout="wide")
st.title("Healthcare KPI Analysis")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)

    df["Date of Admission"] = pd.to_datetime(
        df["Date of Admission"], errors="coerce"
    )
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors="coerce")
    df["Length of Stay"] = (
        df["Discharge Date"] - df["Date of Admission"]
    ).dt.days
    df["YearMonth"] = df["Date of Admission"].dt.to_period("M").astype(str)
    df["Age Group"] = pd.cut(
        df["Age"],
        bins=[0, 20, 40, 60, float("inf")],
        labels=["Below 20", "20-40", "41-60", "60+"],
        include_lowest=True,
    )

    return df


def format_currency(value: float) -> str:
    if pd.isna(value):
        return "$0"
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.2f}K"
    return f"${value:,.2f}"


def sorted_values(df: pd.DataFrame, column: str) -> list[str]:
    return sorted(df[column].dropna().unique().tolist())


df = load_data()

st.sidebar.header("Filters")

hospital = st.sidebar.multiselect(
    "Hospital",
    options=sorted_values(df, "Hospital"),
    default=sorted_values(df, "Hospital"),
)

gender = st.sidebar.multiselect(
    "Gender",
    options=sorted_values(df, "Gender"),
    default=sorted_values(df, "Gender"),
)

insurance = st.sidebar.multiselect(
    "Insurance Provider",
    options=sorted_values(df, "Insurance Provider"),
    default=sorted_values(df, "Insurance Provider"),
)

admission_dates = df["Date of Admission"].dropna()
date_range = st.sidebar.date_input(
    "Admission Date Range",
    value=(admission_dates.min().date(), admission_dates.max().date()),
    min_value=admission_dates.min().date(),
    max_value=admission_dates.max().date(),
)

start_date, end_date = admission_dates.min().date(), admission_dates.max().date()
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
elif not isinstance(date_range, (list, tuple)) and date_range:
    start_date = end_date = date_range

df_filtered = df[
    (df["Hospital"].isin(hospital))
    & (df["Gender"].isin(gender))
    & (df["Insurance Provider"].isin(insurance))
    & (df["Date of Admission"].dt.date.between(start_date, end_date))
].copy()

st.caption(
    f"Analyzing {len(df_filtered):,} of {len(df):,} patient records "
    f"from {start_date} to {end_date}."
)

if df_filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

total_revenue = df_filtered["Billing Amount"].sum()
total_patients = len(df_filtered)
avg_billing = df_filtered["Billing Amount"].mean()
avg_los = df_filtered["Length of Stay"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", format_currency(total_revenue))
col2.metric("Total Patients", f"{total_patients:,}")
col3.metric("Average Billing", format_currency(avg_billing))
col4.metric("Average Length of Stay", f"{avg_los:.2f} days")

st.subheader("Monthly Revenue Trend")

monthly_revenue = (
    df_filtered.groupby("YearMonth", as_index=False)["Billing Amount"]
    .sum()
    .sort_values("YearMonth")
)
monthly_revenue["3-Month Moving Average"] = (
    monthly_revenue["Billing Amount"].rolling(3).mean()
)

fig_ts = px.line(
    monthly_revenue,
    x="YearMonth",
    y=["Billing Amount", "3-Month Moving Average"],
    title="Revenue Trend with 3-Month Moving Average",
    markers=True,
)
st.plotly_chart(fig_ts, use_container_width=True)

col1, col2, col3 = st.columns(3)

age_rev = (
    df_filtered.groupby("Age Group", observed=False, as_index=False)["Billing Amount"]
    .sum()
    .sort_values("Age Group")
)
fig1 = px.pie(
    age_rev,
    names="Age Group",
    values="Billing Amount",
    title="Revenue by Age Group",
)
col1.plotly_chart(fig1, use_container_width=True)

admission = (
    df_filtered["Admission Type"]
    .value_counts()
    .rename_axis("Admission Type")
    .reset_index(name="Count")
)
fig2 = px.pie(
    admission,
    names="Admission Type",
    values="Count",
    title="Admission Type Distribution",
)
col2.plotly_chart(fig2, use_container_width=True)

hospital_bill = (
    df_filtered.groupby("Hospital", as_index=False)["Billing Amount"]
    .sum()
    .sort_values("Billing Amount", ascending=False)
)
fig3 = px.bar(
    hospital_bill.head(10).sort_values("Billing Amount"),
    x="Billing Amount",
    y="Hospital",
    orientation="h",
    title="Top 10 Hospitals by Billing",
)
col3.plotly_chart(fig3, use_container_width=True)

col1, col2 = st.columns(2)

doctor_bill = (
    df_filtered.groupby("Doctor", as_index=False)["Billing Amount"]
    .sum()
    .sort_values("Billing Amount", ascending=False)
)
fig4 = px.bar(
    doctor_bill.head(10).sort_values("Billing Amount"),
    x="Billing Amount",
    y="Doctor",
    orientation="h",
    title="Top 10 Doctors by Billing",
)
col1.plotly_chart(fig4, use_container_width=True)

condition_bill = (
    df_filtered.groupby("Medical Condition", as_index=False)["Billing Amount"]
    .sum()
    .sort_values("Billing Amount", ascending=False)
)
fig5 = px.bar(
    condition_bill.sort_values("Billing Amount"),
    x="Billing Amount",
    y="Medical Condition",
    orientation="h",
    title="Billing by Medical Condition",
)
col2.plotly_chart(fig5, use_container_width=True)

st.subheader("Key Insights")

top_age = age_rev.sort_values("Billing Amount", ascending=False).iloc[0]["Age Group"]
top_condition = condition_bill.iloc[0]["Medical Condition"]
top_hospital = hospital_bill.iloc[0]["Hospital"]
negative_billing_count = int((df_filtered["Billing Amount"] < 0).sum())

st.write(f"- Highest revenue comes from the **{top_age}** age group.")
st.write(f"- Top contributing medical condition is **{top_condition}**.")
st.write(f"- Top hospital by billing is **{top_hospital}**.")
st.write(
    f"- Average length of stay is **{avg_los:.2f} days**, based on discharge date "
    "minus admission date."
)
if negative_billing_count:
    st.write(
        f"- Data quality note: **{negative_billing_count:,}** filtered records have "
        "negative billing amounts and may need review."
    )

with st.expander("Dataset Preview"):
    st.dataframe(df_filtered.head(100), use_container_width=True)
