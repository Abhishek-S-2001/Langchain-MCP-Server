import requests
import os
from agent.memory_store import MemoryStore  # New: To track options

DB_API_URL = "http://127.0.0.1:5000/api/db/ai"

memory_store = MemoryStore()

def search_services_by_type(service, location=""):
    try:
        response = requests.get(f"{DB_API_URL}/services", params={"type": service, "location": location})
        response.raise_for_status()
        results = response.json().get("services", [])

        if not results:
            return "❌ No services found."

        memory_store.last_service_options = {str(idx + 1): r for idx, r in enumerate(results)}

        formatted = []
        for idx, r in enumerate(results):
            option_num = idx + 1
            formatted.append(
                f"{option_num}️⃣ [{r.get('provider_name', 'N/A')} - {r.get('service_name', 'N/A')}]\n"
                f"📍 Location: {r.get('location', {}).get('name', 'N/A')}, {r.get('location', {}).get('city', 'N/A')}\n"
                f"📏 Distance: {round(r.get('distance_km', 0), 2)} km\n"
                f"💲 Price: ₹{r.get('price', 'N/A')}\n"
                f"🕐 Availability: {r.get('availability_hours', 'N/A')}\n"
            )

        return f"Here are the available options for \"{service}\":\n\n" + "\n".join(formatted) + "\n\nPlease reply with the option number to proceed with booking."

    except Exception as e:
        return f"❌ Error calling search service: {str(e)}"

def book_appointment_by_input(selected_option: str, user_note: str = ""):
    try:
        if selected_option not in memory_store.last_service_options:
            return "❌ Invalid selection. Please choose a valid option."

        selected_service = memory_store.last_service_options[selected_option]

        booking_payload = {
            "user_id": "user-123",  # Replace with real user_id if available
            "provider_offering_id": selected_service["provider_offering_id"],
            "appointment_date": "2025-07-01",  # You can make this dynamic
            "appointment_start_time": "10:00",
            "appointment_end_time": "11:00",
            "notes": user_note
        }

        response = requests.post(f"{DB_API_URL}/book", json=booking_payload)
        response.raise_for_status()

        return f"✅ Your booking request for {selected_service['service_name']} at {selected_service['provider_name']} has been placed successfully."

    except Exception as e:
        return f"❌ Error booking appointment: {str(e)}"
