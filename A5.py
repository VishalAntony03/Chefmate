import streamlit as st
import pandas as pd
import requests
from streamlit_option_menu import option_menu
import google.generativeai as genai
import folium
from streamlit_folium import folium_static

# Full screen CSS style
st.set_page_config(layout="wide")

# Add custom CSS for dark theme
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stButton > button {
        background-color: #f0ad4e;
        color: black;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #ec971f;
        color: white;
    }
    .stSelectbox, .stMultiselect {
        background-color: #fff;
        color: white;
        border-radius: 8px;
    }
    .stTextInput > div > input {
        background-color: #fff;
        color: white;
        border-radius: 8px;
    }
    .stMarkdown h1 {
        color: #fff;
    }
    .stMarkdown h2, .stMarkdown h3 {
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Navigation Menu
st.title("HungerHub")
web = option_menu(
    menu_title="Welcome to HungerHub",
    options=["Home", "Hunger Assistant"],
    icons=["house", "robot"],
    orientation="horizontal",
    styles={
        "nav-link": {"--hover-color": "#f0ad4e"},
        "nav-link-selected": {"background-color": "#f0ad4e"},
    },
)

# Load the merged dataset
@st.cache_data
def load_data():
    return pd.read_csv('merged_restaurant_data.csv')

data = load_data()

# Home Page
if web == "Home":
    st.title("🍴 Restaurant Recommendation System")
    st.subheader("🔍 Filter Restaurants")

    # Create three columns for the filters
    col1, col2, col3 = st.columns(3)

    with col1:
        cities = data['restaurant.location.city'].unique()
        selected_city = st.selectbox("Select City", cities)
    with col2:
        filtered_localities = data[data['restaurant.location.city'] == selected_city]['restaurant.location.locality'].unique()
        selected_locality = st.selectbox("Select Locality", filtered_localities)
    with col3:
        # Ensure that 'restaurant.cuisines' is a string and handle NaN values
        data['restaurant.cuisines'] = data['restaurant.cuisines'].apply(lambda x: str(x) if isinstance(x, str) else '')
        data['restaurant.cuisines'] = data['restaurant.cuisines'].fillna('')

        # Cuisines filter
        all_cuisines = set(', '.join(data['restaurant.cuisines']).split(', '))
        selected_cuisines = st.multiselect("Select Cuisines", all_cuisines)

    # Apply filters
    filtered_data = data[
        (data['restaurant.location.city'] == selected_city) &
        (data['restaurant.location.locality'] == selected_locality)
    ]

    if selected_cuisines:
        filtered_data = filtered_data[filtered_data['restaurant.cuisines'].apply(lambda x: any(cuisine in x for cuisine in selected_cuisines))]

    # Sorting the filtered_data by rating in descending order
    filtered_data = filtered_data.sort_values(by='restaurant.user_rating.aggregate_rating', ascending=False)

    st.subheader(f"🍽️ Restaurants in {selected_locality}, {selected_city}")

    if not filtered_data.empty:
        latitude = filtered_data['restaurant.location.latitude'].iloc[0]
        longitude = filtered_data['restaurant.location.longitude'].iloc[0]
        m = folium.Map(location=[latitude, longitude], zoom_start=12)

        for index, row in filtered_data.iterrows():
            folium.Marker(
                location=[row['restaurant.location.latitude'], row['restaurant.location.longitude']],
                popup=folium.Popup(f"<b>{row['restaurant.name']}</b><br>Cuisines: {row['restaurant.cuisines']}<br>Rating: {row['restaurant.user_rating.aggregate_rating']} stars", max_width=300)
            ).add_to(m)

        col1, col2 = st.columns([2, 1])

        with col1:
            counter = 1
            for _, row in filtered_data.iterrows():
                with st.container():
                    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 2, 1])
                    with col1:
                        st.write(f"**Name:** {row['restaurant.name'].upper()}")
                    with col2:
                        st.write(f"**Cuisines:** {row['restaurant.cuisines']}")
                    with col3:
                        st.write(f"**Rating:** {str(row['restaurant.user_rating.aggregate_rating'])} stars")
                    with col4:
                        st.write(f"**Cost for Two:** ₹{str(row['restaurant.average_cost_for_two'])}")
                    with col5:
                        st.markdown(f"[📋 View Menu]({row['restaurant.menu_url']})", unsafe_allow_html=True)
                        st.markdown(f"[📷 View Photos]({row['restaurant.photos_url']})", unsafe_allow_html=True)
                    with col6:
                        st.image(row['restaurant.thumb'], width=500)
                st.markdown("---")
                counter += 1

        with col2:
            folium_static(m)
    else:
        st.write("No restaurants found based on your criteria.")

# Hunger Assistant Page
elif web == "Hunger Assistant":
    GEMINI_API_KEY = 'AIzaSyBrq84GMFjmQhnbNyQhNOUd8KIFdCe4hD4'
    genai.configure(api_key=GEMINI_API_KEY)

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 512,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    def is_food_related(query):
        food_keywords = ['recipe', 'ingredients', 'how to cook', 'how to make', 'cooking', 'dish', 'prepare']
        return any(keyword in query.lower() for keyword in food_keywords)

    st.title("Chef Mate: Assistant 🤖🍳")
    st.write("Ask me how to cook your favorite dishes! For other queries, I'll politely decline. 😊")

    query = st.text_input("Ask your recipe question:")
    ask_button = st.button("Generate Recipe")

    if ask_button and query.strip():
        if is_food_related(query):
            try:
                response = chat_session.send_message(query)
                st.write(f"🍴 **Chef Mate says:** {response.text}")
            except Exception as e:
                st.error(f"Sorry, something went wrong: {e}")
        else:
            st.warning("❌ I'm only allowed to assist you with food recipes. Please ask about recipes or cooking methods.")
