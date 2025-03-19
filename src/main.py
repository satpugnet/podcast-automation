from tools import voice_design
from tools import discussion_script
from tools import audio
from tools import publication
from tools import discussion_script
import json

script_path = None
guest_voice_id = None
audio_path = None

# Ask user for the character name
character_name = input("Enter the name of the historical character 🧠: ")

generate_voice = input("Generate character voice? (yes/no) 🎙️: ")

# Skip voice generation if character name is empty
if not generate_voice in ["yes", "y"]:
    print("Voice generation skipped. ⏭️")
else:
    # Call the generate_voice_preview function only if user confirms by typing the character name
    guest_voice_id = voice_design.generate_voice_preview(character_name=character_name)


# Ask user if they want to generate a podcast script
generate_script = input("Generate podcast script? (yes/no) 📝: ").lower().strip()

if generate_script in ["yes", "y"]:
    script_path = input("Enter path to existing script file (optional, press Enter to generate new script) 📄: ")
    script_path = None if script_path == "" else script_path

    # Optional additional knowledge
    additional_knowledge_file_path = input("Enter additional knowledge file path (optional, press Enter to skip) 📚: ").strip()
    additional_knowledge = None
    if additional_knowledge_file_path:
        with open(additional_knowledge_file_path, 'r', encoding='utf-8') as file:
            additional_knowledge = file.read()
    
    # Generate the script
    print(f"Generating podcast script for {character_name}... ✍️")
    script = discussion_script.generate_podcast_script(character_name, additional_knowledge)
    
    # Save the script
    script_path = discussion_script.save_script_to_file(script, script_path)
    print(f"Podcast script for {character_name} generated successfully! ✅")
else:
    print("Podcast script generation skipped. ⏭️")

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

# Ask user if they want to publish the podcast
publish_podcast = input("Publish podcast to Transistor.fm? (yes/no) 🚀: ").lower().strip()

if publish_podcast in ["yes", "y"]:
    if not audio_path:
        audio_path = input("No audio file found. Please enter the path to the audio file 🔍: ")
    
    # Load the script JSON to use for the description
    if not script_path:
        script_path = input("No script file found. Please enter the path to the script file 📄: ")
    
    with open(script_path, 'r', encoding='utf-8') as file:
        script_data = json.load(file)
    
    # Use the title and description from the script if available, otherwise create one
    description = script_data["description"]
    title = script_data["title"]
    
    image_path = input("Enter the path to the episode image, note that it does not work yet and needs to be implemented (optional, press Enter to skip) 🖼️: ").strip()
    image_path = image_path if image_path else None
    
    publish_now = input("Publish episode immediately? (yes/no) ⏱️: ").lower().strip() in ["yes", "y"]
    
    print(f"Publishing podcast episode '{title}'... 📡")
    episode = publication.publish_episode(
        title=title,
        audio_path=audio_path,
        description=description,
        image_path=image_path,
        publish_now=publish_now
    )
    print(f"Podcast episode '{title}' published successfully! 🎉")
else:
    print("Podcast publication skipped. ⏭️")