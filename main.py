import random
import namegenerator
import hashlib as hasher
import torch
import torch.nn as nn
import torch.optim as optim
import numpy

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

blockchain = [create_genesis_block()]
blockchain1=[create_genesis_block()]
previous_block = blockchain[0]
previous_block1=blockchain1[0]
num_of_blocks_to_add = 100

for i in range(0,num_of_blocks_to_add):
    name = namegenerator.gen()
    age = random.randint(18, 80)
    gender = random.choice(['Male', 'Female'])
    medical_history = random.choice(['None', 'Hypertension', 'Diabetes', 'Asthma','Anxiety','Covid'])
    label = random.randint(0,1)
    block_to_add = next_block(previous_block1, name, age, gender, medical_history, label)
    blockchain1.append(block_to_add)
    previous_block1 = block_to_add
    '''
    # print("Name: {}\n".format(block_to_add.name))
    # print("Age: {}\n".format(block_to_add.age))
    # print("Gender: {}\n".format(block_to_add.gender))
    # print("Medical History: {}\n".format(block_to_add.medical_history))
    # print("Label: {}\n".format(block_to_add.label))
    # print("Hash: {}\n".format(block_to_add.hash))
    '''
for i in range(num_of_blocks_to_add+1,num_of_blocks_to_add):
    name = namegenerator.gen()
    age = random.randint(18, 80)
    gender = random.choice(['Male', 'Female'])
    medical_history = random.choice(['None', 'Hypertension', 'Diabetes', 'Asthma'])
    label = random.randint(0,1)
    block_to_add = next_block(previous_block, name, age, gender, medical_history, label)
    blockchain.append(block_to_add)
    previous_block = block_to_add

datasets = []

for i in range(len(blockchain)):
    datasets.append((torch.tensor([blockchain[i].age]), torch.tensor([blockchain[i].label])))

def train(iterations=1,callback=None):
    model = nn.Linear(1,1)
    optimizer = optim.SGD(params = model.parameters(), lr = 0.01)
    for iter in range(iterations):
        for data, target  in datasets:
            optimizer.zero_grad()
            pred = model(data.float())
            loss = (( pred - target.float()) ** 2).sum()
            loss.backward()
            optimizer.step()
            # print("Loss : {}\n".format(loss.item()))
            # return format(loss.item())
            
            if callback:
                callback(loss.item())

train()