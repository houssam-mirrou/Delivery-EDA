from datetime import date, time
from typing import Literal

from pydantic import BaseModel, Field


class DeliveryPredictionRequest(BaseModel):

    Delivery_person_Age: float = Field(gt=0)

    Delivery_person_Ratings: float = Field(
        ge=0,
        le=5,
    )

    Restaurant_latitude: float = Field(
        ge=-90,
        le=90,
    )

    Restaurant_longitude: float = Field(
        ge=-180,
        le=180,
    )

    Delivery_location_latitude: float = Field(
        ge=-90,
        le=90,
    )

    Delivery_location_longitude: float = Field(
        ge=-180,
        le=180,
    )

    Order_Date: date

    Time_Orderd: time

    Time_Order_picked: time

    Vehicle_condition: int = Field(
        ge=0,
        le=3,
    )

    Weatherconditions: Literal[
        "Sunny",
        "Stormy",
        "Sandstorms",
        "Cloudy",
        "Fog",
        "Windy",
    ]

    Road_traffic_density: Literal[
        "Low",
        "Medium",
        "High",
        "Jam",
    ]

    Type_of_order: Literal[
        "Snack",
        "Meal",
        "Drinks",
        "Buffet",
    ]

    Type_of_vehicle: Literal[
        "motorcycle",
        "scooter",
        "electric_scooter",
        "bicycle",
    ]

    multiple_deliveries: int = Field(
        ge=0,
    )

    Festival: Literal[
        "No",
        "Yes",
    ]

    City: Literal[
        "Metropolitian",
        "Urban",
        "Semi-Urban",
        "Unknown",
    ]
