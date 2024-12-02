document.addEventListener("DOMContentLoaded", function () {
    const cameraButton = document.createElement("button");
    cameraButton.textContent = "Capture from Camera";
    cameraButton.type = "button";
    cameraButton.style.margin = "10px 0";

    const fileInput = document.getElementById("id_profile_picture");
    const fileInputParent = fileInput.parentNode;

    const video = document.createElement("video");
    video.autoplay = true;
    video.style.width = "300px";
    video.style.height = "300px";
    video.style.border = "1px solid #ccc";
    video.style.display = "none";

    const canvas = document.createElement("canvas");
    canvas.width = 300;
    canvas.height = 300;

    const captureButton = document.createElement("button");
    captureButton.textContent = "Capture Photo";
    captureButton.type = "button";
    captureButton.style.margin = "10px 0";
    captureButton.style.display = "none";

    cameraButton.addEventListener("click", () => {
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then((stream) => {
                video.srcObject = stream;
                video.style.display = "block";
                captureButton.style.display = "inline-block";
            })
            .catch((error) => {
                console.error("Camera access denied:", error);
            });
    });

    captureButton.addEventListener("click", () => {
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.toBlob((blob) => {
            const file = new File([blob], "profile_picture.jpg", { type: "image/jpeg" });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;

            // Stop the video stream
            const tracks = video.srcObject.getTracks();
            tracks.forEach((track) => track.stop());

            video.style.display = "none";
            captureButton.style.display = "none";
        });
    });

    fileInputParent.appendChild(cameraButton);
    fileInputParent.appendChild(video);
    fileInputParent.appendChild(captureButton);
});
