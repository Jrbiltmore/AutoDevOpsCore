import threading
import time
import queue
import readline

from transformers import GPTJForCausalLM, GPTJTokenizerFast

# Define the conversation queue
conversation_queue = queue.Queue()

# Define the models and tokenizers
model_1 = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")
tokenizer_1 = GPTJTokenizerFast.from_pretrained("EleutherAI/gpt-j-6B")

model_2 = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")
tokenizer_2 = GPTJTokenizerFast.from_pretrained("EleutherAI/gpt-j-6B")

# Function to process user input and generate model responses
def process_input(model, tokenizer, role):
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break

        # Tokenize user input
        input_ids = tokenizer.encode(user_input, return_tensors="pt")

        # Generate model response
        output = model.generate(input_ids, max_length=100, num_return_sequences=1)
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        # Add the role to the response
        response_with_role = f"{role}: {response}"

        # Put the response in the conversation queue
        conversation_queue.put(response_with_role)

# Function to print the conversation
def print_conversation():
    while True:
        if not conversation_queue.empty():
            message = conversation_queue.get()
            print(message)
        time.sleep(0.1)

# Start the conversation printing thread
print_thread = threading.Thread(target=print_conversation)
print_thread.daemon = True
print_thread.start()

# Start the input processing threads for both models
thread_1 = threading.Thread(target=process_input, args=(model_1, tokenizer_1, "Model 1"))
thread_2 = threading.Thread(target=process_input, args=(model_2, tokenizer_2, "Model 2"))

thread_1.start()
thread_2.start()

# Wait for the input threads to complete
thread_1.join()
thread_2.join()

# Wait for the conversation printing thread to complete
print_thread.join()
