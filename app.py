from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Replace with your OpenAI API Key
openai.api_key = "your_openai_api_key"

@app.route('/')
def home():
    return render_template('index.html')  # Loads the chatbot interface

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')  # Get user message from frontend
    if not user_message:
        return jsonify({"reply": "Please enter a valid message."})

    try:
        # Call OpenAI API for response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"User: {user_message}\nAI:",
            max_tokens=150,
            temperature=0.7
        )
        bot_reply = response.choices[0].text.strip()
        return jsonify({"reply": bot_reply})  # Send the AI's reply back to frontend
    except openai.error.OpenAIError as e:
        print(f"OpenAI Error: {str(e)}")  # Log OpenAI-specific errors
        return jsonify({"reply": "Sorry, there was an issue with the AI service. Please try again later."})
    except Exception as e:
        print(f"General Error: {str(e)}")  # Log general errors
        return jsonify({"reply": "Sorry, an unexpected error occurred. Please try again later."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT provided by the hosting platform
    app.run(debug=True, host='0.0.0.0', port=port)
