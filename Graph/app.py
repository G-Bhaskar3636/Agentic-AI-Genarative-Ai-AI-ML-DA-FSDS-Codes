import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------- NAV BAR --------------------------- #
st.set_page_config(page_title="Data Visualizer", layout="wide")

menu = ["Home", "Data View", "Visualizations"]
choice = st.sidebar.selectbox("📌 Navigation Menu", menu)

# --------------------------- FILE UPLOAD --------------------------- #
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

# --------------------------- HOME PAGE --------------------------- #
if choice == "Home":
    st.title("📊 Interactive Data Visualization App")
    st.write("""
    Welcome to the Streamlit Data Explorer!
    Upload a CSV file and explore your dataset visually.
    """)

# --------------------------- DATA VIEW --------------------------- #
elif choice == "Data View":
    st.title("📄 Dataset Viewer")

    if uploaded_file:
        st.subheader("🔹 Dataset Preview")
        st.dataframe(df)

        st.subheader("🔹 Statistical Summary")
        st.write(df.describe(include='all'))

    else:
        st.warning("Upload a CSV file to view data.")

# --------------------------- VISUALIZATION --------------------------- #
elif choice == "Visualizations":
    st.title("📈 Data Visualization")

    if uploaded_file:

        numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
        categorical_cols = df.select_dtypes(include='object').columns.tolist()

        graph_type = st.selectbox(
            "Select Graph Type", 
            ["Scatter Plot","Line Plot","Bar Graph","Histogram","Box Plot","Count Plot","Heatmap"]
        )

        if graph_type != "Heatmap":
            x_axis = st.selectbox("X-Axis", df.columns)

            if graph_type in ["Scatter Plot","Line Plot","Bar Graph","Box Plot"]:
                y_axis = st.selectbox("Y-Axis", numeric_cols)

            hue_col = st.selectbox("Hue (Optional)", [None] + df.columns.tolist()) \
                       if graph_type not in ["Histogram","Heatmap"] else None

        # ========= PLOT AREA ========= #
        fig, ax = plt.subplots(figsize=(10,5))

        if graph_type == "Scatter Plot":
            sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=hue_col, ax=ax)

        elif graph_type == "Line Plot":
            sns.lineplot(data=df, x=x_axis, y=y_axis, hue=hue_col, marker="o", ax=ax)

        elif graph_type == "Bar Graph":
            sns.barplot(data=df, x=x_axis, y=y_axis, hue=hue_col, ax=ax)

        elif graph_type == "Histogram":
            sns.histplot(data=df, x=x_axis, kde=True, ax=ax)

        elif graph_type == "Box Plot":
            sns.boxplot(data=df, x=x_axis, y=y_axis, hue=hue_col, ax=ax)

        elif graph_type == "Count Plot":
            col = st.selectbox("Select Column", categorical_cols)
            sns.countplot(data=df, x=col, hue=hue_col, ax=ax)

        elif graph_type == "Heatmap":
            fig, ax = plt.subplots(figsize=(9,5))
            
            numeric_df = df.select_dtypes(include=['int64','float64'])  # ⬅ FIX APPLIED

            if numeric_df.shape[1] > 1:
                sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
            else:
                st.error("❌ No numeric columns available for Heatmap!")

        # Graph formatting
        plt.xticks(rotation=45)
        plt.tight_layout()

        if graph_type != "Heatmap" and hue_col:
            ax.legend(bbox_to_anchor=(1.05,1), loc='upper left')

        st.pyplot(fig)

    else:
        st.warning("Upload CSV to visualize your data.")

