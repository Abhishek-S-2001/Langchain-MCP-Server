from flask import Flask, request, jsonify
from flasgger import Swagger
from agent.agent_executor import agent_executor

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/chat", methods=["POST"])
def handle_chat():
    """
    Interact with Healthcare AI Agent
    ---
    parameters:
      - name: input
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
    response = agent_executor.run(message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5002, debug=True)
