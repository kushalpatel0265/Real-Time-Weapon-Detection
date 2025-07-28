import os
from ultralytics import YOLO
import torch
from pathlib import Path

# Detect and print the device (GPU if available, otherwise CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("Device being used:", device)

def train_weapon_detector(
    data_yaml,
    epochs=100,         # Number of training epochs
    img_size=640,       # Input image size
    batch_size=4,       
    model_size='yolov8m'
):
    """
    Trains a YOLOv8 model for weapon detection using a custom dataset.
    
    :param data_yaml:  Path to the data.yaml file defining the training/validation sets.
    :param epochs:     Number of training epochs.
    :param img_size:   Input image size (e.g., 640).
    :param batch_size: Batch size for training.
    :param model_size: YOLOv8 checkpoint to use (e.g., 'yolov8m', 'yolov8l').
    """
    # Load the pretrained YOLOv8 model
    model = YOLO(f"{model_size}.pt")

    # Define custom save path for training results
    custom_save_path = "D:/Deep Learning/DL_Assignement"

    # Train the model using the detected device (GPU/CPU)
    model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        device=device,           
        workers=2,               
        project=custom_save_path,
        name='train',           
        # -- Recommended Performance Tweaks --
        cos_lr=True,             
        close_mosaic=10,         
        mosaic=1.0,              
        mixup=0.2,               
        copy_paste=0.1          
    )

    # Get the save directory from the trainer and construct the best weights path
    save_dir = model.trainer.save_dir 
    best_weight_path = save_dir / 'weights' / 'best.pt'
    if best_weight_path.exists():
        print(f"[INFO] Training complete. Best weights saved at: {best_weight_path}")
    else:
        print("[WARNING] Could not find best.pt. Check training logs.")

if __name__ == "__main__":
    # Path to the data.yaml file
    data_yaml_path = r"D:\Deep Learning\DL_Assignement\augmented_dataset\data.yaml"
    
    # Training configuration
    train_epochs = 100        
    image_size = 640
    batch = 4                
    model_variant = 'yolov8m' 

    train_weapon_detector(
        data_yaml=data_yaml_path,
        epochs=train_epochs,
        img_size=image_size,
        batch_size=batch,
        model_size=model_variant
    )