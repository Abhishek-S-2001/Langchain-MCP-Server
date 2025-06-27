from flask import Flask, request, jsonify
from flasgger import Swagger
from agent.agent_executor import agent_executor
from agent.tool import book_appointment_by_input  # direct API access to tool function

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/chat", methods=["POST"])
def handle_chat():
    """
    Interact with Healthcare AI Agent
    ---
    parameters:
      - name: message
        in: body
        required: true
        schema:
          type: object
          properties:
            message:
              type: string
    responses:
      200:
        description: Agent response
    """
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Missing 'message' field"}), 400

    try:
        response = agent_executor.run({"input": message})  # ✅ FIXED HERE
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if "I do not have access" in response:
        response += "\nℹ️ Tip: Try rephrasing your query like 'Find MRI in Pune' or 'Book an X-ray at ABC Clinic on July 5'."

    return jsonify({"response": response})

@app.route("/book-direct", methods=["POST"])
def direct_booking_api():
    """
    Direct Booking API (Bypasses LLM)
    ---
    parameters:
      - name: input
        in: body
        required: true
        schema:
          type: object
          properties:
            input:
              type: string
              description: JSON string with provider_offering_id, user_id, appointment_date, etc.
    responses:
      200:
        description: Booking tool response
    """
    data = request.get_json()
    input_str = data.get("input", "")
    result = book_appointment_by_input(input_str)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(port=5002, debug=True)
