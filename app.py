from flask import Flask, render_template, request, jsonify
from groq import Groq
import json

app = Flask(__name__)

client = Groq(api_key="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")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/generate-idea", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        problem = data.get("problem", "")

        prompt = f"""
User problem: {problem}

Generate a professional startup idea with realistic financial projections.

Return ONLY valid JSON in this exact format:

{{
"ideaName":"",
"solution":"",
"targetAudience":"",
"marketingStrategy":"",
"revenueModel":"",
"budget":"",
"marketTrends":"",
"USP":"",
"profitLoss": {{
    "2021": 0,
    "2022": 0,
    "2023": 0,
    "2024": 0,
    "2025": 0
}}
}}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content.strip()

        try:
            result = json.loads(text)
        except:
            start = text.find("{")
            end = text.rfind("}") + 1
            result = json.loads(text[start:end])


        if "profitLoss" not in result:
            result["profitLoss"] = {
                "2021": -20000,
                "2022": 30000,
                "2023": 80000,
                "2024": 150000,
                "2025": 300000
            }

        return jsonify(result)

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "ideaName": "Error",
            "solution": str(e),
            "targetAudience": "",
            "marketingStrategy": "",
            "revenueModel": "",
            "budget": "",
            "marketTrends": "",
            "USP": "",
            "profitLoss": {
                "2021": 0,
                "2022": 0,
                "2023": 0,
                "2024": 0,
                "2025": 0
            }
        })

if __name__ == "__main__":
    app.run(debug=True)