import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.workflows.router_workflow import create_router_graph

app = Flask(__name__)
CORS(app)

@app.route("/answer", methods=["POST"])
def chat():
    """Handle chat requests and return responses"""
    data = request.json
    message = data.get("question", "")

    workflow = create_router_graph()
    state = {
        "message": message,
        "question_type": None,
        "response": None,
        "error": None
    }
    result = workflow.invoke(state)
    result = result["response"] if not result.get("error") else {"error": result["error"]}

    return jsonify({"response": result})


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return "OK", 200

if __name__ == "__main__":
    # Determine environment and set debug mode accordingly
    environment = os.getenv('ENVIRONMENT', 'production')
    host = os.getenv('SERVER_HOST', '0.0.0.0')
    port = os.getenv('SERVER_PORT', '5000')

    debug = environment == 'development'

    app.run(host=host, port=port, debug=debug)
