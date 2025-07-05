import os
import torch
import numpy as np
from bark import SAMPLE_RATE, generate_audio
from scipy.io.wavfile import write as write_wav
from pydub import AudioSegment

# 🔁 Bark auto-detects GPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"💻 Bark will use: {DEVICE.upper()} (handled internally)")

def fallback_generate_voiceover(script_data, output_dir="assets/audio/lines"):
    os.makedirs(output_dir, exist_ok=True)
    print("\n🔄 ElevenLabs failed or skipped. Using fallback TTS (🎙️ Bark)...")

    for idx, item in enumerate(script_data):
        sentence = item["sentence"]
        wav_temp_path = os.path.join(output_dir, f"temp_line_{idx + 1}.wav")
        mp3_final_path = os.path.join(output_dir, f"line_{idx + 1}.mp3")

        print(f"🧠 Bark TTS: Generating line {idx + 1}: '{sentence}'")

        try:
            # Generate audio array
            audio_array = generate_audio(sentence)

            # Convert to int16 and save as WAV
            audio_int16 = (audio_array * 32767).astype(np.int16)
            write_wav(wav_temp_path, SAMPLE_RATE, audio_int16)

            # Check if temp WAV was created
            if not os.path.exists(wav_temp_path):
                raise FileNotFoundError(f"Temp WAV not found: {wav_temp_path}")

            # Convert WAV to MP3 using pydub + ffmpeg
            try:
                sound = AudioSegment.from_wav(wav_temp_path)
                sound.export(mp3_final_path, format="mp3")
                print(f"✅ Fallback line {idx + 1} saved to: {mp3_final_path}")
            except Exception as conv_error:
                print(f"❌ Error converting to MP3: {conv_error}")
            finally:
                if os.path.exists(wav_temp_path):
                    os.remove(wav_temp_path)

        except Exception as e:
            print(f"❌ Bark TTS failed on line {idx + 1}: {e}")
