# ==========================================================
# NAIROBI CITY COUNTY
# OWN SOURCE REVENUE DASHBOARD
# ==========================================================

# ----------------------------
# IMPORT LIBRARIES
# ----------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from PIL import Image

# ----------------------------
# PAGE CONFIGURATION
# ----------------------------

st.set_page_config(
    page_title="Nairobi County OSR Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# NAIROBI COUNTY THEME
# ----------------------------

PRIMARY_GREEN = "#078930"
PRIMARY_YELLOW = "#FCDD09"
BACKGROUND = "#FFFFFF"
PANEL = "#F5F5F5"
TEXT = "#333333"
SUCCESS = "#2E7D32"
WARNING = "#FFC107"
DANGER = "#D32F2F"

st.markdown("""
<style>

/* Selected items inside multiselect */
.stMultiSelect [data-baseweb="tag"]{
    background-color: #FCDD09 !important;
    color: black !important;
    border-radius: 8px;
}

/* Text inside the tag */
.stMultiSelect [data-baseweb="tag"] span{
    color: black !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD DATA
# ----------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "processed" / "OSR2025JUNE30_Clean.xlsx"

df = pd.read_excel(file_path)

# ==========================================================
# PAGE HEADER
# ==========================================================

st.markdown(
    """
    <h1 style="
        text-align:center;
        color:#078930;
        margin-bottom:0px;
        font-size:52px;
        font-weight:700;
    ">
    Nairobi City County
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style="
        text-align:center;
        color:#333333;
        margin-top:0px;
        margin-bottom:5px;
    ">
    Own Source Revenue Executive Dashboard
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        color:gray;
        font-size:20px;
        margin-top:0px;
    ">
    Financial Year 2024/2025
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <hr style="
        border:2px solid #FCDD09;
        margin-top:20px;
        margin-bottom:35px;
    ">
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <hr style="
        border:2px solid #FCDD09;
    ">
    """,
    unsafe_allow_html=True
)

# ==========================================================
# CUSTOM KPI CARD
# ==========================================================

def kpi_card(title, value, subtitle):

    st.markdown(
        f"""
        <div style="
            background-color:white;
            padding:20px;
            border-radius:12px;
            border-left:8px solid #078930;
            box-shadow:2px 2px 8px rgba(0,0,0,0.15);
            margin-bottom:10px;
        ">

        <h5 style="
            color:#333333;
            margin-bottom:8px;
        ">
        {title}
        </h5>

        <h2 style="
            color:#078930;
            margin-bottom:5px;
        ">
        {value}
        </h2>

        <p style="
            color:gray;
            font-size:14px;
        ">
        {subtitle}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.markdown(
    """
    <div style="
        background-color:#078930;
        padding:15px;
        border-radius:10px;
        margin-bottom:15px;
    ">
        <h2 style="color:white; text-align:center; margin:0;">
        Dashboard Filters
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### Revenue Streams")

selected_streams = st.sidebar.multiselect(
    "Choose revenue streams",
    options=sorted(df["Revenue_Stream"].unique()),
    default=sorted(df["Revenue_Stream"].unique()),
    placeholder="Search or select revenue streams..."
)

st.sidebar.header("Interactive Analysis")

selected_quarter = st.sidebar.selectbox(
    "Quarter",
    ["Q1", "Q2", "Q3", "Q4"]
)

top_n = st.sidebar.slider(
    "Number of Revenue Streams to Display",
    min_value=5,
    max_value=20,
    value=10,
    step=1
)

# =========================================================
# Create a working copy of the data
# =========================================================
filtered_df = df.copy()

# Filter by Revenue Stream
if selected_streams != "All":
    filtered_df = filtered_df[
    filtered_df["Revenue_Stream"].isin(selected_streams)
]

# ======================================================
# DOWNLOADS
# ======================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Downloads")

# Convert filtered data to CSV
csv = filtered_df.to_csv(index=False).encode("utf-8")

if len(selected_streams) == 1:
    safe_stream = selected_streams[0].replace(" ", "_")
else:
    safe_stream = "Multiple_Streams"

st.sidebar.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name=f"Nairobi_OSR_{safe_stream}_{selected_quarter}.csv",
    mime="text/csv"
)



# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = df[
    df["Revenue_Stream"].isin(selected_streams)
]

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

# Total Revenue
total_revenue = filtered_df["Total"].sum()

# Number of Revenue Streams
total_streams = filtered_df["Revenue_Stream"].nunique()

# Best Performing Quarter
quarter_totals = filtered_df[["Q1", "Q2", "Q3", "Q4"]].sum()

best_quarter = quarter_totals.idxmax()

# Highest Revenue Stream
top_stream = filtered_df.loc[filtered_df["Total"].idxmax(), "Revenue_Stream"]

# ==========================================================
# KPI CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    kpi_card(

        "💰 Total Revenue",

        f"KES {total_revenue/1e9:.2f} B",

        "FY 2024/25"

    )

with col2:

    kpi_card(

        "📑 Revenue Streams",

        total_streams,

        "Revenue Sources"

    )

with col3:

    kpi_card(

        "🏆 Best Quarter",

        best_quarter,

        "Highest Collection"

    )

with col4:

    kpi_card(

        "⭐ Top Stream",

        top_stream,

        "Highest Contributor"

    )

# ==========================================================
# ROW 1 - CHARTS
# ==========================================================

chart1, chart2 = st.columns(2)

# ----------------------------
# LEFT CHART
# ----------------------------

with chart1:

    st.subheader("Revenue by Quarter")

    quarter_totals = filtered_df[["Q1", "Q2", "Q3", "Q4"]].sum()

    fig, ax = plt.subplots(figsize=(7,4))

    colors = ["#078930", "#FCDD09", "#078930", "#FCDD09"]

    ax.bar(
        quarter_totals.index,
        quarter_totals.values,
        color=colors
    )

    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x/1e9:.1f}B")
    )

    ax.set_ylabel("Revenue (KSh Billions)")
    ax.set_xlabel("Quarter")
    ax.set_title("Quarterly Revenue Performance")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# ----------------------------
# RIGHT CHART
# ----------------------------

with chart2:

    st.subheader("Top Revenue Streams")

    top_streams = (
        filtered_df
        .sort_values(by="Total", ascending=False)
        .head(top_n)
    )

    fig2, ax2 = plt.subplots(figsize=(7,4))

    ax2.barh(
        top_streams["Revenue_Stream"],
        top_streams["Total"],
        color="#078930"
    )

    ax2.invert_yaxis()

    ax2.xaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x/1e9:.1f}B")
    )

    ax2.set_xlabel("Revenue (KSh Billions)")
    ax2.set_ylabel("")

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig2)

import plotly.express as px

# ======================================================
# DASHBOARD HEALTH SCORE
# ======================================================

health_score = 70

st.markdown("---")

st.subheader("Revenue Health Score")

st.progress(health_score / 100)

st.metric(
    label="Overall Performance",
    value=f"{health_score}%"
)

if health_score >= 90:
    st.success("Excellent revenue performance observed across the selected revenue streams.")

elif health_score >= 75:
    st.warning("Revenue performance is good, with opportunities for improvement.")

else:
    st.error("Revenue performance requires immediate management attention.")

# ==========================================================
# ROW 2 - EXECUTIVE ANALYSIS
# ==========================================================

chart3, chart4 = st.columns(2)
with chart3:
    st.subheader("Revenue Contribution")
    revenue_share = (
    filtered_df
    .groupby("Revenue_Stream")["Total"]
    .sum()
    .reset_index()
)
    revenue_share["Percentage"] = (
    revenue_share["Total"] /
    revenue_share["Total"].sum()
) * 100
    revenue_share = revenue_share.sort_values(
    by="Total",
    ascending=False
).head(top_n)
    fig3 = px.pie(
    revenue_share,
    values="Total",
    names="Revenue_Stream",
    hole=0.55,
    color_discrete_sequence=[
        "#078930",
        "#FCDD09",
        "#4CAF50",
        "#FFC107",
        "#66BB6A",
        "#FFEB3B",
        "#81C784",
        "#FFD54F",
        "#A5D6A7",
        "#FFF176"
    ]
)
    fig3.update_layout(

    margin=dict(
        l=20,
        r=20,
        t=30,
        b=20
    ),

    legend_title="Revenue Stream"

)
    st.plotly_chart(
    fig3,
    use_container_width=True
)
with chart4:
    st.subheader(f"Revenue Streams - {selected_quarter}")
    quarter_data = (
    filtered_df[
        ["Revenue_Stream", selected_quarter]
    ]
    .sort_values(
        by=selected_quarter,
        ascending=False
    )
    .head(top_n)
)
    fig4 = px.bar(

    quarter_data,

    x=selected_quarter,

    y="Revenue_Stream",

    orientation="h",

    color=selected_quarter,

    color_continuous_scale=[
        "#FCDD09",
        "#078930"
    ]

)
    fig4.update_yaxes(
    autorange="reversed"
)
    fig4.update_layout(

    xaxis_title="Revenue (KES)",

    yaxis_title="",

    coloraxis_showscale=False,

    margin=dict(
        l=20,
        r=20,
        t=30,
        b=20
    )

)
    st.plotly_chart(

    fig4,

    use_container_width=True

)

# ==========================================================
# EXECUTIVE BUSINESS INSIGHTS
# ==========================================================
st.markdown("---")

st.header("Executive Business Insights")
total_revenue = filtered_df["Total"].sum()
top_stream = (
    filtered_df
    .sort_values("Total", ascending=False)
    .iloc[0]
)
quarter_totals = filtered_df[
    ["Q1","Q2","Q3","Q4"]
].sum()

best_quarter = quarter_totals.idxmax()

top5_percentage = (

    filtered_df
    .sort_values("Total", ascending=False)
    .head(5)["Total"]
    .sum()

    /

    total_revenue

) * 100

st.info(f"""

### Executive Summary

• Total Own Source Revenue collected was **KSh {total_revenue/1e9:.2f} Billion**.

• **{top_stream['Revenue_Stream']}** was the largest revenue contributor.

• Revenue collection peaked during **{best_quarter}**.

• The Top 5 revenue streams generated **{top5_percentage:.1f}%** of total revenue.

""")

st.success("""

### Strategic Recommendations

• Strengthen revenue collection among low-performing streams.

• Reduce dependence on a small number of revenue sources.

• Replicate the collection strategies used during the best-performing quarter.

• Continue expanding digital payment systems to improve compliance.

""")

# ==========================================================
# KEY PERFORMANCE ALERTS
# ==========================================================

st.markdown("---")
st.header("🚨 Key Performance Alerts")
st.success(
    f"🟢 {best_quarter} recorded the highest Own Source Revenue collection."
)
st.info(
    f"🔵 {top_stream['Revenue_Stream']} remains the largest contributor to Own Source Revenue."
)
lowest_stream = (
    filtered_df
    .sort_values("Total")
    .iloc[0]
)
st.warning(
    f"🟡 {lowest_stream['Revenue_Stream']} generated the lowest revenue and may require policy attention."
)
dependency = top_stream["Total"] / total_revenue
if dependency > 0.30:

    st.error(
        f"🔴 Revenue dependency is high. {top_stream['Revenue_Stream']} contributes {dependency:.1%} of total revenue."
    )

else:

    st.success(
        "🟢 Revenue sources are reasonably diversified."
    )

if top5_percentage > 80:

    st.error(
        f"🔴 Top five revenue streams contribute {top5_percentage:.1f}% of total revenue. Diversification is recommended."
    )

elif top5_percentage > 60:

    st.warning(
        f"🟡 Top five streams contribute {top5_percentage:.1f}% of revenue."
    )

else:

    st.success(
        "🟢 Revenue portfolio is well diversified."
    )


# ======================================================
# FOOTER
# ======================================================

import pandas as pd

# Current date
generated_date = pd.Timestamp.now().strftime("%d %B %Y")

st.markdown("---")

st.markdown(
    f"""
    <style>
    .footer {{
        text-align: center;
        color: #6c757d;
        font-size: 13px;
        line-height: 1.6;
        padding-top: 10px;
        padding-bottom: 20px;
    }}
    </style>

    <div class="footer">

    <b style="font-size:16px; color:#078930;">
    Nairobi City County Government
    </b>

    <br>
    <b>Own Source Revenue (OSR) Business Intelligence Dashboard</b>
    <br>
    Financial Year <b>2024/2025</b>
    <br><br>
    Developed by
    <br>
    <b>Erastus Okomo</b>
    <br>
    Senior Economist
    <br>
    Economic Planning Department
    <br><br>
    Powered by
    <span style="color:#078930;"><b>Python</b></span> •
    <span style="color:#078930;"><b>Streamlit</b></span> •
    <span style="color:#078930;"><b>Pandas</b></span> •
    <span style="color:#078930;"><b>Plotly</b></span>
    <br><br>

    Dashboard Version <b>1.0</b>
    <br>
    Generated on <b>{generated_date}</b>
    <br><br>
    © 2026 Nairobi City County Government. All Rights Reserved.
    </div>

    """,
    unsafe_allow_html=True
)