# Agricultural Vehicle Monitoring System (Vision AI)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/agricultural-vehicle-monitoring.git
   ```
2. Navigate to the project directory:
   ```
   cd agricultural-vehicle-monitoring
   ```
3. Create a virtual environment and activate it:
   ```
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the API Server
1. Start the Flask API server:
   ```
   python run_api.py
   ```
   The API will be available at `http://localhost:5000`.

### Running the Camera Detector
1. Start the camera-based detection:
   ```
   python run_camera.py
   ```
   This will launch the camera detection and display the results.

### Interacting with the API
1. You can use the provided `test_api.py` script to test the API:
   ```
   python test_api.py
   ```
   This will send a sample image to the API and print the response.

2. You can also test the number plate processing using `test_plate.py`:
   ```
   python test_plate.py
   ```
   This will load an image, extract the number plate text, and detect the plate color.

## API

The API provides the following endpoints:

- `POST /detect`: Accepts an image file and returns the detected objects and their bounding boxes.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Submit a pull request to the main repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

To run the tests, use the following command:
```
python -m unittest discover tests
```