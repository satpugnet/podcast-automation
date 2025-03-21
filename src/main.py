from tools import voice_design
from tools import discussion_script
from tools import audio
from tools import publication
from tools import discussion_script
from tools import transcript
import json

script_path = None
guest_voice_id = None
audio_path = None

# =============================================
# ========= STEP 1: CHARACTER SELECTION ======
# =============================================

# Ask user for the character name
character_name = input("Enter the name of the historical character 🧠: ")

# =============================================
# ========= STEP 2: VOICE GENERATION =========
# =============================================

generate_voice = input("Generate character voice? (yes/no) 🎙️: ")

# Skip voice generation if character name is empty
if not generate_voice in ["yes", "y"]:
    print("Voice generation skipped. ⏭️")
else:
    # Call the generate_voice function only if user confirms by typing the character name
    guest_voice_id = voice_design.generate_voice(character_name=character_name)

# =============================================
# ========= STEP 3: SCRIPT GENERATION ========
# =============================================

# Ask user if they want to generate a podcast script
generate_script = input("Generate podcast script? (yes/no) 📝: ").lower().strip()

if generate_script in ["yes", "y"]:
    script_path = input("Enter path to existing script file (optional, press Enter to generate new script) 📄: ")
    script_path = None if script_path == "" else script_path

    # Optional additional knowledge
    background_research_file_path = input("Enter background research file path (optional, press Enter to skip) 📚: ").strip()
    background_research = None
    if background_research_file_path:
        with open(background_research_file_path, 'r', encoding='utf-8') as file:
            background_research = file.read()
    
    # Generate the script
    print(f"Generating podcast script for {character_name}... ✍️")
    script_path = discussion_script.generate_podcast_script(historical_figure=character_name, background_research=background_research, script_path=script_path)
    print(f"Podcast script for {character_name} generated successfully! ✅")
else:
    print("Podcast script generation skipped. ⏭️")

# =============================================
# ========= STEP 4: AUDIO GENERATION =========
# =============================================

# Ask user if they want to generate audio
generate_audio = input("Generate podcast audio? (yes/no) 🔊: ").lower().strip()

if generate_audio in ["yes", "y"]:
    if not script_path:
        script_path = input("No script file found. Please enter the path to the script file 📄: ")

    if not guest_voice_id:
        guest_voice_id = input("No voice ID found. Please enter the voice ID for the historical figure 🗣️: ")
    
    print(f"Generating podcast audio for podcast script at {script_path}... 🎵")
    audio_path = audio.process_script_to_audio(script_path, guest_voice_id)
    print(f"Podcast audio for {script_path} generated successfully at {audio_path} 🎧")
else:
    print("Podcast audio generation skipped. ⏭️")

# =============================================
# ======= STEP 5: TRANSCRIPT GENERATION ======
# =============================================

generate_transcript = input("Generate podcast transcript? (yes/no) 📝: ").lower().strip()

if generate_transcript in ["yes", "y"]:
    if not audio_path:
        audio_path = input("No audio file found. Please enter the path to the audio file 🔍: ")
    
    if not script_path:
        script_path = input("No script file found. Please enter the path to the script file 📄: ")
    
    with open(script_path, 'r', encoding='utf-8') as file:
        script_data = json.load(file)
    
    print(f"Generating transcript for {script_data['title']}... 📝")
    transcript_path = transcript.generate_vtt_from_audio(script_data, audio_path)
    print(f"Transcript generated successfully at {transcript_path} ✅")
else:
    print("Transcript generation skipped. ⏭️")

# =============================================
# ======= STEP 6: EPISODE PUBLICATION ========
# =============================================

# Ask user if they want to publish the episode
publish_episode = input("Publish episode to Transistor.fm? (yes/no) 🚀: ").lower().strip()

if publish_episode in ["yes", "y"]:
    if not audio_path:
        audio_path = input("No audio file found. Please enter the path to the audio file 🔍: ")
    
    if not transcript_path:
        transcript_path = input("No transcript file found. Please enter the path to the transcript file 📄: ")
    
    # Load the script JSON to use for the description
    if not script_path:
        script_path = input("No script file found. Please enter the path to the script file 📄: ")
    
    with open(script_path, 'r', encoding='utf-8') as file:
        script_data = json.load(file)
    
    image_path = input("Enter the path to the episode image, note that it does not work yet and needs to be implemented (optional, press Enter to skip) 🖼️: ")
    image_path = image_path if image_path else None
    
    publish_now = input("Publish episode immediately? (yes/no) ⏱️: ").lower().strip() in ["yes", "y"]
    
    print(f"Publishing episode '{script_data['title']}'... 📡")
    episode = publication.publish_episode(
        script_path=script_path,
        audio_path=audio_path,
        transcript_path=transcript_path,
        image_path=image_path,
        publish_now=publish_now
    )
    print(f"Episode '{script_data['title']}' published successfully! 🎉")
else:
    print("Episode publication skipped. ⏭️")