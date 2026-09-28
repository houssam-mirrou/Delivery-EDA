import numpy as np
import pandas as pd
from .schemas import DeliveryPredictionRequest

TRAFFIC_LEVEL_MAPPING = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Jam": 3,
}
RUSH_HOURS = {
    12,
    13,
    14,
    19,
    20,
    21,
}
def haversine_distance_km(
    latitude_1,
    longitude_1,
    latitude_2,
    longitude_2,
):
    earth_radius_km = 6371.0
    lat1 = np.radians(latitude_1)
    lon1 = np.radians(longitude_1)
    lat2 = np.radians(latitude_2)
    lon2 = np.radians(longitude_2)
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = (
        np.sin(delta_lat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2) ** 2
    )
    a = np.clip(a, 0, 1)
    c = 2 * np.arctan2(
        np.sqrt(a),
        np.sqrt(1 - a),
    )
    return earth_radius_km * c


def build_model_input(data: DeliveryPredictionRequest):
    distance_km = haversine_distance_km(
        data.Restaurant_latitude,
        data.Restaurant_longitude,
        data.Delivery_location_latitude,
        data.Delivery_location_longitude,
    )
    order_hour = data.Time_Orderd.hour
    pickup_hour = data.Time_Order_picked.hour
    order_day = data.Order_Date.day
    order_month = data.Order_Date.month

    order_day_of_week = data.Order_Date.weekday()
    is_weekend = int(order_day_of_week in [5, 6])
    order_minutes = (
        data.Time_Orderd.hour * 60
        + data.Time_Orderd.minute
        + data.Time_Orderd.second / 60
    )
    pickup_minutes = (
        data.Time_Order_picked.hour * 60
        + data.Time_Order_picked.minute
        + data.Time_Order_picked.second / 60
    )
    preparation_time = pickup_minutes - order_minutes
    if preparation_time < 0:
        preparation_time += 24 * 60
    traffic_level = TRAFFIC_LEVEL_MAPPING[data.Road_traffic_density]
    distance_x_traffic = distance_km * traffic_level
    distance_per_delivery = distance_km / (data.multiple_deliveries + 1)
    prep_to_distance_ratio = preparation_time / (distance_km + 1)
    is_rush_hour = int(order_hour in RUSH_HOURS)
    order_hour_sin = np.sin(2 * np.pi * order_hour / 24)
    order_hour_cos = np.cos(2 * np.pi * order_hour / 24)
    order_hour_sin2 = np.sin(2 * np.pi * 2 * order_hour / 24)
    order_hour_cos2 = np.cos(2 * np.pi * 2 * order_hour / 24)
    pickup_hour_sin = np.sin(2 * np.pi * pickup_hour / 24)
    pickup_hour_cos = np.cos(2 * np.pi * pickup_hour / 24)
    pickup_hour_sin2 = np.sin(2 * np.pi * 2 * pickup_hour / 24)
    pickup_hour_cos2 = np.cos(2 * np.pi * 2 * pickup_hour / 24)
    order_day_of_week_sin = np.sin(2 * np.pi * order_day_of_week / 7)
    order_day_of_week_cos = np.cos(2 * np.pi * order_day_of_week / 7)
    order_month_sin = np.sin(2 * np.pi * (order_month - 1) / 12)
    order_month_cos = np.cos(2 * np.pi * (order_month - 1) / 12)
    features = pd.DataFrame(
        [
            {
                "Delivery_person_Age": data.Delivery_person_Age,
                "Delivery_person_Ratings": data.Delivery_person_Ratings,
                "multiple_deliveries": data.multiple_deliveries,
                "Distance_km": distance_km,
                "Order_Day": order_day,
                "Preparation_Time_min": preparation_time,
                "Vehicle_condition": data.Vehicle_condition,
                "Traffic_Level": traffic_level,
                "Distance_x_Traffic": distance_x_traffic,
                "Distance_per_Delivery": distance_per_delivery,
                "Prep_to_Distance_Ratio": prep_to_distance_ratio,
                "Order_Hour_sin": order_hour_sin,
                "Order_Hour_cos": order_hour_cos,
                "Order_Hour_sin2": order_hour_sin2,
                "Order_Hour_cos2": order_hour_cos2,
                "Pickup_Hour_sin": pickup_hour_sin,
                "Pickup_Hour_cos": pickup_hour_cos,
                "Pickup_Hour_sin2": pickup_hour_sin2,
                "Pickup_Hour_cos2": pickup_hour_cos2,
                "Order_DayOfWeek_sin": order_day_of_week_sin,
                "Order_DayOfWeek_cos": order_day_of_week_cos,
                "Order_Month_sin": order_month_sin,
                "Order_Month_cos": order_month_cos,
                "Weatherconditions": data.Weatherconditions,
                "Type_of_order": data.Type_of_order,
                "Type_of_vehicle": data.Type_of_vehicle,
                "Festival": data.Festival,
                "City": data.City,
                "Order_Hour": order_hour,
                "Order_Month": order_month,
                "Order_DayOfWeek": order_day_of_week,
                "Pickup_Hour": pickup_hour,
                "Is_Weekend": is_weekend,
                "Is_Rush_Hour": is_rush_hour,
            }
        ]
    )
    return features
