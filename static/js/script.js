async function uploadInvoice() {
    const fileInput = document.getElementById("invoiceFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload a file first.");
        return;
    }

    const progressContainer = document.getElementById("progressContainer");
    const progressBar = document.getElementById("progressBar");
    progressContainer.style.display = "block";
    progressBar.style.width = "10%"; // starting

    const formData = new FormData();
    formData.append("file", file);

    try {
        // Fake progress for UI feedback
        let progress = 10;
        const fakeInterval = setInterval(() => {
            progress = Math.min(progress + 5, 90);
            progressBar.style.width = progress + "%";
        }, 500);

        const response = await fetch("/extract", {
            method: "POST",
            body: formData
        });

        clearInterval(fakeInterval);
        progressBar.style.width = "100%";

        const data = await response.json();
        console.log("Server response:", data);

        const tableBody = document.querySelector("#resultTable tbody");
        tableBody.innerHTML = "";

        const row = `
            <tr>
                <td>${data.supplier_name || "null"}</td>
                <td>${data.total_price ?? "null"}</td>
                <td>${data.payment_method || "null"}</td>
                <td>${data.date_time || "null"}</td>
                <td>${data.confidence ?? "null"}</td>
            </tr>
        `;
        tableBody.innerHTML = row;

        // ✅ Hide progress bar after completion and reset
        progressContainer.style.display = "none";
        progressBar.style.width = "0%";

    } catch (error) {
        alert("Extraction failed: " + error);
        // Hide progress bar if error occurs
        progressContainer.style.display = "none";
        progressBar.style.width = "0%";
    }
}