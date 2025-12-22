import serpapi 
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def compare(med_name):
    params = {
        "engine": "google_shopping",
        "location": "Austin, Texas, United States",
        "q": med_name,
        "api_key": "8e71093d165f2b0c28f3dd039b113d3eccda45abb4e22f2f2586bef314b933ce",
        "gl": "in"
        }
    search = serpapi.GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    return shopping_results

def main_header():
    c1, c2 = st.columns(2)
    c1.image(r"C:\Users\bhask\OneDrive\Desktop\NIT\Projects\serpet\image\logo.png")
    c2.title("E-Pharmacy Price Comparisition System")

med_title = []
med_price = []



st.sidebar.title("Enter The Name Of Medicine")
med_name = st.sidebar.text_input("Enter Name Here 👇")
num = st.sidebar.text_input("Enter Number of Options 👇")


main_header()
st.write("Welcome to E-Pharmacy Price Comparison System")

if med_name.strip() != '' and num != None:
    if st.sidebar.button("Price Compare"):

        result = compare(med_name)
        low_price = result[0].get('price')
        low_index = 0

        for i in range(int(num)):
            med_title.append(result[i].get('title'))
            med_price.append(result[i].get('price')[1:])
            st.title(f"Option {i+1}")
            c1, c2, c3 = st.columns(3)
            curr_price = result[i].get('price')

            c1.write("Company")
            c2.write(f"{result[i].get('source')}")
            c3.image(result[i].get('thumbnail'), width=200)

            c1.write("Medicine Name")
            c2.write(f"{result[i].get('title')}")

            c1.write("Price")
            c2.write(f"{result[i].get('price')}")

            c1.write("Buy Link")
            url = result[i].get('product_link')
            c2.write("[See on Web](%s)"%url)
            """________________________________________________________________"""

            if curr_price < low_price:
                low_price = curr_price
                low_index = i

        st.title(f"Lowest Prise Medicine Option is {i+1}")
        c1, c2, c3 = st.columns(3)

        c1.write("Company")
        c2.write(f"{result[low_index].get('source')}")
        c3.image(result[low_index].get('thumbnail'))

        c1.write("Medicine Name")
        c2.write(f"{result[low_index].get('title')}")

        c1.write("Price")
        c2.write(f"{result[low_index].get('price')}")

        c1.write("Buy Link")
        url = result[low_index].get('product_link')
        c2.write("[See on Web](%s)"%url)


if len(med_price) == 0:
    st.warning("⚠️ Please compare medicines first.")
else:
    df = pd.DataFrame({"Medicine Name": med_title,"Medicine Cost": pd.to_numeric(med_price)})

    st.subheader("📊 Price Comparison Bar Chart")
    fig, ax = plt.subplots()
    sns.barplot(data=df, x='Medicine Name', y='Medicine Cost', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)

    st.subheader("🥧 Price Distribution Pie Chart")
    fig2, ax2 = plt.subplots()
    ax2.pie(df['Medicine Cost'], labels = df['Medicine Name'], autopct="%1.1f%%", startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2)
    