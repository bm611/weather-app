"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import os
import asyncio
import requests
import json
from rxconfig import config

API_KEY = os.environ["WEATHER_API_KEY"]


class State(rx.State):
    """The app state."""

    location: str = ""
    city: str = ""
    country: str = ""
    temp: str = ""
    speed: str = ""
    humidity: str = ""
    icon: str = "sun"
    show: bool = False

    user_input = ""

    def get_user_input(self, user_input):
        self.user_input = user_input

    async def get_weather(self):

        # switch show bool to display card on click
        self.show = True

        __city__: str = self.user_input
        response = requests.get(get_weather_request(__city__))
        if response.status_code == 200:
            data = response.json()

            self.city = __city__
            self.country = data["sys"]["country"]
            self.temp = f"{data['main']['temp']}°C"
            self.speed = f"{data['wind']['speed']} km/h"
            self.humidity = f"{data['main']['humidity']} %"

            self.location = f"{self.city.upper()}, {self.country.upper()}"

            if data["weather"][0]["main"].lower() in ["clear", "sun"]:
                self.icon = "sun"
            else:
                self.icon = "cloud"

            self.user_input = ""


def get_weather_request(city):
    return f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("WEATHER APP", size="8", weight="bold", color_scheme="gold"),
            rx.hstack(
                rx.input(
                    value=State.user_input,
                    on_change=State.get_user_input,
                    placeholder="Enter city name to get weather...",
                    color_scheme="tomato",
                    radius="large",
                    style={"width": "40vh"},
                ),
                rx.button("Submit", on_click=State.get_weather),
            ),
            rx.cond(
                State.show,
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.badge(
                                rx.match(
                                    State.icon,
                                    ("cloud", rx.icon("cloud", size=34)),
                                    ("sun", rx.icon("sun", size=34)),
                                ),
                                color_scheme="blue",
                                radius="full",
                                padding="0.7rem",
                            ),
                            rx.vstack(
                                rx.heading(
                                    State.temp,
                                    size="6",
                                    weight="bold",
                                ),
                                rx.text("temp", size="4", weight="medium"),
                                spacing="1",
                                height="100%",
                                align_items="center",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.heading(
                                    State.humidity,
                                    size="6",
                                    weight="bold",
                                ),
                                rx.text("humidity", size="4", weight="medium"),
                                spacing="1",
                                height="100%",
                                align_items="center",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.heading(
                                    State.speed,
                                    size="6",
                                    weight="bold",
                                ),
                                rx.text("wind", size="4", weight="medium"),
                                spacing="1",
                                height="100%",
                                align_items="center",
                                width="100%",
                            ),
                            height="100%",
                            spacing="5",
                            align="center",
                            justify="center",
                            width="100%",
                        ),
                        rx.code(State.location, variant="outline", size="5"),
                        align="center",
                        spacing="5",
                    ),
                    size="4",
                    width="100%",
                    max_width="40rem",
                ),
            ),
            spacing="5",
            align="center",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


style = {
    "font_family": "Monaspace Krypton",
    "font_size": "16px",
}

app = rx.App(
    stylesheets=[
        "/fonts/myfonts.css",
    ],
    style=style,
)
app.add_page(index)
