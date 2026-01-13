import os
import shutil
import random

train_dir = "dataset/images/train"
val_dir = "dataset/images/val"

os.makedirs(val_dir, exist_ok=True)

images = [
    f for f in os.listdir(train_dir)
    if f.lower().endswith((".jpg", ".png", ".jpeg"))
]

random.shuffle(images)

split_count = int(0.2 * len(images))

for img in images[:split_count]:
    shutil.move(
        os.path.join(train_dir, img),
        os.path.join(val_dir, img)
    )

print("✅ Train / Validation split completed successfully")
