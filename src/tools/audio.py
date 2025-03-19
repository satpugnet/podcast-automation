import os
import json
import time
from pathlib import Path
from pydub import AudioSegment
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

def generate_podcast_audio(script, guest_voice_id, output_dir):
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
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_LABS_API_KEY not found in environment variables")
    
    # Initialize ElevenLabs client
    client = ElevenLabs(api_key=api_key)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "segments"), exist_ok=True)
    
    # Define voice IDs for each speaker
    voice_ids = {
        "Narrator": "NOpBlnGInO9m6vDvFkFC",  # Adam voice for intro and outro
        "Leo": "v2YwWtvprj8WUvzb7D4K", 
        script["historical_figure"]: guest_voice_id
    }
    # Generate audio segments
    audio_segments = []
    segment_paths = []
    
    # Process intro
    print(f"Generating audio for intro...")
    intro_path = os.path.join(output_dir, "segments/intro.mp3")
    intro_audio = client.text_to_speech.convert(
        text=script["intro"],
        voice_id=voice_ids["Narrator"],
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    # Convert generator to bytes
    intro_audio_bytes = b"".join(list(intro_audio))
    with open(intro_path, "wb") as f:
        f.write(intro_audio_bytes)
    segment_paths.append(intro_path)
    
    # Process arrival scene
    print(f"Generating audio for arrival scene...")
    arrival_path = os.path.join(output_dir, "segments/arrival_scene.mp3")
    arrival_audio = client.text_to_speech.convert(
        text=script["arrival_scene"],
        voice_id=voice_ids["Narrator"],
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    # Convert generator to bytes
    arrival_audio_bytes = b"".join(list(arrival_audio))
    with open(arrival_path, "wb") as f:
        f.write(arrival_audio_bytes)
    segment_paths.append(arrival_path)
    
    # Process conversation
    for i, exchange in enumerate(script["conversation"]):
        speaker = exchange["speaker"]
        text = exchange["text"]
        
        # Determine which voice to use
        if speaker == "Leo":
            voice_id = voice_ids["Leo"]
        elif speaker == "Narrator":
            voice_id = voice_ids["Narrator"]
        else:
            voice_id = voice_ids[script["historical_figure"]]
        
        print(f"Generating audio for {speaker}, line {i+1}...")
        exchange_path = os.path.join(output_dir, f"segments/conversation_{i+1}.mp3")
        
        exchange_audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        # Convert generator to bytes
        exchange_audio_bytes = b"".join(list(exchange_audio))
        with open(exchange_path, "wb") as f:
            f.write(exchange_audio_bytes)
        segment_paths.append(exchange_path)
        
        # Avoid rate limiting
        time.sleep(0.5)
    
    # Process outro
    print(f"Generating audio for outro...")
    outro_path = os.path.join(output_dir, "segments/outro.mp3")
    outro_audio = client.text_to_speech.convert(
        text=script["outro"],
        voice_id=voice_ids["Narrator"],
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    # Convert generator to bytes
    outro_audio_bytes = b"".join(list(outro_audio))
    with open(outro_path, "wb") as f:
        f.write(outro_audio_bytes)
    segment_paths.append(outro_path)
    
    # Combine all audio segments
    print("Combining all audio segments...")
    combined = AudioSegment.empty()
    
    # Add a short pause between segments (500ms silence)
    pause = AudioSegment.silent(duration=1200)
    
    for path in segment_paths:
        segment = AudioSegment.from_file(path)
        combined += segment
        combined += pause  # Add pause after each segment
    
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