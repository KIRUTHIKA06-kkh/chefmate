import streamlit as st
import pickle
import pandas as pd
import geopy.distance
import google.generativeai as genai

with open('rating_map.pkl', 'rb') as f:
    rating_map = pickle.load(f)

with open('cuisines_list.pkl', 'rb') as f:
    cuisines = pickle.load(f)

with open('city_encoder.pkl', 'rb') as f:
    city_encoder = pickle.load(f)

with open('kmeans_model.pkl', 'rb') as f:
    kmeans = pickle.load(f)

features = ['Rating text', 'City', 'Average Cost for Two', 'Price Range', 
            'Table Booking', 'Online Delivery', 'Delivering now', 'Longitude', 'Latitude'] + list(cuisines)

st.set_page_config(page_title="ChefMate", page_icon="🍴", layout="wide")
 
st.title("Welcome to ChefMate - Restaurant Recommendation & Cooking Assistant")
st.subheader("Get personalized restaurant recommendations and cooking guidance!")

st.sidebar.title("User Preferences")

selected_cuisine = st.sidebar.multiselect('Choose your preferred cuisine(s):', options=cuisines)
selected_city = st.sidebar.selectbox('Select City:', options=city_encoder.classes_)
budget_range = st.sidebar.slider('Average Cost for Two:', 0, 5000, 500)

user_lat = st.sidebar.number_input('Enter your latitude:', value=19.0760)
user_lon = st.sidebar.number_input('Enter your longitude:', value=72.8777)

def recommend_restaurants():
    restaurant_data = pd.read_csv('zomatodata.csv') 

    city_idx = city_encoder.transform([selected_city])[0]
    filtered_data = restaurant_data[restaurant_data['City'] == city_idx]
    
    if filtered_data.empty:
        st.write("No restaurants found for the selected city.")
        return  
    
    features_data = filtered_data[features]
    
    if features_data.empty:
        st.write("No data available for clustering.")
        return
    
    try:
        predictions = kmeans.predict(features_data)
        filtered_data['KMeans_Cluster'] = predictions
    except ValueError as e:
        st.write(f"Error during clustering: {str(e)}")
        return
    
    recommended_restaurants = filtered_data[['Restaurant Name', 'Ratings', 'Cuisine', 'Average Cost for Two', 'Location']]
    st.write(f"Here are some restaurant recommendations in {selected_city}:")
    st.dataframe(recommended_restaurants)

if st.sidebar.button('Get Restaurant Recommendations'):
    recommend_restaurants()

def get_nearby_restaurants():
    restaurant_data = pd.read_csv('zomatodata.csv') 
    nearby_restaurants = []
    
    for idx, row in restaurant_data.iterrows():
        restaurant_coords = (row['Latitude'], row['Longitude'])
        user_coords = (user_lat, user_lon)
        
        distance = geopy.distance.distance(user_coords, restaurant_coords).km
        
        if distance <= 5:
            row['Location'] = row['Location']  
            nearby_restaurants.append(row)
    
    if nearby_restaurants:
        nearby_df = pd.DataFrame(nearby_restaurants)
        
        nearby_df = nearby_df[['Restaurant Name', 'Ratings', 'Cuisine', 'Average Cost for Two', 'Location']]
        
        st.write("Your Nearby Restaurants:")
        st.dataframe(nearby_df)
    else:
        st.write("No nearby restaurants for your Location.")

if st.sidebar.button('Nearby Restaurants'):
    get_nearby_restaurants()

api_key = st.secrets["gemini_api_key"] 
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

cooking_keywords = ["recipe", "cook", "bake", "grill", "boil", "fry", "kitchen", "ingredients",
                    "spices", "cooking", "dish", "meal", "food", "chef", "oven", "stove", "cuisine", "prepare","make"]

def contains_cooking_keywords(user_message):
    return any(keyword in user_message.lower() for keyword in cooking_keywords)

history = [
    {"role": "user", "parts": "Hello! I need some cooking advice."},
    {"role": "model", "parts": "Hello! I'm here to help with your cooking. What would you like to know?"}
]

chat = model.start_chat(history=history)

def get_chatbot_response(user_message):
    if contains_cooking_keywords(user_message):
        response = chat.send_message(user_message)
        return response.text
    else:
        return "Please ask a cooking recipes"

st.header("Ask ChefMate Anything About Cooking")
user_query = st.text_input("How can I help you in cooking:")

if user_query:
    chatbot_reply = get_chatbot_response(user_query)
    st.write(f"**ChefMate says**: {chatbot_reply}")
else:
    st.write("Type a question in the box above to ask ChefMate about cooking!")