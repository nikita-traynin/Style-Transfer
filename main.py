import matplotlib.pyplot as plt
from PIL import Image
import torch
from torchvision import transforms, models
import numpy as np
from torch import optim

# Original 2016 paper by Gatys et al: https://arxiv.org/pdf/1508.06576.pdf
# Wikipedia: https://en.wikipedia.org/wiki/Neural_Style_Transfer

# Choose the images you want to work with
style_image_name = 'the-scream.jpg'
content_image_name = 'northwest-landscape.jpg'

#
if torch.cuda.is_available():
    dev = torch.device('cuda')
else:
    dev = torch.device('cpu')

# Get the original VGG net model (only the feature extraction layers)
vgg19 = models.vgg19(pretrained=True).features
vgg19.to(dev)

# Freeze the network parameters since it is pretrained and we aren't transfer learning
for param in vgg19.parameters():
    param.requires_grad_(False)


def load_image(image_path):
    image = Image.open(image_path).convert('RGB')
    in_transform = transforms.Compose([transforms.Resize(224),
                                       transforms.CenterCrop(224),
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.485, 0.456, 0.406),
                                                            (0.229, 0.224, 0.225))])
    image = in_transform(image).unsqueeze(0)
    print(image.shape)
    return image


def get_features(image, model, layers=None):
    """
    Run an image forward through a model and get the features for a set of layers.
    """

    # Label the relevant layers that can be used for style and content
    if layers is None:
        layers = {'0': 'conv1_1',
                  '5': 'conv2_1',
                  '10': 'conv3_1',
                  '19': 'conv4_1',
                  '21': 'conv4_2',
                  '28': 'conv5_1'}

    features = {}
    x = image
    # model._modules is a dictionary holding each module in the model
    for name, layer in model._modules.items():
        x = layer(x)
        if name in layers:
            features[layers[name]] = x

    return features


def gram_matrix(tensor):
    # Ignore batch size since it is 1 in this case
    _, c, h, w = tensor.shape

    # Vectorize the feature, c is the channel count or "depth"
    tensor_v = tensor.view(c, h*w)

    # Compute the gram matrix
    gram = torch.mm(tensor_v, tensor_v.transpose(0, 1))

    return gram

def show_image(tensor):
    # Get rid of batch dimension, rearrange dimensions into matplot and numpy standard
    image = np.transpose(tensor.squeeze(0).clone().detach().numpy(), axes=(1, 2, 0))

    # Un-scale image and clip the pixel values
    image = image * np.array((0.229, 0.224, 0.225)) + np.array((0.485, 0.456, 0.406))
    image = image.clip(0, 1)

    # display the image
    plt.imshow(image)
    plt.show()

    return image



# Get the image paths
style_path = 'img/style/' + style_image_name
content_path = 'img/content/' + content_image_name

# Pre-process the images
style_image = load_image(style_path).to(dev)
content_image = load_image(content_path).to(dev)

# Display them
show_image(style_image)
show_image(content_image)

# Get relevant features (dicts)
content_features = get_features(content_image, vgg19)
style_features = get_features(style_image, vgg19)

# Get the style gram matrices for relevant layers
style_grams = {layer: gram_matrix(style_features[layer]) for layer in style_features}

# Set weights for each "style" layer as prescribed in the paper
# Have them add up to one, keep them equal for now but can experiment
style_weights = {'conv1_1': 1.0,
                 'conv2_1': 0.8,
                 'conv3_1': 0.4,
                 'conv4_1': 0.2,
                 'conv5_1': 0.1}

# Set weight for loss function
content_weight = 1  # alpha
style_weight = 2e5  # beta

# The image we are generating
target_image = content_image.clone().requires_grad_(True).to(dev)

# Use ADAM (Adagrad + RMSProp combination since 2015)
optimizer = optim.Adam([target_image], lr=0.003)

# The number of iterations we run
steps = 1000

# Interval for displaying intermediate results
display_interval = 50 # for now: no displaying to avoid blocking

for iter_count in range(1, steps+1):
    target_features = get_features(target_image, vgg19)

    content_loss = torch.mean((content_features['conv4_2'] - target_features['conv4_2'])**2)

    #initialize the style loss
    style_loss = 0

    # Weighted sum of the target style gram matrices
    for layer in style_weights:
        _, c, h, w = target_features[layer].shape
        style_loss += (1 / (4 * h * h * w * w)) * style_weights[layer] * torch.mean((gram_matrix(style_features[layer]) - gram_matrix(target_features[layer]))**2)


    total_loss = content_weight * content_loss + style_weight * style_loss

    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()

    if iter_count % display_interval == 0:
        show_image(target_image)

# Now our target image has been created; let's save it
final_image = Image.fromarray((show_image(target_image) * 255).astype(np.uint8))
final_image.save('img/output/' + content_image_name[:-4] + '-' + style_image_name[:-4] + '.jpg')
