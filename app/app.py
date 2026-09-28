import os
from datetime import date, time
import requests
import streamlit as st

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000/predict",
)
st.set_page_config(
    page_title="Delivery Time Prediction",
    layout="wide",
)
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        div[data-testid="stMetric"] {
            background-color: rgba(128, 128, 128, 0.08);
            border: 1px solid rgba(128, 128, 128, 0.20);
            padding: 20px;
            border-radius: 12px;
        }

        div[data-testid="stForm"] {
            border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 14px;
            padding: 24px;
        }

        .section-description {
            color: #888;
            margin-top: -12px;
            margin-bottom: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Delivery Time Prediction")
st.write(
    "Enter the delivery information below to estimate " "the expected delivery time."
)
st.divider()
with st.form("prediction_form"):
    st.subheader("Courier information")
    st.markdown(
        '<p class="section-description">'
        "Information about the delivery person and vehicle."
        "</p>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input(
            "Delivery person age",
            min_value=18,
            max_value=80,
            value=30,
        )
    with col2:
        rating = st.number_input(
            "Delivery person rating",
            min_value=0.0,
            max_value=5.0,
            value=4.5,
            step=0.1,
        )
    with col3:
        vehicle_condition = st.selectbox(
            "Vehicle condition",
            [0, 1, 2, 3],
            help="Vehicle condition category used by the model.",
        )
    st.divider()
    st.subheader("Delivery conditions")
    st.markdown(
        '<p class="section-description">'
        "Environmental and operational conditions for the delivery."
        "</p>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    with col1:
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
    with col2:
        traffic = st.selectbox(
            "Traffic density",
            [
                "Low",
                "Medium",
                "High",
                "Jam",
            ],
        )
    with col3:
        city = st.selectbox(
            "City type",
            [
                "Metropolitian",
                "Urban",
                "Semi-Urban",
                "Unknown",
            ],
        )
    col1, col2, col3 = st.columns(3)
    with col1:
        order_type = st.selectbox(
            "Order type",
            [
                "Snack",
                "Meal",
                "Drinks",
                "Buffet",
            ],
        )
    with col2:
        vehicle_type = st.selectbox(
            "Vehicle type",
            [
                "motorcycle",
                "scooter",
                "electric_scooter",
                "bicycle",
            ],
        )
    with col3:
        festival = st.selectbox(
            "Festival",
            [
                "No",
                "Yes",
            ],
        )
    multiple_deliveries = st.number_input(
        "Number of additional deliveries",
        min_value=0,
        value=0,
        help="Number of simultaneous deliveries handled by the courier.",
    )
    st.divider()
    st.subheader("Delivery route")
    st.markdown(
        '<p class="section-description">'
        "Restaurant and customer GPS coordinates."
        "</p>",
        unsafe_allow_html=True,
    )
    restaurant_col, customer_col = st.columns(2)
    with restaurant_col:
        st.markdown("#### Restaurant")
        restaurant_latitude = st.number_input(
            "Restaurant latitude",
            value=22.745000,
            format="%.6f",
        )
        restaurant_longitude = st.number_input(
            "Restaurant longitude",
            value=75.892000,
            format="%.6f",
        )
    with customer_col:
        st.markdown("#### Customer")
        delivery_latitude = st.number_input(
            "Delivery latitude",
            value=22.765000,
            format="%.6f",
        )
        delivery_longitude = st.number_input(
            "Delivery longitude",
            value=75.912000,
            format="%.6f",
        )
    st.divider()
    st.subheader("Order timing")
    st.markdown(
        '<p class="section-description">' "Date, order time, and pickup time." "</p>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        order_date = st.date_input(
            "Order date",
            value=date.today(),
        )
    with col2:
        order_time = st.time_input(
            "Order time",
            value=time(12, 0),
        )
    with col3:
        pickup_time = st.time_input(
            "Pickup time",
            value=time(12, 15),
        )
    st.write("")
    submitted = st.form_submit_button(
        "Predict delivery time",
        use_container_width=True,
        type="primary",
    )

if submitted:
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
    with st.spinner("Calculating delivery time..."):
        try:
            response = requests.post(
                API_URL,
                json=payload,
                timeout=10,
            )
            if response.status_code == 200:
                result = response.json()
                prediction = result["predicted_delivery_time_minutes"]
                st.success("Prediction completed successfully.")
                st.metric(
                    label="Estimated delivery time",
                    value=f"{prediction:.2f} minutes",
                )
            else:
                st.error(f"API error ({response.status_code})")
                st.code(response.text)
        except requests.exceptions.ConnectionError as error:
            st.error("Could not connect to the FastAPI server.")
            st.code(str(error))
        except requests.exceptions.Timeout:
            st.error("The API request timed out.")
        except requests.exceptions.RequestException as error:
            st.error("An unexpected API error occurred.")
            st.code(str(error))
