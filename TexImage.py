import io
import os
import sys
import requests
import PIL
import torch
import torchvision.transforms as T
import torchvision.transforms.functional as TF
import matplotlib.pyplot as plt

from dall_e import map_pixels,unmap_pixels,load_model

target_size = 256
def download_img(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return PIL.Image.open(io.BytesIO(resp.content))

def preprocessing(img):
    s = min(img.size)
    if s < target_size:
        raise ValueError(f'min dim for image')
    r = target_size / s
    s = round(r * img.size[1]),round(r * img.size[0])
    img = TF.resize(img,s,interpolation=PIL.Image.LANCZOS)
    img = TF.center_crop(img,output_size=2*[target_size])
    img = torch.unsqueeze(T.ToTensor()(img),0)
    return map_pixels(img)


class TextToImage:
    def __init__(self):
        self.Story = list()
        self.Session = list()
        self.Session_Name = list()
        self.Story.append(self.Session)

    def WriteStoryLine(self):
        SingleStoryLine = input('Continue your Story:: ')
        self.Session.append(SingleStoryLine)

    def NewStorySession(self,Name):
        self.Session = list()
        self.Story.append(self.Session)
        self.Session_Name.append(Name)

    def ShowWholeStory(self):
        for session_index in range(len(self.Session)):
            session_of_story = self.Session[session_index]
            session_name = self.Session_Name[session_index]
            print("Session Name : ",session_name)
            print("-------------------------------->")
            session_story = ""
            for line_of_session in session_of_story:
                session_story += line_of_session
            print(session_story)


if __name__ == "__main__":
    print("Load Torch with CPU")
    dev = torch.device('cpu')
    print("Load Encoder Model")
    enc = load_model("encoder.pkl",dev)
    #enc = load_model("https://cdn.openai.com/dall-e/encoder.pkl", dev)
    print("Decoder Model")
    #dec = load_model("https://cdn.openai.com/dall-e/decoder.pkl", dev)
    dec = load_model("decoder.pkl",dev)
    print("Preprocessing and download image")
    x = preprocessing(download_img('https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iKIWgaiJUtss/v2/1000x-1.jpg'))

    img = T.ToPILImage(mode='RGB')(x[0])
    plt.imshow(img)
    plt.show()
    import torch.nn.functional as F

    z_logits = enc(x)

    z = torch.argmax(z_logits, axis=1)
    z = F.one_hot(z, num_classes=enc.vocab_size).permute(0, 3, 1, 2).float()


    ch_array = z[0,0:100,:,:]

    for i in range(100):
        ch_sub_array = z[0,i].flatten()
        byte_ch = 0
        for ch_item in ch_sub_array:
            if ch_item > 0:
                print(ch_item)
                print( byte_ch)
                ch_print = byte_ch % 256
                print(chr(ch_print))
            byte_ch += 1

    x_stats = dec(z).float()
    x_rec = unmap_pixels(torch.sigmoid(x_stats[:, :3]))
    x_rec = T.ToPILImage(mode='RGB')(x_rec[0])
    plt.imshow(x_rec)
    plt.show()
