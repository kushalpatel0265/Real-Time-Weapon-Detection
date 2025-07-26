document.addEventListener('DOMContentLoaded', function() {
    const cameraSelect = document.getElementById('cameraSelect');
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    let isRunning = false;

    // Handle camera selection
    cameraSelect.addEventListener('change', function() {
        fetch('/set_camera', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `camera_id=${this.value}`
        });
    });

    // Handle start/stop surveillance
    startButton.addEventListener('click', function() {
        if (!isRunning) {
            isRunning = true;
            startButton.disabled = true;
            stopButton.disabled = false;
            cameraSelect.disabled = true;
        }
    });

    stopButton.addEventListener('click', function() {
        if (isRunning) {
            isRunning = false;
            startButton.disabled = false;
            stopButton.disabled = true;
            cameraSelect.disabled = false;
        }
    });
});
