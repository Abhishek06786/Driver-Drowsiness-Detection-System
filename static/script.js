// ---------------- Dashboard Update ----------------

async function updateDashboard() {

    try {

        const response = await fetch("/data");
        const data = await response.json();

        document.getElementById("status").innerHTML = data.status;
        document.getElementById("ear").innerHTML = data.ear;
        document.getElementById("mar").innerHTML = data.mar;
        document.getElementById("blinks").innerHTML = data.blinks;
        document.getElementById("yawns").innerHTML = data.yawns;

        const alertBox = document.getElementById("alert");

        if (data.status === "Drowsy") {

            alertBox.innerHTML = "🚨 DRIVER IS DROWSY";
            alertBox.style.background = "#ef4444";

        }

        else if (data.status === "Eyes Closed") {

            alertBox.innerHTML = "⚠️ Eyes Closed";
            alertBox.style.background = "#f59e0b";

        }

        else if (data.status === "No Face") {

            alertBox.innerHTML = "📷 No Face Detected";
            alertBox.style.background = "#64748b";

        }

        else {

            alertBox.innerHTML = "✅ No Drowsiness Detected";
            alertBox.style.background = "#22c55e";

        }

    }

    catch (error) {

        console.log(error);

    }

}

// Dashboard Auto Refresh

setInterval(updateDashboard, 500);

updateDashboard();


// ---------------- START BUTTON ----------------

document.getElementById("startBtn").addEventListener("click", async () => {

    const response = await fetch("/start");
    const result = await response.json();

    if (result.success) {

        const img = new Image();

        img.id = "cameraFeed";
        img.className = "camera";
        img.alt = "Live Camera Feed";

        img.onload = () => {

            document.getElementById("cameraContainer").innerHTML = "";
            document.getElementById("cameraContainer").appendChild(img);

            console.log("Camera Started");

        };

        img.src = "/video?" + new Date().getTime();

    }

});


// ---------------- STOP BUTTON ----------------


document.getElementById("stopBtn").addEventListener("click", async () => {

    const response = await fetch("/stop");
    const result = await response.json();

    if (result.success) {

        document.getElementById("cameraContainer").innerHTML = `
            <div class="camera-placeholder">

                <div class="camera-icon">📷</div>

                <h2>Camera Stopped</h2>

                <p>Press <b>Start</b> to Continue</p>

            </div>
        `;

        console.log("Camera Stopped");

    }

});

// ---------------- RESET BUTTON ----------------

document.getElementById("resetBtn").addEventListener("click", async () => {

    const response = await fetch("/reset");
    const result = await response.json();

    if (result.success) {

        updateDashboard();

        console.log("Dashboard Reset");

    }

});