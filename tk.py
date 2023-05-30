import tkinter as tk
import random
import namegenerator
import hashlib as hasher
import torch
import torch.nn as nn
import torch.optim as optim
import main

class Block:
    def __init__(self, name, age, gender, medical_history, label):
        self.name = name
        self.age = age
        self.gender = gender
        self.medical_history = medical_history
        self.label = label
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.name).encode('utf-8') +
                   str(self.age).encode('utf-8') +
                   str(self.gender).encode('utf-8') +
                   str(self.medical_history).encode('utf-8') +
                   str(self.label).encode('utf-8'))
        return sha.hexdigest()

def create_genesis_block():
    name = "Genesis"
    age = 0
    gender = ""
    medical_history = ""
    label = 0
    return Block(name, age, gender, medical_history, label)

def next_block(last_block, name, age, gender, medical_history, label):
    this_name = name
    this_age = age
    this_gender = gender
    this_medical_history = medical_history
    this_label = label
    this_hash = last_block.hash
    return Block(this_name, this_age, this_gender, this_medical_history, this_label)

def add_blocks(num_blocks):
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]

    for _ in range(num_blocks):
        name = namegenerator.gen()
        age = random.randint(18, 80)
        gender = random.choice(['Male', 'Female'])
        medical_history = random.choice(['None', 'Hypertension', 'Diabetes', 'Asthma', 'Anxiety', 'Covid'])
        label = random.randint(0, 1)
        block_to_add = next_block(previous_block, name, age, gender, medical_history, label)
        blockchain.append(block_to_add)

        app.text_output.insert(tk.END, "Name: {}\n".format(block_to_add.name))
        app.text_output.insert(tk.END, "Age: {}\n".format(block_to_add.age))
        app.text_output.insert(tk.END, "Gender: {}\n".format(block_to_add.gender))
        app.text_output.insert(tk.END, "Medical History: {}\n".format(block_to_add.medical_history))
        app.text_output.insert(tk.END, "Label: {}\n".format(block_to_add.label))
        app.text_output.insert(tk.END, "Hash: {}\n".format(block_to_add.hash))

        # Scroll to the end of the text output
        app.text_output.see(tk.END)

def train_model():
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]
    num_of_blocks_to_add = 100

    for _ in range(num_of_blocks_to_add):
        name = namegenerator.gen()
        age = random.randint(18, 80)
        gender = random.choice(['Male', 'Female'])
        medical_history = random.choice(['None', 'Hypertension', 'Diabetes', 'Asthma'])
        label = random.randint(0, 1)
        block_to_add = next_block(previous_block, name, age, gender, medical_history, label)
        blockchain.append(block_to_add)
        previous_block = block_to_add

    datasets = []

    for i in range(len(blockchain)):
        datasets.append((torch.tensor([blockchain[i].age]), torch.tensor([blockchain[i].label])))

    def train(iterations=100):
        main.train()


class BlockChainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain App")

        # Create and configure GUI elements
        self.label_num_blocks = tk.Label(root, text="Number of Blocks:")
        self.entry_num_blocks = tk.Entry(root)

        self.label_num_iterations = tk.Label(root, text="Number of Iterations:")
        self.entry_num_iterations = tk.Entry(root)

        self.button_add_blocks = tk.Button(root, text="Add Blocks", command=self.add_blocks)
        self.button_train = tk.Button(root, text="Train", command=self.train_model)

        self.text_output = tk.Text(root, height=10, width=50)

        # Grid layout for GUI elements
        self.label_num_blocks.grid(row=0, column=0, padx=10, pady=5)
        self.entry_num_blocks.grid(row=0, column=1, padx=10, pady=5)
        self.button_add_blocks.grid(row=1, column=0, padx=10, pady=5)

        self.label_num_iterations.grid(row=0, column=2, padx=10, pady=5)
        self.entry_num_iterations.grid(row=0, column=3, padx=10, pady=5)
        self.button_train.grid(row=1, column=2, columnspan=2, padx=10, pady=5)

        self.text_output.grid(row=2, columnspan=4, padx=10, pady=5)

    def add_blocks(self):
        num_blocks = int(self.entry_num_blocks.get())

        add_blocks(num_blocks)

        self.text_output.insert(tk.END, "Blocks added.\n")
        self.text_output.insert(tk.END, "--------------------------\n")
        

        # Clear the entry field
        self.entry_num_blocks.delete(0, tk.END)

    def train_model(self):
        num_iterations = int(self.entry_num_iterations.get())

        self.text_output.insert(tk.END, "Model training started...\n")
        self.text_output.insert(tk.END, "--------------------------\n")

        def update_loss_value(loss):
            self.text_output.insert(tk.END, "Loss: {}\n".format(loss))
            self.text_output.see(tk.END)
            self.root.update()
        main.train(callback=update_loss_value)

        main.train(iterations=num_iterations, callback=update_loss_value)

        self.entry_num_iterations.delete(0, tk.END)


# Create the root window
root = tk.Tk()

# Set the window size and position
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Create an instance of the BlockChainApp
app = BlockChainApp(root)

# Start the GUI event loop
root.mainloop()