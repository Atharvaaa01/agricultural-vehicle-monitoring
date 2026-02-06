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
    formData.append("image", file);

    try {
        const response = await fetch("http://127.0.0.1:5000/detect", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            alert("Image could not be processed.");
            return;
        }

        const data = await response.json();
        console.log("API RESPONSE:", data);

        // Vehicle type
        document.getElementById("vehicleType").innerText =
            data.vehicle_detected ? data.vehicle_type : "Not Detected";

        // Vehicle color
        document.getElementById("vehicleColor").innerText =
            data.vehicle_color ? data.vehicle_color : "N/A";

        // Sugarcane
        document.getElementById("sugarcane").innerText =
            data.sugarcane_detected ? "Yes" : "No";

        // ✅ NUMBER PLATE (FIXED LOGIC)
        if (data.number_plate && data.number_plate !== "UNKNOWN") {
            document.getElementById("plate").innerText = data.number_plate;
        } else {
            document.getElementById("plate").innerText = "Not Detected";
        }

        // Plate color
        document.getElementById("plateColor").innerText =
            data.plate_color ? data.plate_color : "N/A";

        popup.style.display = "flex";

    } catch (error) {
        console.error("Fetch failed:", error);
        alert("Backend not running. Please start the API.");
    }
}

// Close popup
function closePopup() {
    popup.style.display = "none";
}
