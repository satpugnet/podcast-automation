from dotenv import load_dotenv
import base64
import os
import logging
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
import openai
import json

def generate_voice_description(character_name, max_characters=1000):
    """Generate a voice description for a historical character using OpenAI."""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    Create a detailed voice description for the historical figure {character_name}. Make it short but comprehensive and complete. It needs to be under {int(max_characters * 0.7)} characters.
    The description should:
    1. Capture how this historical figure might have sounded based on historical accounts and documentation
    2. Include specific vocal qualities (pitch, resonance, breathiness), accent details, speech patterns, cadence, and emotional tone that would be authentic to their time period, region, and background
    3. Consider their personality, education level, social status, profession, and complete historical context
    4. Be comprehensive enough for voice synthesis (3-4 sentences) while remaining focused on distinctive vocal characteristics
    5. Mention any known speech impediments, unique verbal mannerisms, or notable speaking styles from historical records if available
    6. Include specific references to the era they lived in and how that might have influenced their speech patterns
    7. Specify the sex of the historical figure to ensure appropriate voice characteristics
    8. Ensure the voice carries appropriate emotion - whether passionate conviction, quiet determination, scholarly enthusiasm, or other emotions that would be characteristic of this historical figure's personality and circumstances
    
    Important: Do not mention the historical figure's name in the description itself. Refer to them using pronouns or as "the speaker" instead.
    """
    
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {"role": "system", "content": "You are a historical voice expert who specializes in creating authentic voice profiles for historical figures based on primary sources, biographical accounts, and period-appropriate linguistic patterns."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=int(max_characters/6)
    )
    
    voice_description = response.choices[0].message.content.strip()
    logging.info(f"Generated historical voice description ({len(voice_description)} characters): {voice_description}")
    return voice_description

def generate_voice(character_name):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"Starting voice preview generation for historical figure: {character_name}")
    
    load_dotenv()

    # Generate voice description using OpenAI
    voice_description = generate_voice_description(character_name, max_characters=1000)
    
    while True:
        client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))

        # Create voice previews with a historically appropriate sample text
        sample_text = f"I am {character_name}. My words and actions have shaped history, and through this voice, you can hear an approximation of how I might have sounded during my time."
        
        previews_response = client.text_to_voice.create_previews(
            voice_description=voice_description,
            text=sample_text,
            quality=0.80,
            guidance_scale=80.0
        )

        if not previews_response.previews:
            logging.error("No voice previews generated.")
            return

        logging.info("Voice previews generated successfully")
        
        # Play each audio preview
        for i, preview in enumerate(previews_response.previews):
            generated_voice_id = preview.generated_voice_id
            logging.info(f"Preview {i+1} - Generated voice ID: {generated_voice_id}")

            # Decode and play the audio preview
            audio_bytes = base64.b64decode(preview.audio_base_64)
            logging.info(f"Playing audio preview {i+1}")
            play(audio_bytes)
        
        # Ask user to select a voice or restart
        while True:
            user_choice = input("Enter 1, 2, or 3 to select a voice, or 'r' to restart voice generation: ")
            
            if user_choice.lower() == 'r':
                logging.info("Restarting voice generation...")
                break
            
            try:
                choice_index = int(user_choice) - 1
                if 0 <= choice_index < len(previews_response.previews):
                    selected_preview = previews_response.previews[choice_index]
                    
                    # Create a voice from the selected preview
                    voice_response = client.text_to_voice.create_voice_from_preview(
                        voice_name=f"{character_name} - Historical Voice",
                        voice_description=generate_voice_description(character_name, max_characters=500),
                        generated_voice_id=selected_preview.generated_voice_id,
                    )

                    logging.info(f"Historical voice creation completed. New Voice ID: {voice_response.voice_id}")
                    
                    # Save the voice ID to a file
                    voice_file_path = os.path.join(os.path.join("output", character_name.replace(" ", "_")), "voice_id.json")
                    os.makedirs(os.path.dirname(voice_file_path), exist_ok=True)
                    with open(voice_file_path, 'w') as f:
                        json.dump({"voice_id": voice_response.voice_id}, f, indent=4)
                    
                    logging.info(f"Voice ID saved to {voice_file_path}")
                    return voice_response.voice_id, voice_file_path
                else:
                    print(f"Please enter a number between 1 and {len(previews_response.previews)}")
            except ValueError:
                print("Invalid input. Please enter a number or 'r'")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        character_name = sys.argv[1]
        voice_id, voice_file_path = generate_voice(character_name)
        print(f"Generated voice ID for {character_name}: {voice_id}")
        print(f"Voice ID saved to {voice_file_path}")
    else:
        print("Usage: python voice_design.py <character_name>")
