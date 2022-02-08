import torch
from PIL import Image
import torchvision.transforms as transforms
import cv2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# photo_size = 128

def resize_photo(massiv_photo):
    imsize = 512 if torch.cuda.is_available() else 128

    loader = transforms.Compose([
        transforms.Resize(imsize),
        transforms.ToTensor()])

    def image_loader(image_name):
        image = cv2.imread(image_name, 1)
        image = cv2.resize(image, (128, 128), interpolation=cv2.INTER_NEAREST)
        image = loader(Image.fromarray(image)).unsqueeze(0)
        return image.to(device, torch.float)

    style_img = image_loader(massiv_photo[0])
    content_img = image_loader(massiv_photo[1])
    input_img = content_img.clone()

    assert style_img.size() == content_img.size(), \
        "Картинки для стиля и для контента должны быть одного размера"

    return input_img, content_img, style_img
