import os
import shutil

base_dir = "dataset/images/train"

for item in os.listdir(base_dir):
    item_path = os.path.join(base_dir, item)

    if os.path.isdir(item_path):
        for file in os.listdir(item_path):
            if file.lower().endswith((".jpg", ".png", ".jpeg")):
                shutil.move(
                    os.path.join(item_path, file),
                    os.path.join(base_dir, file)
                )
        os.rmdir(item_path)

print("✅ Images flattened successfully")
