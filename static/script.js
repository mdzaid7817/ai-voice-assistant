document.addEventListener("DOMContentLoaded", () => {
  let mediaRecorder = null;
  let recordedChunks = [];
  let isRecording = false;

  const recordBtn = document.getElementById("recordBtn");
  const statusDisplay = document.getElementById("statusDisplay");
  const audioPlayer = document.getElementById("audioPlayer");

  // Ensure session ID persists
  let sessionId = new URLSearchParams(window.location.search).get("session_id");
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    window.history.replaceState({}, "", `?session_id=${sessionId}`);
  }

  async function startRecording() {
    if (!navigator.mediaDevices?.getUserMedia) {
      alert("Mic not supported.");
      return;
    }
    recordBtn.textContent = "⏹ Stop Recording";
    recordBtn.classList.add("recording");
    statusDisplay.textContent = "Recording...";

    recordedChunks = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) recordedChunks.push(e.data);
    };
    mediaRecorder.onstop = handleStopRecording;

    mediaRecorder.start();
    isRecording = true;
  }

  async function handleStopRecording() {
    recordBtn.disabled = true;
    recordBtn.textContent = "Thinking...";
    recordBtn.classList.remove("recording");
    statusDisplay.textContent = "Processing your query...";

    const blob = new Blob(recordedChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio_file", blob, "recording.webm");

    try {
      const response = await fetch(`/agent/chat/${sessionId}`, { method: "POST", body: formData });

      if (response.headers.get("X-Error") === "true") {
        statusDisplay.textContent = "Error occurred.";
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayer.src = audioUrl;
        audioPlayer.hidden = false;
        audioPlayer.play();
      } else {
        const result = await response.json();
        if (result.audio_url) {
          audioPlayer.src = result.audio_url;
          audioPlayer.hidden = true;
          audioPlayer.play();
          statusDisplay.textContent = "Here’s my response...";
        }
      }
    } catch (err) {
      console.error(err);
      statusDisplay.textContent = "Error processing request.";
    }
    recordBtn.disabled = false;
    recordBtn.textContent = "🎙 Start Talking";
    isRecording = false;
  }

  recordBtn.addEventListener("click", () => {
    if (isRecording) {
      mediaRecorder.stop();
    } else {
      startRecording();
    }
  });
});
