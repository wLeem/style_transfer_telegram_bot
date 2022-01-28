import os
import argparse
from PIL import Image
import torch
from torchvision import transforms
from torchvision.utils import save_image
import model_adain

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

trans = transforms.Compose([transforms.ToTensor(),
                            normalize])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def denorm(tensor, device):
    std = torch.Tensor([0.229, 0.224, 0.225]).reshape(-1, 1, 1).to(device)
    mean = torch.Tensor([0.485, 0.456, 0.406]).reshape(-1, 1, 1).to(device)
    res = torch.clamp(tensor * std + mean, 0, 1)
    return res


# model = model_adain.Model()
#     if model_state_path is not None:
#         model.load_state_dict(torch.load(model_state_path, map_location=lambda storage, loc: storage))
#     model = model.to(device)

# model.load_state_dict(torch.load(''))

# c = Image.open('')
# s = Image.open('')

# c_tensor = trans(c).unsqueeze(0).to(device)
# s_tensor = trans(s).unsqueeze(0).to(device)
# alpha = 1
# with torch.no_grad():
#     out = model.generate(c_tensor, s_tensor, alpha)

# out = denorm(out, device)

# output_name = '.'
# save_image(out, f'{output_name}.jpg', nrow=1)

# print(f'result saved into files starting with {output_name}')


def transfering_style(massiv_photo):
    model = model_adain.Model()
    model.load_state_dict(torch.load('20_epoch.pth', map_location=torch.device('cpu')))
    c = Image.open(massiv_photo[1])
    s = Image.open(massiv_photo[0])
    size = 650, 650
    c.thumbnail(size, Image.ANTIALIAS)
    s.thumbnail(size, Image.ANTIALIAS)
    c_tensor = trans(c).unsqueeze(0).to(device)
    s_tensor = trans(s).unsqueeze(0).to(device)
    alpha = 1
    with torch.no_grad():
        out = model.generate(c_tensor, s_tensor, alpha)
    out = denorm(out, device)
    return out
