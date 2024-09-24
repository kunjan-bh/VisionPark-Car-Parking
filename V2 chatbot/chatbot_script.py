import sys

def get_response(prompt):
    # Replace this with your actual chatbot logic
    return f"Chatbot Response: {prompt}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_message = sys.argv[1]
        print(get_response(user_message))
