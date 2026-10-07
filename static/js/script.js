const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const status = document.getElementById("status");

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        previewImage.style.display = "none";
        return;
    }

    const imageURL = URL.createObjectURL(file);

    previewImage.src = imageURL;
    previewImage.style.display = "block";

    status.textContent = "Image selected successfully.";
});