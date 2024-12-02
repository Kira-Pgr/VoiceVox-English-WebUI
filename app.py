import streamlit as st
import base64
from voicevox_tts import VoicevoxTTS

def get_audio_html(audio_path):
    """Convert audio file to HTML audio player."""
    audio_file = open(audio_path, 'rb')
    audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    return f'<audio controls><source src="data:audio/wav;base64,{audio_base64}" type="audio/wav"></audio>'

def get_speaker_info(tts):
    """Get organized speaker information."""
    speakers = tts.get_speakers()
    speaker_dict = {}
    
    for speaker in speakers:
        name = speaker["name"]
        speaker_dict[name] = {
            "uuid": speaker["speaker_uuid"],
            "styles": {style["name"]: style["id"] for style in speaker["styles"]}
        }
    
    return speaker_dict

def main():
    st.set_page_config(
        page_title="VOICEVOX TTS",
        page_icon="🎤",
        layout="wide"
    )
    
    st.title("🎤 VOICEVOX Text-to-Speech")
    st.write("Convert text to speech using any VOICEVOX speaker")

    # Initialize TTS engine
    tts = VoicevoxTTS()
    
    # Get speaker information
    speakers = get_speaker_info(tts)
    
    # Sidebar for speaker selection
    with st.sidebar:
        st.header("Speaker Selection")
        
        # Speaker selection
        selected_speaker = st.selectbox(
            "Select Speaker:",
            list(speakers.keys()),
            index=list(speakers.keys()).index("ナースロボ＿タイプＴ") if "ナースロボ＿タイプＴ" in speakers else 0
        )
        
        # Voice type selection for the chosen speaker
        selected_style = st.selectbox(
            "Select Voice Type:",
            list(speakers[selected_speaker]["styles"].keys())
        )
        
        # Get the speaker ID
        speaker_id = speakers[selected_speaker]["styles"][selected_style]
        
        st.markdown("---")
        
        # About section
        st.header("About")
        st.write("""
        This is a web interface for VOICEVOX Text-to-Speech system. 
        It supports all available VOICEVOX speakers and their voice types.
        The system converts Japanese text into natural-sounding speech.
        """)

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input
        text = st.text_area(
            "Enter Japanese text:",
            height=150,
            help="Enter the Japanese text you want to convert to speech",
            placeholder="こんにちは、音声合成の世界へようこそ！"
        )
        
        # Display current selection
        st.info(f"Selected: {selected_speaker} - {selected_style} (ID: {speaker_id})")
        
        # Generate button
        if st.button("Generate Voice 🔊", type="primary", use_container_width=True):
            if text:
                with st.spinner('Generating voice...'):
                    try:
                        # Generate speech
                        output_file = tts.text_to_speech(
                            text=text,
                            speaker_id=speaker_id,
                            output_file="temp.wav"
                        )
                        
                        # Display audio player
                        st.markdown("### Generated Audio:")
                        st.markdown(get_audio_html(output_file), unsafe_allow_html=True)
                        
                        # Add download button
                        with open(output_file, "rb") as file:
                            st.download_button(
                                label="Download WAV File 💾",
                                data=file,
                                file_name=f"voicevox_{selected_speaker}_{selected_style}.wav",
                                mime="audio/wav",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter some text first.")
    
    with col2:
        # Usage instructions
        st.markdown("### How to Use")
        st.markdown("""
        1. Select a speaker from the sidebar
        2. Choose a voice type for the selected speaker
        3. Enter Japanese text in the text box
        4. Click 'Generate Voice' button
        5. Use the audio player to listen
        6. Download the WAV file if needed
        
        **Note:** This system only works with Japanese text input.
        """)
        
        # Display available voice types for current speaker
        st.markdown("### Available Voice Types")
        st.markdown("Current speaker's voice types:")
        for style, style_id in speakers[selected_speaker]["styles"].items():
            st.markdown(f"- {style} (ID: {style_id})")

if __name__ == "__main__":
    main() 