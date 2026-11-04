
from flask import Flask, jsonify

app = Flask(__name__)


def add(a, b):
    return a + b

# adding comment so that i can push on github to check if codebuild is working fine 
# webhook test for automatic build trigger
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
def multiply(a, b):
    return a * b

@app.route("/")
def home():
    return jsonify({
        "message": "CodeBuild CI/CD Demo",
        "status": "running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
