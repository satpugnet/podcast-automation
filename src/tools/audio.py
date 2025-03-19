import os
import json
import time
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
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "segments"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "sfx"), exist_ok=True)
    
    # Define voice IDs for each speaker
    voice_ids = {
        "Narrator": "NOpBlnGInO9m6vDvFkFC",  # Adam voice for intro and outro
        "Leo": "UgBBYS2sOqTuMpoF3BR0",   # Used to be v2YwWtvprj8WUvzb7D4K (Adam)
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
                sfx_path = os.path.join(output_dir, f"sfx/{section}_sfx_{i}.mp3")
                duration = float(item.get("duration", 5.0))  # Default to 5 seconds if not specified
                generate_sound_effect(item["text"], duration, sfx_path)
                segment_paths.append(sfx_path)
                sfx_durations[sfx_path] = duration  # Store the duration for later use
            else:
                # Generate speech
                voice_id = voice_ids.get(item["speaker"], voice_ids["Narrator"])
                speech_path = os.path.join(output_dir, f"segments/{section}_{i}.mp3")
                
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
                segment_paths.append(speech_path)
            
            # Avoid rate limiting for conversation section
            if section == "conversation":
                time.sleep(0.5)
    
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
    character_name = script["historical_figure"].replace(" ", "_")
    combined_path = os.path.join(output_dir, f"podcast_{character_name}.mp3")
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
    output_dir = f"output/{script['historical_figure'].replace(' ', '_')}/audio"
    
    # Generate the podcast audio
    audio_path = generate_podcast_audio(script, guest_voice_id, output_dir)
    
    return audio_path

if __name__ == "__main__":
    script_path = "/Users/saturninpugnet/PycharmProjects/perso/podcast-automation/output/podcast_script_Napoleon_Bonaparte.json"
    guest_voice_id = "VR6AewLTigWG4xSOukaG"
    process_script_to_audio(script_path, guest_voice_id)