const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const popup = document.getElementById("popup");

// Preview selected image
imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];
    if (file) {
        previewImage.src = URL.createObjectURL(file);
        previewImage.style.display = "block";
    }
});

// Send image to backend
async function sendImage() {
    const file = imageInput.files[0];

    if (!file) {
        alert("Please select an image");
        return;
    }

    const formData = new FormData();
    // 🔴 MUST MATCH api.py → request.files["image"]
    formData.append("image", file);

    try {
        const response = await fetch("http://127.0.0.1:5000/detect", {
            method: "POST",
            body: formData
        });

        // API reachable but request failed
        if (!response.ok) {
            const errText = await response.text();
            console.error("API error:", errText);
            alert("Image could not be processed. Try a JPG/PNG image.");
            return;
        }

        const data = await response.json();
        console.log("API RESPONSE:", data);

        // Vehicle type
        document.getElementById("vehicleType").innerText =
            data.vehicle_detected
                ? data.vehicle_type
                : "Not Detected";

        // Sugarcane
        document.getElementById("sugarcane").innerText =
            data.sugarcane_detected ? "Yes" : "No";

        // Number plate text (OCR)
        if (data.number_plate) {
            if (data.plate_text && data.plate_text !== "UNKNOWN") {
                document.getElementById("plate").innerText = data.plate_text;
            } else {
                document.getElementById("plate").innerText =
                    "Detected (Text unclear)";
            }
        } else {
            document.getElementById("plate").innerText = "Not Detected";
        }

        // Plate color
        document.getElementById("plateColor").innerText =
            data.plate_color ? data.plate_color : "N/A";

        // Show popup
        popup.style.display = "flex";

    } catch (error) {
        console.error("Fetch failed:", error);
        alert("Backend not running. Please start the API.");
    }
}

// Close result popup
function closePopup() {
    popup.style.display = "none";
}
