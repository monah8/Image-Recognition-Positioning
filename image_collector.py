import os 
from pathlib import Path 

def get_all_images(directory_path='/home/monah/Project-ComputerVision-AI/py_verse/data'):
    # Define the directory containing the images 
    image_dir = Path(directory_path)

    # get all images paths 
    image_paths = [str(f) for f in image_dir.glob('*.jpg')]  
    
    print(f'Found {len(image_paths)} images')
    
    return image_paths

