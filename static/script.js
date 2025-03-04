document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("toggleBlur").addEventListener("click", function () {
        fetch("/toggle_blur", { method: "POST" })
            .then(response => response.json())
            .then(data => console.log("Blur status:", data.status))
            .catch(error => console.error("Error:", error));
    });
});
