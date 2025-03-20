import os
from dotenv import load_dotenv
from io import BytesIO
import requests
from elevenlabs.client import ElevenLabs
from openai import OpenAI
import json

def seconds_to_timestamp(seconds):
    """Convert seconds to VTT timestamp format (HH:MM:SS.mmm)"""
    millis = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}.{millis:03}"

def identify_speakers(script, transcript_text):
    """
    Use GPT-4o to identify which speaker_id corresponds to which character in the script
    
    Args:
        script (dict): The podcast script with character information
        transcript_text (str): The raw transcript text with speaker_ids
        
    Returns:
        dict: Mapping of speaker_ids to character names
    """
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = """
    You are an expert at analyzing podcast transcripts and identifying speakers.
    Given a podcast script and a transcript with generic speaker IDs, identify which speaker_id corresponds to which character.
    
    Return your answer as a JSON object with the following structure:
    {
        "speaker_mapping": {
            "speaker_0": "Character Name",
            "speaker_1": "Character Name",
            ...
        }
    }
    
    The characters in the podcast are typically:
    - Leo (the time traveler)
    - The historical figure being interviewed
    - Narrator (occasionally)
    
    Base your identification on speech patterns, content, and context from both the script and transcript.
    """
    
    # Extract character information from script
    historical_figure = script.get("historical_figure", "Unknown Historical Figure")
    
    user_prompt = f"""
    Here is information about the podcast:
    
    Historical Figure: {historical_figure}
    
    Here is a sample of the script conversation:
    {json.dumps(script.get('conversation', [])[:10], indent=2)}
    
    Here is a sample of the transcript with generic speaker IDs:
    {transcript_text[:1000]}
    
    Please identify which speaker_id corresponds to which character (Leo, {historical_figure}, or Narrator).
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    try:
        # Extract and parse the response
        content = response.choices[0].message.content
        # Find JSON content (it might be wrapped in markdown code blocks)
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].strip()
        else:
            json_str = content
            
        speaker_mapping = json.loads(json_str)
        return speaker_mapping.get("speaker_mapping", {})
    except Exception as e:
        print(f"Error parsing speaker identification response: {e}")
        print(f"Raw response: {response.choices[0].message.content}")
        # Return empty mapping if parsing fails
        return {}

def generate_vtt_from_audio(script, audio_path, output_file=None):
    load_dotenv()
    client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))

    if audio_path.startswith(('http://', 'https://')):
        response = requests.get(audio_path)
        audio_data = BytesIO(response.content)
    else:
        with open(audio_path, 'rb') as f:
            audio_data = BytesIO(f.read())

    transcription = client.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v1",
        tag_audio_events=True,
        diarize=True,
    )

    if output_file is None:
        output_file = f"output/{script['title'].replace(' ', '_')}/transcript.vtt"

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Create a raw transcript text for speaker identification
    raw_transcript = ""
    for word in transcription.words:
        if not raw_transcript or word.speaker_id != transcription.words[transcription.words.index(word)-1].speaker_id:
            raw_transcript += f"\n<v {word.speaker_id}> "
        raw_transcript += word.text + " "
    
    # Identify speakers if script is provided
    speaker_mapping = {}
    speaker_mapping = identify_speakers(script, raw_transcript)
    print(f"Identified speakers: {speaker_mapping}")
    
    vtt_content = ["WEBVTT\n"]
    words = transcription.words

    segment = []
    segment_start = words[0].start
    segment_end = words[0].end
    current_speaker = words[0].speaker_id

    for word in words:
        if word.speaker_id == current_speaker and (word.start - segment_end) < 1.5:
            segment.append(word.text)
            segment_end = word.end
        else:
            start_timestamp = seconds_to_timestamp(segment_start)
            end_timestamp = seconds_to_timestamp(segment_end)
            text = ' '.join(segment).strip()
            # Fix multiple spaces between words
            text = ' '.join(text.split())
            
            # Use mapped speaker name if available
            speaker_name = speaker_mapping.get(current_speaker, current_speaker)
            
            vtt_content.append(f"{start_timestamp} --> {end_timestamp}")
            vtt_content.append(f"<v {speaker_name}> {text}\n")
            
            segment = [word.text]
            segment_start = word.start
            segment_end = word.end
            current_speaker = word.speaker_id

    if segment:
        start_timestamp = seconds_to_timestamp(segment_start)
        end_timestamp = seconds_to_timestamp(segment_end)
        text = ' '.join(segment).strip()
        # Fix multiple spaces between words
        text = ' '.join(text.split())
        
        # Use mapped speaker name if available
        speaker_name = speaker_mapping.get(current_speaker, current_speaker)
        
        vtt_content.append(f"{start_timestamp} --> {end_timestamp}")
        vtt_content.append(f"<v {speaker_name}> {text}\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(vtt_content))

    print(f"VTT transcript saved to {output_file}")

    return output_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        script_path = sys.argv[1]
        audio_path = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        with open(script_path, 'r', encoding='utf-8') as f:
            script_data = json.load(f)
                
        output_file = generate_vtt_from_audio(script_data, audio_path, output_file)
        print(f"Generated transcript saved to: {output_file}")
    else:
        print("Usage: python transcript.py <script_path> <audio_path> [output_file]")