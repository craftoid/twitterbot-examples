""" Talk to Alice on the Commandline (German AIML) """
import aiml

alice = aiml.Kernel()
alice.learn("german.aiml")

prompt = ">  "
while True:
    question = raw_input(prompt)
    response = alice.respond(question)
    print(response)
