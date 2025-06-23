import streamlit as st
import requests

# Replace this with your actual Google Maps API Key
API_KEY = "AIzaSyC7vWtHhPzTbwhH9KAFwXWMuSL8o1p5rFs"

# Sample warehouse data
warehouses = [
    {"name": "Delhi", "location": "Delhi, India", "has_stock": True},
    {"name": "Mumbai", "location": "Mumbai, India", "has_stock": True},
    {"name": "Jaipur", "location": "Jaipur, India", "has_stock": False},  # Out of stock example
]

def get_delivery_info(origin, destination):
    """Use Google Maps Distance Matrix API to get distance and duration"""
    url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origin}&destinations={destination}&key={API_KEY}"
    )
    res = requests.get(url)
    data = res.json()
    try:
        info = data["rows"][0]["elements"][0]
        return {
            "distance_text": info["distance"]["text"],
            "distance_val": info["distance"]["value"],
            "duration_text": info["duration"]["text"],
            "duration_val": info["duration"]["value"],
        }
    except:
        return None

def find_best_warehouse(customer_location):
    """Greedy logic to find fastest + cheapest warehouse"""
    best_score = float("inf")
    best_wh = None

    for wh in warehouses:
        if not wh["has_stock"]:
            continue

        info = get_delivery_info(wh["location"], customer_location)
        if not info:
            continue

        # Simple greedy score = time (sec) + 1% of distance (meters)
        score = info["duration_val"] + 0.01 * info["distance_val"]

        if score < best_score:
            best_score = score
            best_wh = {
                "name": wh["name"],
                "distance": info["distance_text"],
                "duration": info["duration_text"],
                "score": round(score, 2),
            }

    return best_wh

# ---------------- Streamlit UI ------------------

st.title("📦 Polaris Order Fulfillment Optimizer")

customer_location = st.text_input("Enter Customer Location (e.g. Bangalore, India)")

if st.button("Find Best Warehouse") and customer_location:
    result = find_best_warehouse(customer_location)
    if result:
        st.success(f"✅ Best Warehouse: **{result['name']}**")
        st.write(f"📍 Distance: {result['distance']}")
        st.write(f"⏱ Delivery Time: {result['duration']}")
        st.write(f"🧠 Greedy Score: {result['score']}")
    else:
        st.error("No warehouse found or API error.")
