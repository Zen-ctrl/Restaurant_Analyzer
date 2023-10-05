import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import difflib
from geopy.geocoders import Nominatim
import geocoder
import folium
import seaborn as sns
from streamlit_folium import folium_static


# Add the title text
st.title("Restaurant Analyzer")


def get_state(lat, lon):
    location = geocoder.osm([lat, lon], method='reverse')
    return location.state, location.country

@st.cache_data
def load_data():
    data = pd.read_csv(r"https://www.kaggle.com/datasets/kwxdata/380k-restaurants-mostly-usa-based/download")
    data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')
    data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')
    data.dropna(subset=['Rating'], inplace=True)
    return data.dropna(subset=['Latitude', 'Longitude'])

df = load_data()

COLOR_MAP = plt.cm.viridis(np.linspace(0, 1, len(df['Category'].unique())))
category_to_color = dict(zip(df['Category'].unique(), COLOR_MAP))
df['color'] = df['Category'].apply(lambda x: category_to_color.get(x))

page = st.sidebar.selectbox("Choose a view", ["Map View", "Analytics", "Search"])

if page == "Map View":
    st.title("Restaurants")
    choice = st.selectbox("Choose a viewing mode", ["View all data on map", "Paginate data for faster viewing", "Select a specific category"])

    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=4)

    if choice == "View all data on map":
        data_to_plot = df.copy()
    elif choice == "Paginate data for faster viewing":
        items_per_page = 1000
        num_pages = len(df) // items_per_page + 1
        page_num = st.selectbox('Select page number', list(range(1, num_pages+1)))
        start = (page_num - 1) * items_per_page
        end = start + items_per_page
        data_to_plot = df.iloc[start:end]
    elif choice == "Select a specific category":
        category = st.selectbox("Select a category", df['Category'].unique())
        data_to_plot = df[df['Category'] == category]

    for _, row in data_to_plot.iterrows():
        tooltip_text = f"Name: {row['Title']}<br>Category: {row['Category']}<br>Rating: {row['Rating']}"
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            tooltip=tooltip_text,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    folium_static(m)

    if choice == "Paginate data for faster viewing":
        st.table(data_to_plot[['Title', 'Category', 'Rating', 'Phone', 'Address', 'Latitude', 'Longitude']])

elif page == "Analytics":
    st.title("Restaurants Analytics")
    
    selected_category = st.selectbox("Select a category to analyze", df['Category'].unique())
    filtered_df = df[df['Category'] == selected_category]
    
    top_n = st.slider("Select the number of top restaurants to display:", 1, 50, 10)
    
    # Dynamically adjust the plot width based on the number of results to display
    width = max(10, top_n * 0.2)
    height = 6
    
    # Bar plot
    fig, ax = plt.subplots(figsize=(width, height))
    top_restaurants = filtered_df['Title'].value_counts().nlargest(top_n)
    ax.bar(top_restaurants.index, top_restaurants.values, color=plt.cm.viridis(np.linspace(0, 1, len(top_restaurants))))
    ax.set_xlabel("Restaurant Names")
    ax.set_ylabel("Number of Occurrences")
    ax.set_title("Top Restaurants in " + selected_category)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    # Histogram
    fig, ax = plt.subplots(figsize=(width, height))
    filtered_df['Rating'].hist(bins=20, ax=ax, color="skyblue", edgecolor="black")
    ax.set_title("Ratings Distribution for " + selected_category)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Number of Restaurants")
    st.pyplot(fig)
    
    # Pie chart
    fig, ax = plt.subplots(figsize=(width, height))
    ratings_distribution = filtered_df['Rating'].value_counts()
    ax.pie(ratings_distribution, labels=ratings_distribution.index, startangle=90, autopct='%1.1f%%', wedgeprops=dict(width=0.4))
    ax.set_title("Ratings Pie Chart for " + selected_category)
    st.pyplot(fig)
    
    # Scatter plot of average rating for each restaurant title
    fig, ax = plt.subplots(figsize=(width, height))
    average_ratings = filtered_df.groupby('Title')['Rating'].mean()
    titles = average_ratings.index
    ratings = average_ratings.values
    ax.scatter(ratings, titles)
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Restaurant Name")
    ax.set_title("Average Ratings of Restaurants in " + selected_category)
    st.pyplot(fig)

    # Area Chart
    fig, ax = plt.subplots(figsize=(width, height))
    filtered_df['Rating'].value_counts().sort_index().plot.area(ax=ax)
    ax.set_title("Area Chart of Ratings for " + selected_category)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Number of Restaurants")
    st.pyplot(fig)

    # Donut Plot
    fig, ax = plt.subplots(figsize=(width, height))
    ax.pie(top_restaurants.values, labels=top_restaurants.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.viridis(np.linspace(0, 1, len(top_restaurants))))
    ax.add_artist(plt.Circle((0,0),0.70,fc='white'))
    ax.set_title("Donut Plot of Top Restaurants in " + selected_category)
    st.pyplot(fig)



elif page == "Search":
    st.title("Search Restaurants")
    search_query = st.text_input("Search for a restaurant:")

    if search_query:
        close_matches = difflib.get_close_matches(search_query, df['Title'].tolist(), n=5)
        if close_matches:
            matched_dataframes = [df[df['Title'] == match] for match in close_matches]
            combined_matched_data = pd.concat(matched_dataframes)

            # Display the number of entries in the DataFrame
            st.write(f"Number of restaurants found: {len(combined_matched_data)}")

            st.write(combined_matched_data)  # Display the combined data for all close matches

            selected_match = st.selectbox("Select a specific match:", close_matches)
            match_data = df[df['Title'] == selected_match]
            
            lat = match_data['Latitude'].iloc[0]
            lon = match_data['Longitude'].iloc[0]
            state, country = get_state(lat, lon)
            st.write(f"Approximate Location: {state}, {country}")
            st.map(match_data[['Latitude', 'Longitude', 'color']].rename(columns={"Latitude": "lat", "Longitude": "lon", "color": "color"}))
