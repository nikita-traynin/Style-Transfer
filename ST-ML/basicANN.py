import torch
from torch import nn
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from torch.optim.lr_scheduler import StepLR

# Hyperparameters
n_epochs = 10
batch_size = 50
lr = 0.07

# Load in the data
trans = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (1.0,))])
mnist_train_dataset = MNIST("./", train=True, download=True, transform=trans)
mnist_test_dataset = MNIST("./", train=False, download=True, transform=trans)
train_dataloader = DataLoader(mnist_train_dataset, batch_size=50, shuffle=True)
test_dataloader = DataLoader(mnist_test_dataset, shuffle=False)


# Define the model
class MyNN(nn.Module):
    def __init__(self):
        super(MyNN, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(784, 300),
            nn.ReLU(),
            nn.Linear(300, 10),
            nn.ReLU(),
            # nn.Linear(50, 10),
            # nn.ReLU(),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


model = MyNN()
CELoss = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(params=model.parameters(), lr=lr)
scheduler = StepLR(optimizer, step_size=1, gamma=0.75)

rows, columns = 3, 3
test_indices = torch.randint(0, 10000, (rows*columns,))


def test():
    total_count = mnist_test_dataset.data.size()[0]
    correct_count = 0
    for x, y in test_dataloader:
        output = model(x)
        result = int(torch.argmax(output))
        if result == y:
            correct_count += 1
    return correct_count / total_count


def display_sample():
    fig, axs = plt.subplots(rows, columns)
    disp_transform = transforms.ToPILImage()
    for idx, disp_idx in enumerate(test_indices):
        img = disp_transform(mnist_test_dataset.data[disp_idx])
        label = int(torch.argmax(model(mnist_test_dataset[disp_idx][0])))
        x, y = idx // rows, idx % columns
        axs[x, y].imshow(img, cmap='gray')
        axs[x, y].set_title(label)
    plt.show()


for epoch in range(n_epochs):
    i = 1
    total_loss = 0

    # Training loop
    for batch_x, batch_y in train_dataloader:
        optimizer.zero_grad()

        outputs = model(batch_x)
        loss = CELoss(outputs, batch_y)
        total_loss += loss.detach().numpy()

        loss.backward()
        optimizer.step()

        if i % 100 == 0:
            print("Epoch: " + str(epoch) + ", Done with batch: " + str(i))
        i += 1

    # Print results and decay learning rate
    print("Done with Epoch: " + str(epoch) + ", total loss: " + str(total_loss))
    scheduler.step()

    # Testing
    print("Test accuracy: " + str(test()) + ". ")
    display_sample()





