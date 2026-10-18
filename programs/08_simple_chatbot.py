"""Lab 1 - Program 8: A small rule-based chatbot."""

print("AI Lab Chatbot")
print("Type a message, or type 'quit' to stop.")
print("Try: hello, your name, python, ai, bye")

replies = {
    "hello": "Hello! I am a small rule-based chatbot.",
    "hi": "Hi! How can I help you with Lab 1?",
    "your name": "My name is LabBot. I only know a few replies.",
    "python": "Python is the language we are using in Google Colab.",
    "ai": "Artificial intelligence lets computers learn patterns and make decisions.",
    "bye": "Goodbye! Good luck with your lab.",
}

while True:
    message = input("You: ").strip().lower()
    if message in ("quit", "exit", "bye"):
        print("LabBot: Goodbye!")
        break
    if message in replies:
        print("LabBot:", replies[message])
    else:
        print("LabBot: I do not know that yet. Try hello, python, or ai.")
