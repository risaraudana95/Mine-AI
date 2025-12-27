from flask import Flask, render_template, request, jsonify
import http.client
import json

app = Flask(__name__)

# Your Serper API key
SERPER_API_KEY = "3c2605613a47c4fc49e2d2f29d5484f4ba0a9cf4"

def search_internet(query: str) -> str:
    try:
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": query})
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        result = json.loads(data.decode("utf-8"))

        if "organic" in result and len(result["organic"]) > 0:
            return result["organic"][0].get("snippet", "No snippet found.")
        else:
            return "Sorry, I couldn’t find anything online."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_text = data.get("message", "").lower()

    # 🔹 Custom rules first
    if "who made you" in user_text:
        reply = "I was made by Risara Udana."
    elif "your name" in user_text:
        reply = "I’m Mine AI, your assistant."
    else:
        # fallback: search the internet
        reply = search_internet(user_text)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
