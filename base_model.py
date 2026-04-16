# from pyexpat import model
import numpy as np
from tqdm import tqdm 
import torch
from torchvision import models, transforms
from PIL import Image
import os 
import image_collector 

# generating vector embeddings 
class ImageEmbedder: 
    def __init__(self):
        self.model = models.resnet50(weights='DEFAULT')
    
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])
        self.model.eval()

    # scaling all images and normalizing them 
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225]),
        ]) 

    # @staticmethod
    def get_embedding(self, image_path): 
        # load and transform the image 
        img = Image.open(image_path).convert('RGB')
        img_t = self.transform(img)
        batch_t = torch.unsqueeze(img_t, 0)

        # get the embedding using the model resnet50 
        with torch.no_grad(): 
            embedding = self.model(batch_t)

        # return the embedding as a numpy array
        return embedding.squeeze().cpu().numpy()

    # generate embeddings for a list of image paths 
#embeddings = {}
#for image_path in tqdm(image_collector.get_all_images(), desc="Generating image embeddings"):
 #   try:
  #      img_id = os.path.basename(image_path.split('.')[0])  # Extract image ID from filename

   #     embedding = ImageEmbedder.get_images_embedded(image_path)
    #    embeddings[img_id] = embedding

    #except Exception as e: 
     #   print(f'Error processing {image_path}: {e}')

#print(f'Generated embeddings for {len(embeddings)} images.')       
