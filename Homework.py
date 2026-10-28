def echo(message):
    if message.text == "hi":
        return "Hello!"
    elif message.text == "bye":
        return "bye!"
    else:
        return "Unknown message"

class Message:
    def __init__(self, text):
        self.text = text

nachricht = Message("hi")
antwort = echo(nachricht)
print(antwort)

nachricht = Message("bye")
antwort = echo(nachricht)
print(antwort)