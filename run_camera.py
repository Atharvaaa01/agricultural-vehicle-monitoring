from src.camera_detector import run_camera

if __name__ == "__main__":
    rtsp_url = "rtsp://wb:Bal12345@192.168.25.171:554/stream1"
    run_camera(rtsp_url)
