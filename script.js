document.getElementById('startRecording').addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];

    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            chunks.push(event.data);
        }
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);

        // Play the recorded audio
        document.getElementById('audioPlayer').src = audioUrl;

        // Send the audio file to the server for prediction
        sendAudioToServer(audioBlob);
    };

    // Start recording
    mediaRecorder.start();

    // Stop recording after 5 seconds (you can adjust the duration)
    setTimeout(() => {
        mediaRecorder.stop();
    }, 5000);
});

function sendAudioToServer(audioBlob) {
    // Use AJAX or Fetch API to send the audio to the server
    // Update the URL endpoint and method as needed
    $.ajax({
        url: '/predict_audio',
        type: 'POST',
        data: audioBlob,
        contentType: false,
        processData: false,
        success: function (data) {
            // Handle the prediction result returned from the server
            console.log('Prediction Result:', data);
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}
