import test

while True:
    intpt = input("You: ")
    if intpt == "quit":
        break
    else:
        print(test.chatbot(intpt))