"""
Utility Functions Module
Common utility functions used across the project
"""

import os
import cv2
import numpy as np
from typing import List, Tuple
import json
from datetime import datetime
import shutil


def create_project_directories():
    """
    Create necessary project directories
    """
    directories = [
        'dataset/images/train',
        'dataset/images/val',
        'dataset/images/test',
        'dataset/labels/train',
        'dataset/labels/val',
        'dataset/labels/test',
        'models',
        'outputs/detections',
        'outputs/logs',
        'outputs/api_tests',
        'static/test_images',
        'runs/train',
        'runs/val'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✓ Project directories created")


def check_project_structure():
    """
    Verify project structure is correct
    """
    print("\n" + "="*60)
    print("Checking Project Structure")
    print("="*60)
    
    required_dirs = [
        'dataset',
        'models',
        'src',
        'outputs'
    ]
    
    required_files = [
        'requirements.txt',
        'README.md'
    ]
    
    all_good = True
    
    # Check directories
    print("\nDirectories:")
    for dir_name in required_dirs:
        exists = os.path.exists(dir_name) and os.path.isdir(dir_name)
        status = "✓" if exists else "✗"
        print(f"  {status} {dir_name}")
        if not exists:
            all_good = False
    
    # Check files
    print("\nFiles:")
    for file_name in required_files:
        exists = os.path.exists(file_name) and os.path.isfile(file_name)
        status = "✓" if exists else "✗"
        print(f"  {status} {file_name}")
        if not exists:
            all_good = False
    
    if all_good:
        print("\n✓ Project structure is correct")
    else:
        print("\n⚠ Some files/directories are missing")
        print("Run: python -m src.utils to create missing directories")
    
    return all_good


def load_config(config_path='config/config.yaml'):
    """
    Load configuration from YAML file
    """
    import yaml
    
    if not os.path.exists(config_path):
        print(f"⚠ Config file not found: {config_path}")
        return {}
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def save_config(config, config_path='config/config.yaml'):
    """
    Save configuration to YAML file
    """
    import yaml
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"✓ Config saved to: {config_path}")


def log_detection(detection_result, log_file='outputs/logs/detections.json'):
    """
    Log detection result to file
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Prepare log entry
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'vehicle_type': detection_result.get('vehicle_type'),
        'sugarcane_detected': detection_result.get('sugarcane_detected'),
        'number_plate_present': detection_result.get('number_plate_present'),
        'number_plate_text': detection_result.get('number_plate_text', 'N/A'),
        'number_plate_color': detection_result.get('number_plate_color', 'N/A')
    }
    
    # Load existing logs
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    
    # Append new log
    logs.append(log_entry)
    
    # Save logs
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)


def get_detection_statistics(log_file='outputs/logs/detections.json'):
    """
    Get statistics from detection logs
    """
    if not os.path.exists(log_file):
        return None
    
    with open(log_file, 'r') as f:
        logs = json.load(f)
    
    if not logs:
        return None
    
    # Calculate statistics
    stats = {
        'total_detections': len(logs),
        'vehicle_types': {},
        'sugarcane_count': 0,
        'plates_detected': 0,
        'plate_colors': {}
    }
    
    for log in logs:
        # Vehicle types
        vehicle_type = log.get('vehicle_type', 'Unknown')
        stats['vehicle_types'][vehicle_type] = stats['vehicle_types'].get(vehicle_type, 0) + 1
        
        # Sugarcane
        if log.get('sugarcane_detected'):
            stats['sugarcane_count'] += 1
        
        # Plates
        if log.get('number_plate_present'):
            stats['plates_detected'] += 1
            
            color = log.get('number_plate_color', 'Unknown')
            stats['plate_colors'][color] = stats['plate_colors'].get(color, 0) + 1
    
    return stats


def print_statistics(stats):
    """
    Print detection statistics
    """
    if stats is None:
        print("No statistics available")
        return
    
    print("\n" + "="*60)
    print("Detection Statistics")
    print("="*60)
    
    print(f"\nTotal Detections: {stats['total_detections']}")
    
    print("\nVehicle Types:")
    for vehicle, count in stats['vehicle_types'].items():
        percentage = (count / stats['total_detections']) * 100
        print(f"  - {vehicle}: {count} ({percentage:.1f}%)")
    
    print(f"\nSugarcane Detected: {stats['sugarcane_count']}")
    print(f"Number Plates Detected: {stats['plates_detected']}")
    
    if stats['plate_colors']:
        print("\nPlate Colors:")
        for color, count in stats['plate_colors'].items():
            print(f"  - {color}: {count}")


def resize_image(image, max_size=1920):
    """
    Resize image if too large
    """
    height, width = image.shape[:2]
    
    if max(height, width) > max_size:
        scale = max_size / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return image


def draw_text_with_background(image, text, position, font_scale=0.6, 
                              thickness=2, text_color=(255, 255, 255), 
                              bg_color=(0, 0, 0)):
    """
    Draw text with background rectangle
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(
        text, font, font_scale, thickness
    )
    
    x, y = position
    
    # Draw background rectangle
    cv2.rectangle(
        image,
        (x, y - text_height - baseline - 5),
        (x + text_width + 5, y + baseline),
        bg_color,
        -1
    )
    
    # Draw text
    cv2.putText(
        image,
        text,
        (x, y - baseline),
        font,
        font_scale,
        text_color,
        thickness
    )
    
    return image


def create_montage(images, rows=2, cols=2, size=(640, 480)):
    """
    Create a montage of images
    """
    # Resize all images to same size
    resized = []
    for img in images:
        if img is not None:
            resized.append(cv2.resize(img, size))
        else:
            # Create blank image
            resized.append(np.zeros((size[1], size[0], 3), dtype=np.uint8))
    
    # Pad with blank images if needed
    while len(resized) < rows * cols:
        resized.append(np.zeros((size[1], size[0], 3), dtype=np.uint8))
    
    # Create montage
    row_images = []
    for i in range(rows):
        row = np.hstack(resized[i*cols:(i+1)*cols])
        row_images.append(row)
    
    montage = np.vstack(row_images)
    
    return montage


def backup_dataset(source='dataset', backup_dir='backups'):
    """
    Create backup of dataset
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f'dataset_backup_{timestamp}')
    
    print(f"Creating dataset backup...")
    shutil.copytree(source, backup_path)
    print(f"✓ Backup created: {backup_path}")
    
    return backup_path


def cleanup_old_backups(backup_dir='backups', keep_last=5):
    """
    Remove old backups, keeping only the most recent ones
    """
    if not os.path.exists(backup_dir):
        return
    
    # Get all backup directories
    backups = [d for d in os.listdir(backup_dir) 
               if os.path.isdir(os.path.join(backup_dir, d)) and d.startswith('dataset_backup_')]
    
    # Sort by name (which includes timestamp)
    backups.sort(reverse=True)
    
    # Remove old backups
    for backup in backups[keep_last:]:
        backup_path = os.path.join(backup_dir, backup)
        shutil.rmtree(backup_path)
        print(f"✓ Removed old backup: {backup}")


def main():
    """
    Main utility function
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Project Utilities')
    parser.add_argument('--create-dirs', action='store_true',
                       help='Create project directories')
    parser.add_argument('--check-structure', action='store_true',
                       help='Check project structure')
    parser.add_argument('--stats', action='store_true',
                       help='Show detection statistics')
    parser.add_argument('--backup', action='store_true',
                       help='Backup dataset')
    
    args = parser.parse_args()
    
    if args.create_dirs:
        create_project_directories()
    
    if args.check_structure:
        check_project_structure()
    
    if args.stats:
        stats = get_detection_statistics()
        print_statistics(stats)
    
    if args.backup:
        backup_dataset()
        cleanup_old_backups()
    
    if not any(vars(args).values()):
        print("Project Utilities")
        print("\nUsage:")
        print("  --create-dirs     Create project directories")
        print("  --check-structure Check project structure")
        print("  --stats          Show detection statistics")
        print("  --backup         Backup dataset")


if __name__ == '__main__':
    main()
    