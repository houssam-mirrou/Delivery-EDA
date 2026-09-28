import streamlit as st
import requests
from datetime import date, time
import os

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000/predict",
)
st.title("Delivery Time Prediction")
st.write("Enter the delivery information below.")

age = st.number_input(
    "Delivery person age",
    min_value=1,
    value=30,
)

rating = st.number_input(
    "Delivery person rating",
    min_value=0.0,
    max_value=5.0,
    value=4.5,
    step=0.1,
)

vehicle_condition = st.selectbox(
    "Vehicle condition",
    [0, 1, 2, 3],
)

weather = st.selectbox(
    "Weather",
    [
        "Sunny",
        "Stormy",
        "Sandstorms",
        "Cloudy",
        "Fog",
        "Windy",
    ],
)

traffic = st.selectbox(
    "Traffic density",
    [
        "Low",
        "Medium",
        "High",
        "Jam",
    ],
)

order_type = st.selectbox(
    "Order type",
    [
        "Snack",
        "Meal",
        "Drinks",
        "Buffet",
    ],
)

vehicle_type = st.selectbox(
    "Vehicle type",
    [
        "motorcycle",
        "scooter",
        "electric_scooter",
        "bicycle",
    ],
)

multiple_deliveries = st.number_input(
    "Multiple deliveries",
    min_value=0,
    value=0,
)

festival = st.selectbox(
    "Festival",
    [
        "No",
        "Yes",
    ],
)

city = st.selectbox(
    "City",
    [
        "Metropolitian",
        "Urban",
        "Semi-Urban",
        "Unknown",
    ],
)

st.subheader("Location")
restaurant_latitude = st.number_input(
    "Restaurant latitude",
    value=22.745,
    format="%.6f",
)

restaurant_longitude = st.number_input(
    "Restaurant longitude",
    value=75.892,
    format="%.6f",
)

delivery_latitude = st.number_input(
    "Delivery latitude",
    value=22.765,
    format="%.6f",
)

delivery_longitude = st.number_input(
    "Delivery longitude",
    value=75.912,
    format="%.6f",
)

st.subheader("Order information")

order_date = st.date_input(
    "Order date",
    value=date.today(),
)
order_time = st.time_input(
    "Order time",
    value=time(12, 0),
)
pickup_time = st.time_input(
    "Pickup time",
    value=time(12, 15),
)

if st.button("Predict"):
    payload = {
        "Delivery_person_Age": age,
        "Delivery_person_Ratings": rating,
        "Restaurant_latitude": restaurant_latitude,
        "Restaurant_longitude": restaurant_longitude,
        "Delivery_location_latitude": delivery_latitude,
        "Delivery_location_longitude": delivery_longitude,
        "Order_Date": order_date.isoformat(),
        "Time_Orderd": order_time.isoformat(),
        "Time_Order_picked": pickup_time.isoformat(),
        "Vehicle_condition": vehicle_condition,
        "Weatherconditions": weather,
        "Road_traffic_density": traffic,
        "Type_of_order": order_type,
        "Type_of_vehicle": vehicle_type,
        "multiple_deliveries": multiple_deliveries,
        "Festival": festival,
        "City": city,
    }
    try:
        response = requests.post(
            API_URL,
            json=payload,
        )
        if response.status_code == 200:
            result = response.json()
            prediction = result["predicted_delivery_time_minutes"]
            st.success(f"Predicted delivery time: " f"{prediction:.2f} minutes")
        else:
            st.error(f"API error: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server.")
