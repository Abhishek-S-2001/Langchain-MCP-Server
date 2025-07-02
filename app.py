from flask import Flask, request, jsonify, render_template
from flasgger import Swagger
from agent.agent_executor import agent_executor

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
def chat_ui():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def handle_chat():
    data = request.json
    message = data.get("message", "")

    response = agent_executor.invoke({"input": message})

    return jsonify({"response": response["output"]})

if __name__ == "__main__":
    app.run(port=5002, debug=True)
