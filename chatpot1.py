from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# إعداد البيئة
load_dotenv()

subscription_key = os.getenv("SUBSCRIPTION_KEY")
endpoint = os.getenv("ENDPOINT")
project_name = os.getenv("PROJECT_NAME")
deployment_name = os.getenv("DEPLOYMENT_NAME")

url = f"{endpoint}language/:query-knowledgebases?projectName={project_name}&deploymentName={deployment_name}&api-version=2021-10-01"

app = Flask(__name__)

# 🟢 صفحة واجهة المستخدم
@app.route("/")
def home():
    return render_template("chat.html")

# 🔵 API بترد على السؤال
@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Please provide a question in the JSON body."}), 400

    question = data["question"]

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json"
    }

    payload = {
        "question": question,
        "top": 1
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        answers = response.json().get("answers", [])
        if answers:
            return jsonify({"question": question, "answer": answers[0]["answer"]})
        else:
            return jsonify({"question": question, "answer": "No answer found."})
    else:
        return jsonify({"error": "Failed to connect to Azure QnA", "details": response.text}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)