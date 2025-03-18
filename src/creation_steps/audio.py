import os
import json
import time
from pathlib import Path
from pydub import AudioSegment
from elevenlabs import generate, set_api_key, save
from elevenlabs.api import Voices
from dotenv import load_dotenv

def generate_podcast_audio(script_path, output_dir="output/audio"):
    """
    Generate audio for a podcast script using ElevenLabs API
    
    Args:
        script_path (str): Path to the JSON script file
        output_dir (str): Directory to save the audio files
    
    Returns:
        str: Path to the final combined audio file
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
    
    # Set the API key
    set_api_key(api_key)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the script
    with open(script_path, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    # Get available voices
    available_voices = Voices.from_api()
    
    # Select voices for different speakers
    voice_mapping = {
        "Narrator": "Adam",  # For intro and outro
        "Leo": "Josh",       # Time traveler
        script["historical_figure"]: "Arnold"  # Historical figure
    }
    
    # Map voice names to voice IDs
    voice_ids = {}
    for role, voice_name in voice_mapping.items():
        for voice in available_voices:
            if voice.name.lower() == voice_name.lower():
                voice_ids[role] = voice.voice_id
                break
        if role not in voice_ids:
            print(f"Warning: Voice '{voice_name}' not found for {role}. Using default voice.")
            # Use the first available voice as default
            voice_ids[role] = available_voices[0].voice_id
    
    # Generate audio segments
    audio_segments = []
    segment_paths = []
    
    # Process intro
    print(f"Generating audio for intro...")
    intro_path = os.path.join(output_dir, "intro.mp3")
    intro_audio = generate(
        text=script["intro"],
        voice=voice_ids["Narrator"],
        model="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    save(intro_audio, intro_path)
    segment_paths.append(intro_path)
    
    # Process arrival scene
    print(f"Generating audio for arrival scene...")
    arrival_path = os.path.join(output_dir, "arrival_scene.mp3")
    arrival_audio = generate(
        text=script["arrival_scene"],
        voice=voice_ids["Narrator"],
        model="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    save(arrival_audio, arrival_path)
    segment_paths.append(arrival_path)
    
    # Process conversation
    for i, exchange in enumerate(script["conversation"]):
        speaker = exchange["speaker"]
        text = exchange["text"]
        
        # Determine which voice to use
        if speaker == "Leo":
            voice_id = voice_ids["Leo"]
        else:
            voice_id = voice_ids[script["historical_figure"]]
        
        print(f"Generating audio for {speaker}, line {i+1}...")
        exchange_path = os.path.join(output_dir, f"conversation_{i+1}.mp3")
        
        # If this is not the first exchange, use previous exchange for continuity
        previous_text = None
        if i > 0:
            previous_text = script["conversation"][i-1]["text"]
        
        # If this is not the last exchange, use next exchange for continuity
        next_text = None
        if i < len(script["conversation"]) - 1:
            next_text = script["conversation"][i+1]["text"]
        
        exchange_audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2",
            output_format="mp3_44100_128",
            previous_text=previous_text,
            next_text=next_text
        )
        save(exchange_audio, exchange_path)
        segment_paths.append(exchange_path)
        
        # Avoid rate limiting
        time.sleep(0.5)
    
    # Process outro
    print(f"Generating audio for outro...")
    outro_path = os.path.join(output_dir, "outro.mp3")
    outro_audio = generate(
        text=script["outro"],
        voice=voice_ids["Narrator"],
        model="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    save(outro_audio, outro_path)
    segment_paths.append(outro_path)
    
    # Combine all audio segments
    print("Combining all audio segments...")
    combined = AudioSegment.empty()
    
    for path in segment_paths:
        segment = AudioSegment.from_file(path)
        combined += segment
    
    # Save the combined audio
    character_name = script["historical_figure"].replace(" ", "_")
    combined_path = os.path.join(output_dir, f"podcast_{character_name}.mp3")
    combined.export(combined_path, format="mp3")
    
    print(f"Podcast audio generated and saved to {combined_path}")
    return combined_path

def process_script_to_audio(script_json_path):
    """
    Process a script JSON file to generate audio
    
    Args:
        script_json_path (str): Path to the script JSON file
        
    Returns:
        str: Path to the generated audio file
    """
    # Extract character name from the file path
    script_filename = Path(script_json_path).stem
    
    # Create a specific output directory for this podcast
    output_dir = f"output/audio/{script_filename}"
    
    # Generate the podcast audio
    audio_path = generate_podcast_audio(script_json_path, output_dir)
    
    return audio_path
