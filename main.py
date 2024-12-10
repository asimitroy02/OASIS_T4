import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as tkb
import xml.etree.ElementTree as ET


# 🌦️ get_weather function to fetch and parse XML data from API
def get_weather(city):
    API_key = "05f4ee67848cc2f2685db6e4c1cf5f3e"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&mode=xml&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error ❌", "City not found!")
        return None

    # 🌐 Parse XML response
    root = ET.fromstring(res.content)

    # City details
    city_name = root.find("city").get("name")
    country = root.find("city/country").text

    # Temperature and feels like
    temp = float(root.find("temperature").get("value")) - 273.15
    feels_like = float(root.find("feels_like").get("value")) - 273.15

    # Humidity and pressure
    humidity = root.find("humidity").get("value")
    pressure = root.find("pressure").get("value")

    # Wind details
    wind_direction = root.find("wind/direction").get("name")

    # Weather description and icon
    description = root.find("weather").get("value")
    icon_id = root.find("weather").get("icon")
    icon = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"

    return {
        "icon": icon, "temperature": temp, "feels_like": feels_like,
        "description": description, "city": city_name, "country": country,
        "humidity": humidity, "pressure": pressure, "wind_direction": wind_direction,
    }


# Function to update the background based on the weather condition
def update_background(weather_condition):
    backgrounds = {
        'clear sky': 'images/sunny.png',
        'rain': 'images/rainy.png',
        'clouds': 'images/cloudy.png',
        'haze': 'images/haze.png',
        'mist': 'images/mist.png'
    }

    image_path = backgrounds.get(weather_condition, 'images/default.png')
    update_background_image(image_path, root.winfo_width(), root.winfo_height())


def update_background_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resized_image)
    background_label.configure(image=background_image)
    background_label.image = background_image


# 🌡️ Search Function to fetch and display weather data
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    weather_description = result['description'].lower()
    update_background(weather_description)

    location_label.configure(text=f"{result['city']}, {result['country']}")

    # Fetch and display the icon image
    try:
        image = Image.open(requests.get(result["icon"], stream=True).raw)
        icon = ImageTk.PhotoImage(image)
        icon_label.configure(image=icon)
        icon_label.image = icon  # Store a reference to avoid garbage collection
    except Exception as e:
        print(f"Error loading icon: {e}")
        icon_label.configure(image='')

    # Update other weather details
    temperature_label.configure(text=f"Temperature: {result['temperature']:.2f}°C")
    feels_like_label.configure(text=f"Feels Like: {result['feels_like']:.2f}°C")
    description_label.configure(text=f"Description: {result['description']}")
    humidity_label.configure(text=f"Humidity: {result['humidity']}%")
    pressure_label.configure(text=f"Pressure: {result['pressure']} hPa")
    wind_direction_label.configure(text=f"Wind Direction: {result['wind_direction']}")

    # Show the labels after data is loaded
    location_label.pack(pady=20)
    icon_label.pack()
    temperature_label.pack()
    feels_like_label.pack()
    description_label.pack()
    humidity_label.pack()
    pressure_label.pack()
    wind_direction_label.pack()


# 🌤️ GUI setup
root = tkb.Window(themename="flatly")
root.title("Weather App ☀️🌧️🌡️")
root.geometry("400x800")
root.iconbitmap('empty.ico')

background_label = tk.Label(root)
background_label.place(relwidth=1, relheight=1)

update_background_image("images/default.png", root.winfo_width(), root.winfo_height())

# City Entry
city_entry = tkb.Entry(root, font="Helvetica 18")
city_entry.insert(0, "🏙️ Enter City Name")
city_entry.bind("<FocusIn>", lambda event: city_entry.delete(0, "end"))
city_entry.pack(pady=10)

search_btn = tkb.Button(root, text="Search 📌", command=search, bootstyle="Warning")
search_btn.pack(pady=10)

# Labels to display weather data
label_style = {'fg': 'black', 'bg': root.cget('bg')}  # Set foreground to black and background to match window

location_label = tk.Label(root, font="Helvetica 25", **label_style)
icon_label = tk.Label(root, **label_style)
temperature_label = tk.Label(root, font="Helvetica 20", **label_style)
feels_like_label = tk.Label(root, font="Helvetica 20", **label_style)
description_label = tk.Label(root, font="Helvetica 20", **label_style)
humidity_label = tk.Label(root, font="Helvetica 15", **label_style)
pressure_label = tk.Label(root, font="Helvetica 15", **label_style)
wind_direction_label = tk.Label(root, font="Helvetica 15", **label_style)

# Pack labels initially hidden
location_label.pack_forget()
icon_label.pack_forget()
temperature_label.pack_forget()
feels_like_label.pack_forget()
description_label.pack_forget()
humidity_label.pack_forget()
pressure_label.pack_forget()
wind_direction_label.pack_forget()

root.resizable(False, False)
root.mainloop()