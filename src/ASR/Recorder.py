import pyaudio
import wave
import numpy as np
from datetime import datetime
import os

class SentenceRecorder:
    def __init__(self, 
                 silence_threshold=500,
                 pause_duration=4.0,
                 chunk_size=1024,
                 sample_rate=44100,
                 output_dir="recordings"):

        self.silence_threshold = silence_threshold
        self.pause_duration = pause_duration
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.format = pyaudio.paInt16
        self.channels = 1
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
    def get_rms(self, data):
        try:
            audio_data = np.frombuffer(data, dtype=np.int16)

            rms = np.sqrt(np.mean(audio_data.astype(np.float64)**2))
            if np.isnan(rms) or np.isinf(rms):
                return 0
            return rms
        except:
            return 0
        
    
    def trim_silence(self, frames):
        if not frames:
            return frames
        
        chunks_per_second = self.sample_rate / self.chunk_size
        chunks_to_remove = int(self.pause_duration * chunks_per_second * 0.95)
        
        if len(frames) > chunks_to_remove:
            return frames[:-chunks_to_remove]
        
        return frames

    
    def save_sentence(self, frames, sentence_num, audio):
        trimmed_frames = self.trim_silence(frames)
        
        if not trimmed_frames:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"sentence_{sentence_num}_{timestamp}.wav")
        
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(self.format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(trimmed_frames))
        wf.close()
        
        print(f"✓ Saved: {filename}")
        return filename
    
    def record_continuously(self):
        audio = pyaudio.PyAudio()
        
        stream = audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        frames = []
        silent_chunks = 0
        chunks_per_second = self.sample_rate / self.chunk_size
        pause_chunks_threshold = int(self.pause_duration * chunks_per_second)
        
        is_speaking = False
        sentence_count = 0
        
        try:
            while True:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                
                rms = self.get_rms(data)
                
                if rms > self.silence_threshold:
                    if not is_speaking:
                        is_speaking = True
                        print("\n🎤 Recording sentence...", end='', flush=True)
                    
                    frames.append(data)
                    silent_chunks = 0
                else:
                    if is_speaking:
                        frames.append(data)
                        silent_chunks += 1
                        
                        if silent_chunks > pause_chunks_threshold:
                            if len(frames) > 0:
                                sentence_count += 1
                                a = self.save_sentence(frames, sentence_count, audio)
                                if a.strip() != '':
                                    return a

                            frames = []
                            silent_chunks = 0
                            is_speaking = False
                            print("Listening...")
                    
        except KeyboardInterrupt:
            print("\n\n" + "=" * 60)
            print("Recording stopped by user.")
            
            if is_speaking and len(frames) > 0:
                sentence_count += 1
                self.save_sentence(frames, sentence_count, audio)
            
            print(f"Total sentences recorded: {sentence_count}")
            print("=" * 60)
        
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
