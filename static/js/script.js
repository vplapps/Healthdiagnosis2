document.getElementById("diagnose-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const pressure = document.getElementById("pressure").value;
    const temp = document.getElementById("temp").value;
    const pulse = document.getElementById("pulse").value;

    try {
        const response = await fetch("/diagnose", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, age, pressure, temp, pulse })
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById("result").style.display = "block";
            document.getElementById("result").innerText = `Risk Level: ${data.risk_level}`;
        } else {
            document.getElementById("result").style.display = "block";
            document.getElementById("result").innerText = "Error processing your request.";
        }
    } catch (err) {
        console.error(err);
        document.getElementById("result").style.display = "block";
        document.getElementById("result").innerText = "Unable to connect to the server.";
    }
});

document.getElementById("history-button").addEventListener("click", async () => {
    console.log("History button clicked");  // Лог події
    const historySection = document.getElementById("history-section");
    const historyTableBody = document.getElementById("history-table-body");

    // Очистити таблицю перед завантаженням нових даних
    historyTableBody.innerHTML = "";

    try {
        const response = await fetch("/history");
        console.log("Fetching history from /history");  // Лог для перевірки запиту

        if (response.ok) {
            const data = await response.json();
            console.log("History data received:", data);  // Лог для перевірки отриманих даних

            // Перевіряємо, чи є дані
            if (data.length === 0) {
                alert("No history data found.");
                return;
            }

            // Додати кожен запис у таблицю
            data.forEach(record => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${record.name}</td>
                    <td>${record.age}</td>
                    <td>${record.temperature}</td>
                    <td>${record.pulse}</td>
                    <td>${record.risk_level}</td>
                    <td>${record.created_at}</td>
                `;
                historyTableBody.appendChild(row);
            });

            // Показати секцію історії
            historySection.style.display = "block";
        } else {
            console.error("Failed to fetch history, status:", response.status);
            alert("Failed to load history");
        }
    } catch (error) {
        console.error("Error while fetching history:", error);
        alert("An error occurred while fetching the history.");
    }
});

