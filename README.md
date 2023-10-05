# Restaurant Analyzer
200,000-300,000 Scraped Restaurants from Google. Using Streamlit to display.
https://www.kaggle.com/code/kwxdata/380k-restaurants 

# Restaurant Analyzer

Restaurant Analyzer is a Streamlit app designed to visualize, analyze, and explore restaurant data from a dataset. This app provides various views and analytics options, offering a detailed overview of restaurants across different categories, ratings, and geographical locations. Moreover, it allows users to interact with and explore the data in a variety of ways including maps, charts, and search functionality.

## Features

### 1. Map View
Visualize the geographical distribution of restaurants using an interactive map. Options in this view include:
- **View all data on map**: Displays all restaurant locations on the map.
- **Paginate data for faster viewing**: View a subset of data on the map to enhance loading times. Navigate through different pages to explore different subsets.
- **Select a specific category**: View restaurants belonging to a specific category on the map.

### 2. Analytics
Deep dive into the data analytics of restaurant categories, offering the following visualizations:
- **Bar plot**: Displays the top N restaurants within the selected category.
- **Histogram**: Shows the distribution of ratings within the selected category.
- **Pie chart**: Offers a pie chart visualization of the ratings distribution.
- **Scatter plot**: Plots the average ratings for each restaurant title in the selected category.
- **Area Chart**: Presents the distribution of ratings via an area chart.
- **Donut Plot**: Visualizes the top restaurants in a donut plot.

### 3. Search
Allows users to search for restaurants by name and displays close matches from the dataset. Upon selecting a specific match:
- Displays detailed information about the selected restaurant.
- Provides an approximate location of the restaurant (state and country).
- Showcases the restaurant location on a map.

## Dependencies
The app makes use of the following Python libraries:
- `streamlit`: For app creation and UI components.
- `pandas`: For data manipulation.
- `matplotlib`: For data visualization in analytics.
- `numpy`: For numerical operations.
- `difflib`: For string matching in search.
- `geopy`: To fetch location details.
- `geocoder`: For geocoding and reverse geocoding.
- `folium`: For mapping visualizations.
- `seaborn`: For advanced data visualization.
- `streamlit_folium`: For embedding folium maps in Streamlit.

## How to Use
1. **Map View**: Navigate through different restaurants, inspect their locations, and explore according to categories or pagination as per your requirement.
   
2. **Analytics**: Select a category from the drop-down and visualize the various plots which offer insights into the top restaurants, ratings distribution, and more within the chosen category.
   
3. **Search**: Enter a restaurant name and explore the closely matched results. Click on a match to view detailed information and its location on a map.

## Note for Developers
Ensure to have all the dependencies installed and the necessary API keys (if required by libraries in future updates) configured before running the app.

## Data Source
The data used in this app can be downloaded from [Kaggle](https://www.kaggle.com/datasets/kwxdata/380k-restaurants-mostly-usa-based) and contains information about restaurants, primarily based in the USA.

## Important Note
The dataset URL in the code might not work as direct downloads from Kaggle require login. Therefore, download the dataset manually from the provided Kaggle link, save it locally, and adjust the path in the `load_data` function accordingly.

## Conclusion
Restaurant Analyzer provides an insightful and interactive way to explore and visualize restaurant data, assisting both enthusiasts and professionals in exploring trends, distributions, and specifics of various dining establishments across locations and categories.
