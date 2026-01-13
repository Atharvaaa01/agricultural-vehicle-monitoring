const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const popup = document.getElementById("popup");

imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];
    if (file) {
        previewImage.src = URL.createObjectURL(file);
        previewImage.style.display = "block";
    }
});

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
            throw new Error("API error");
        }

        const data = await response.json();
        console.log("API RESPONSE:", data);

        document.getElementById("vehicleType").innerText =
            data.vehicle_detected ? data.vehicle_type : "Not Detected";

        document.getElementById("sugarcane").innerText =
            data.sugarcane_detected ? "Yes" : "No";

        document.getElementById("plate").innerText =
            data.number_plate ? "Detected" : "Not Detected";

        document.getElementById("plateColor").innerText =
            data.plate_color || "N/A";

        popup.style.display = "flex";

    } catch (err) {
        console.error(err);
        alert("API not reachable");
    }
}

function closePopup() {
    popup.style.display = "none";
}
