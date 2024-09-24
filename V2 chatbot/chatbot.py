from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from load_creds import load_creds

app = Flask(__name__)
CORS(app)

# Load credentials
creds = load_creds()

# Configure the Generative AI client
genai.configure(credentials=creds)

# Specify your fine-tuned model ID
FINE_TUNED_MODEL_ID = 'tunedModels/visionparktrainingdata-6jsttsz2q0wn'

# Initialize the Generative AI model
model = genai.GenerativeModel(FINE_TUNED_MODEL_ID)

# Predefined responses for specific queries
def predefined_responses(query):
    query_lower = query.lower()

    # Specific rules for predefined questions
    if "who are you" in query_lower or "who you are" in query_lower:
        return "I am Vision Park Virtual Assistant."

    elif "what is vision park" in query_lower:
        return "Vision Park is a digital car parking booking system."

    elif "what can you do" in query_lower or "what you do" in query_lower:
        return "I can assist you with managing digital parking solutions, guide you on system usage, and provide support for Vision Park services."

    # Parking location related questions
    elif ("parking locations" in query_lower or 
          "where are the parking locations" in query_lower or 
          "what are the parking locations" in query_lower or 
          "can you tell me the locations" in query_lower or 
          "can you tell me the parking locations" in query_lower or 
          "well, can you tell me the parking locations" in query_lower):
        return "Vision Park has parking locations at Balaju, Maitidevi, and Newroad."

    elif "slots" in query_lower and ("balaju" in query_lower or "maitidevi" in query_lower or "newroad" in query_lower):
        if "balaju" in query_lower:
            return "The Balaju parking location has 0 slots available."
        elif "maitidevi" in query_lower:
            return "The Maitidevi parking location has 4 slots available."
        elif "newroad" in query_lower:
            return "The Newroad parking location has 0 slots available."

    elif "how many slots" in query_lower:
        return "Each of our parking locations (Balaju, Maitidevi, and Newroad) has 4 parking slots."

    elif "how many slots are available" in query_lower or "slots available" in query_lower:
        return "You can see it while booking or check it once at the booking page."
    elif "how can you help me" in query_lower or "help me" in query_lower:
        return "I can support you to know and guide you about parking service of Vision park"

    # Farewell responses
    elif "bye" in query_lower or "goodbye" in query_lower or "see you" in query_lower:
        return "Goodbye! Thank you for using Vision Park. Have a great day!"

    return None  # If no predefined response matches

@app.route("/chat", methods=["POST"])
def chat_with_ai():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400

    # Check for predefined responses
    predefined_response = predefined_responses(user_message)
    
    if predefined_response:
        return jsonify({"response": predefined_response}), 200

    try:
        # Create a new chat session or continue an existing one
        chat = model.start_chat(history=[])

        # Send the user message
        response = chat.send_message(user_message, stream=True)

        # Collect and combine the chunks from the stream
        bot_response = ""
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                bot_response += chunk.text

        if not bot_response:  # Handle case where response is empty
            return jsonify({"response": "Sorry, I couldn't generate a response."}), 200

        return jsonify({"response": bot_response}), 200

    except genai.types.generation_types.BrokenResponseError as e:
        # Handle case where the response is broken or flagged for safety
        return jsonify({"response": "The response was blocked due to safety concerns. Please try again."}), 200

    except Exception as e:
        # General error handling
        return jsonify({"response": "An error occurred, please try again."}), 500

if __name__ == "__main__":
    # app.run(port=5000, debug=True)
    app.run(host="0.0.0.0",port=5000, debug=True)
