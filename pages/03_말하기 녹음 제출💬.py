import streamlit as st
import base64
import os

st.title("🎤 일본어 말하기 녹음 제출")

name = st.text_input("이름을 입력하세요")

SAVE_DIR = "data"
os.makedirs(SAVE_DIR, exist_ok=True)

st.write("버튼을 눌러 바로 녹음을 시작할 수 있습니다.")

audio_component = """
<script>
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        audioChunks = [];
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        mediaRecorder.ondataavailable = e => {
            audioChunks.push(e.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);

            reader.onloadend = () => {
                const base64Audio = reader.result.split(',')[1];
                window.parent.postMessage(
                    {isStreamlitMessage: true, audio_data: base64Audio},
                    "*"
                );
            };
        };
    });
}

function stopRecording() {
    mediaRecorder.stop();
}
</script>

<button onclick="startRecording()">🎙️ 녹음 시작</button>
<button onclick="stopRecording()">⏹️ 녹음 종료</button>
"""

st.components.v1.html(audio_component, height=150)

# 메시지 수신
msg = st.experimental_get_query_params()

if "audio_data" in msg and name:
    audio_bytes = base64.b64decode(msg["audio_data"][0])
    filename = f"{name}_record.wav"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(audio_bytes)

    st.success(f"녹음 저장 완료: {filename}")
    st.audio(audio_bytes)
elif "audio_data" in msg and not name:
    st.error("이름을 먼저 입력해주세요.")
