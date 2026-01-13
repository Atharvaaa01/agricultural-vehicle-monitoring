from ultralytics import YOLO

def train():
    print("Starting YOLOv8 training...")

    model = YOLO("yolov8n.pt")

    model.train(
        data="dataset/data.yaml",
        epochs=30,
        imgsz=640,
        batch=4,
        device="cpu"
    )

if __name__ == "__main__":
    train()
