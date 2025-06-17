import requests

DB_API_URL = "http://127.0.0.1:5000/api/db/ai"

def search_services_by_type(service):
    try:
        response = requests.get(f"{DB_API_URL}/services", params={"type": service})
        response.raise_for_status()  # will raise exception if 4xx/5xx
        results = response.json()

        # Ensure response is a list of dicts
        if not isinstance(results, list):
            return f"❌ Unexpected response format: {results}"

        if not results:
            return "❌ No services found."

        return "\n".join([
            f"{r.get('offering_name', 'N/A')} at {r.get('company_name', 'N/A')} ({r.get('location', 'N/A')})"
            for r in results
        ])

    except Exception as e:
        return f"❌ Error calling search service: {str(e)}"

def book_appointment_by_input(input_str):
    return "🛠 Booking support is coming soon. Please provide a structured booking JSON."
