const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const status = document.getElementById("status");
const compareButton = document.getElementById("compareButton");


// Image selection
imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        previewImage.style.display = "none";
        status.textContent = "";
        return;
    }

    const imageURL = URL.createObjectURL(file);

    previewImage.src = imageURL;
    previewImage.style.display = "block";

    status.textContent = "Image ready for analysis.";
});


// Compare Price button
compareButton.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {
        status.textContent = "Please select an image first.";
        return;
    }

    status.textContent = "Analyzing image...";

    const formData = new FormData();
    formData.append("image", file);

    try {

        const response = await fetch("/api/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!data.success) {
            status.textContent = data.message || "Something went wrong.";
            return;
        }

        // Save result temporarily
        localStorage.setItem("fashionResult", JSON.stringify(data));

        // Open result page
        window.location.href = "/result";

    } catch (error) {

        console.error(error);

        status.textContent =
            "Unable to connect to the backend.";
    }
});