import os 
from pathlib import Path 

def get_all_images(directory_path='/home/monah/Project-ComputerVision-AI/py_verse/data'):
    # Define the directory containing the images 
    image_dir = Path(directory_path)

    # get all images paths 
    return [str(f) for f in image_dir.glob('*.jpg')]  

