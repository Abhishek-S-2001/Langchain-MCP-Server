import requests
import re
import json
from datetime import datetime, timedelta

DB_API_URL = "http://127.0.0.1:5000/api/db/ai"
BOOKING_API_URL = "http://127.0.0.1:5000/bookings"

booking_context = {}

def extract_service_and_location(query):
    match = re.match(r"(.+?)\s+(?:in\s+)?(.+)", query, re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return query.strip(), None

def search_services_by_type(service_input):
    try:
        service, location = extract_service_and_location(service_input)
        params = {"type": service}
        if location:
            params["location"] = location

        response = requests.get(f"{DB_API_URL}/services", params=params)
        response.raise_for_status()
        results = response.json()

        # ✅ Updated here to handle response dict with 'services' key
        if isinstance(results, dict) and "services" in results:
            results = results["services"]

        if not isinstance(results, list):
            return f"❌ Unexpected response format: {results}"
        if not results:
            return f"❌ No services found for '{service}' in '{location}'." if location else f"❌ No services found for '{service}'."

        return "\n".join([
            f"✅ {r.get('offering_name', 'N/A')} at {r.get('company_name', 'N/A')} ({r.get('location', 'N/A')})"
            for r in results
        ])
    except Exception as e:
        return f"❌ Error while searching services: {str(e)}"

def get_hourly_slots(start="09:00", end="17:00"):
    fmt = "%H:%M"
    start_time = datetime.strptime(start, fmt)
    end_time = datetime.strptime(end, fmt)
    slots = []
    while start_time < end_time:
        end_slot = start_time + timedelta(hours=1)
        slots.append({
            "start": start_time.strftime(fmt),
            "end": end_slot.strftime(fmt)
        })
        start_time = end_slot
    return slots

def book_appointment_by_input(input_str):
    global booking_context
    try:
        if input_str.strip().lower().startswith("slot"):
            slot_number = int(re.findall(r"\d+", input_str)[0]) - 1
            slots = booking_context.get("slots", [])
            if 0 <= slot_number < len(slots):
                selected = slots[slot_number]
                payload = {
                    "provider_offering_id": booking_context["provider_offering_id"],
                    "user_id": booking_context["user_id"],
                    "appointment_date": booking_context["appointment_date"],
                    "appointment_start_time": selected["start"],
                    "appointment_end_time": selected["end"],
                    "status": "confirmed",
                    "notes": booking_context.get("notes", "")
                }
                res = requests.post(BOOKING_API_URL, json=payload)
                res.raise_for_status()
                return f"✅ Appointment confirmed on {payload['appointment_date']} from {selected['start']} to {selected['end']}."
            return "❌ Invalid slot number."

        data = json.loads(input_str)
        required_keys = {"provider_offering_id", "user_id", "appointment_date"}
        if not required_keys.issubset(data):
            return "❌ Missing provider_offering_id, user_id or appointment_date."

        slots = get_hourly_slots()
        booking_context = {
            "provider_offering_id": data["provider_offering_id"],
            "user_id": data["user_id"],
            "appointment_date": data["appointment_date"],
            "slots": slots,
            "notes": data.get("notes", "")
        }

        response = f"🗓 Available hourly slots on {data['appointment_date']}:\n"
        for i, s in enumerate(slots):
            response += f"{i+1}. {s['start']} - {s['end']}\n"
        response += "\nReply with 'Slot <number>' to confirm."
        return response

    except Exception as e:
        return f"❌ Error: {str(e)}"
