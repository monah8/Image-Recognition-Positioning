import os 
from pathlib import Path 

# Define the directory containing the images 
image_dir = Path('/home/monah/Project-ComputerVision-AI/py_verse/data')

# get all images paths 
image_paths = [str(f) for f in image_dir.glob('*.jpg')]  
print(f'Found {len(image_paths)} images')

