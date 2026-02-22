document.getElementById("uploadForm").onsubmit = async function (event) {
    event.preventDefault();

    let formData = new FormData(this);
    let response = await fetch("/", { method: "POST", body: formData });

    let result = await response.json();

    // Display uploaded image
    document.getElementById("uploadedImage").src = result.img_url;
    document.getElementById("resultContainer").style.display = "block";

    // Populate table with results
    document.getElementById("carResult").textContent = result.is_car ? "Car Detected" : "Not a Car";
    document.getElementById("damageResult").textContent = result.is_damaged ? "Damaged" : "Not Damaged";
    document.getElementById("locationResult").textContent = result.location || "N/A";
    document.getElementById("severityResult").textContent = result.severity || "N/A";
};
