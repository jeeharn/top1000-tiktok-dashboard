import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="TikTok Influencer Pro Dashboard",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 TikTok Influencer Interactive Dashboard (Top 1000)")
st.markdown("Dashboard สำหรับวิเคราะห์ข้อมูล Influencers จาก Kaggle")

# =========================
# Upload CSV
# =========================
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # =========================
    # Clean numeric columns
    # =========================
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].replace({",": "", "M": "000000", "K": "000"}, regex=True)

    numeric_cols = df.select_dtypes(include=np.number).columns

    # =========================
    # Engagement Rate
    # =========================
    if all(col in df.columns for col in ["Likes", "Comments", "Shares", "Followers"]):
        df["Engagement Rate (%)"] = (
            (df["Likes"] + df["Comments"] + df["Shares"]) 
            / df["Followers"]
        ) * 100

    # =========================
    # Sidebar Filters
    # =========================
    st.sidebar.header("🔎 Filters")

    if "Country" in df.columns:
        country_filter = st.sidebar.multiselect(
            "Select Country",
            df["Country"].unique()
        )
        if country_filter:
            df = df[df["Country"].isin(country_filter)]

    if "Followers" in df.columns:
        min_followers = int(df["Followers"].min())
        max_followers = int(df["Followers"].max())
        followers_range = st.sidebar.slider(
            "Followers Range",
            min_followers,
            max_followers,
            (min_followers, max_followers)
        )
        df = df[
            (df["Followers"] >= followers_range[0]) &
            (df["Followers"] <= followers_range[1])
        ]

    # =========================
    # KPI SECTION
    # =========================
    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    if "Followers" in df.columns:
        col1.metric("Total Influencers", len(df))
        col2.metric("Total Followers", f"{int(df['Followers'].sum()):,}")
        col3.metric("Average Followers", f"{int(df['Followers'].mean()):,}")

    if "Engagement Rate (%)" in df.columns:
        col4.metric(
            "Avg Engagement Rate",
            f"{df['Engagement Rate (%)'].mean():.2f}%"
        )

    # =========================
    # Top 10 Followers
    # =========================
    if "Followers" in df.columns and "Username" in df.columns:
        st.subheader("🏆 Top 10 Influencers by Followers")

        top10 = df.sort_values(
            by="Followers",
            ascending=False
        ).head(10)

        fig1 = px.bar(
            top10,
            x="Followers",
            y="Username",
            orientation="h",
            text="Followers",
            color="Followers",
            title="Top 10 by Followers"
        )

        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)

    # =========================
    # Engagement Chart
    # =========================
    if "Engagement Rate (%)" in df.columns:
        st.subheader("📈 Top 10 Engagement Rate")

        top_engage = df.sort_values(
            by="Engagement Rate (%)",
            ascending=False
        ).head(10)

        fig2 = px.bar(
            top_engage,
            x="Username",
            y="Engagement Rate (%)",
            text="Engagement Rate (%)",
            color="Engagement Rate (%)",
            title="Top 10 Engagement"
        )

        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # Country Distribution
    # =========================
    if "Country" in df.columns:
        st.subheader("🌍 Influencers by Country")

        country_count = df["Country"].value_counts().reset_index()
        country_count.columns = ["Country", "Count"]

        fig3 = px.pie(
            country_count,
            names="Country",
            values="Count",
            title="Country Distribution"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # =========================
    # Scatter Plot
    # =========================
    if "Followers" in df.columns and "Likes" in df.columns:
        st.subheader("📊 Followers vs Likes")

        fig4 = px.scatter(
            df,
            x="Followers",
            y="Likes",
            size="Followers",
            hover_data=["Username"],
            color="Followers",
            title="Followers vs Likes"
        )

        st.plotly_chart(fig4, use_container_width=True)

    # =========================
    # Show Full Data
    # =========================
    st.subheader("📄 Full Dataset")
    st.dataframe(df)

    # =========================
    # Download Button
    # =========================
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download Filtered Data",
        csv,
        "filtered_data.csv",
        "text/csv"
    )

else:
    st.info("📂 กรุณาอัปโหลดไฟล์ CSV เพื่อเริ่มใช้งาน")
