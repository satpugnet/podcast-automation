import os
import json
import time
import hashlib
from pathlib import Path
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

def generate_sound_effect(text: str, duration_seconds: float, output_path: str):
    """
    Generate sound effects using ElevenLabs API
    
    Args:
        text (str): Description of the sound effect
        output_path (str): Path to save the sound effect
        client (ElevenLabs, optional): ElevenLabs client instance
    """
    client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))
    
    print(f"Generating sound effect: {text}...")
    
    result = client.text_to_sound_effects.convert(
        text=text,
        duration_seconds=duration_seconds,  # Optional
        prompt_influence=0.3,
    )
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "wb") as f:
        for chunk in result:
            f.write(chunk)
    
    print(f"Sound effect saved to {output_path}")
    return output_path

def generate_podcast_audio(script, guest_voice_id, output_dir):
    """
    Generate audio for a podcast script using ElevenLabs API
    
    Args:
        script (dict): The podcast script dictionary
        guest_voice_id (str): Voice ID for the historical figure
        output_dir (str): Directory to save the audio files
    
    Returns:
        str: Path to the final combined audio file
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_LABS_API_KEY not found in environment variables")
    
    # Initialize ElevenLabs client
    client = ElevenLabs(api_key=api_key)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.join(output_dir, "audio"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "audio/segments"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "audio/sfx"), exist_ok=True)
    
    # Define voice IDs for each speaker
    voice_ids = {
        "Narrator": "NOpBlnGInO9m6vDvFkFC",  # Adam voice for intro and outro
        "Leo": "UgBBYS2sOqTuMpoF3BR0", # Currently UgBBYS2sOqTuMpoF3BR0 (Mark), used to be v2YwWtvprj8WUvzb7D4K (Leo Time Traveler)
        script["historical_figure"]: guest_voice_id
    }
    
    # Generate audio segments
    segment_paths = []
    sfx_durations = {}  # Store SFX durations for fade calculations
    
    # Process each section of the script
    sections = ["intro", "arrival_scene", "conversation", "outro"]
    
    for section in sections:
        print(f"Generating audio for {section}...")
        for i, item in enumerate(script[section]):
            if item["speaker"] == "SFX":
                # Generate sound effect
                text_hash = hashlib.md5(f"sfx-{item['text']}".encode()).hexdigest()[:8]
                sfx_path = os.path.join(output_dir, f"audio/sfx/{section}_sfx_{i}_{text_hash}.mp3")
                
                # Check if file already exists
                if os.path.exists(sfx_path):
                    print(f"Using existing sound effect: {sfx_path}")
                else:
                    duration = float(item.get("duration", 5.0))  # Default to 5 seconds if not specified
                    generate_sound_effect(item["text"], duration, sfx_path)
                    
                    # Avoid rate limiting only if we generated a new sound effect
                    time.sleep(0.5)
                
                segment_paths.append(sfx_path)
                sfx_durations[sfx_path] = float(item.get("duration", 5.0))  # Store the duration for later use
            else:
                # Generate speech
                voice_id = voice_ids.get(item["speaker"], voice_ids["Narrator"])
                
                # Create hash from voice_id and text
                content_hash = hashlib.md5(f"{voice_id}-{item['text']}".encode()).hexdigest()[:8]
                speech_path = os.path.join(output_dir, f"audio/segments/{section}_{i}_{content_hash}.mp3")
                
                # Check if file already exists
                if os.path.exists(speech_path):
                    print(f"Using existing speech segment: {speech_path}")
                else:
                    speech_audio = client.text_to_speech.convert(
                        text=item["text"],
                        voice_id=voice_id,
                        model_id="eleven_multilingual_v2",
                        output_format="mp3_44100_128"
                    )
                    
                    # Convert generator to bytes
                    speech_audio_bytes = b"".join(list(speech_audio))
                    with open(speech_path, "wb") as f:
                        f.write(speech_audio_bytes)
                    
                    # Avoid rate limiting only if we generated a new speech segment
                    time.sleep(0.5)
                
                segment_paths.append(speech_path)
    
    # Combine all audio segments
    print("Combining all audio segments...")
    combined = AudioSegment.empty()
    
    # Add a short pause between segments (1500ms silence)
    pause = AudioSegment.silent(duration=1200)
    
    for i, path in enumerate(segment_paths):
        segment = AudioSegment.from_file(path)
        
        # Apply fade in/out effects
        if "sfx" in path:
            # Calculate fade durations based on the SFX duration
            duration = sfx_durations.get(path)
            # Use 20% of the duration for fade in and 25% for fade out, with minimums
            # Calculate fade durations based on the SFX duration, with minimums and maximums
            fade_in_duration = max(min(int(duration * 1000 * 0.2), 3000), 500)  # At least 500ms, at most 3s
            fade_out_duration = max(min(int(duration * 1000 * 0.25), 4000), 750)  # At least 750ms, at most 4s
            segment = segment.fade_in(fade_in_duration).fade_out(fade_out_duration)
        else:
            # Apply subtle fades for speech to sound more natural
            segment = segment.fade_in(300).fade_out(500)
        
        combined += segment
        
        # Add pause after each segment except the last one
        if i < len(segment_paths) - 1:
            combined += pause
    
    # Save the combined audio
    combined_path = os.path.join(output_dir, f"audio.mp3")
    combined.export(combined_path, format="mp3")
    
    print(f"Podcast audio generated and saved to {combined_path}")
    return combined_path

def process_script_to_audio(script_json_path, guest_voice_id):
    """
    Process a script JSON file to generate audio
    
    Args:
        script_json_path (str): Path to the script JSON file
        guest_voice_id (str): Voice ID for the historical figure
        
    Returns:
        str: Path to the generated audio file
    """
    # Load the script
    with open(script_json_path, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    # Create a specific output directory for this podcast
    output_dir = f"output/{script['historical_figure'].replace(' ', '_')}"
    
    # Generate the podcast audio
    audio_path = generate_podcast_audio(script, guest_voice_id, output_dir)
    
    return audio_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        script_path = sys.argv[1]
        guest_voice_id = sys.argv[2]
        audio_path = process_script_to_audio(script_path, guest_voice_id)
        print(f"Generated audio saved to: {audio_path}")
    else:
        print("Usage: python audio.py <script_path> <guest_voice_id>")