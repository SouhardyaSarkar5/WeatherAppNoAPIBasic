from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Map condition text to emoji icons
def get_icon(condition):
    condition = condition.lower()
    if "clear" in condition or "sun" in condition:
        return "☀️"
    elif "cloud" in condition or "overcast" in condition:
        return "☁️"
    elif "rain" in condition or "drizzle" in condition:
        return "🌧️"
    elif "storm" in condition or "thunder" in condition:
        return "⛈️"
    elif "snow" in condition or "sleet" in condition:
        return "❄️"
    elif "fog" in condition or "mist" in condition or "haze" in condition:
        return "🌫️"
    elif "wind" in condition:
        return "💨"
    else:
        return "❓"


def fetch_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%l|%C|%t|Humidity:%h|Wind:%w"
        res = requests.get(url)
        if res.status_code == 200:
            raw = res.text.strip().split("|")
            condition = raw[1].strip()
            return {
                "location": raw[0].strip(),
                "condition": condition,
                "temp": raw[2].strip(),
                "humidity": raw[3].strip(),
                "wind": raw[4].strip(),
                "icon": get_icon(condition)
            }
        return None
    except Exception as e:
        print("Error fetching weather:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        weather = fetch_weather(city)
        if not weather:
            error = "Couldn't fetch weather for that city."
    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
