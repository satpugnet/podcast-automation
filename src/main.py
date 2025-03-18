from creation_steps import voice_design
from creation_steps import discussion_script
from creation_steps import audio
import sys
import os

# Ask user for the character name
character_name = input("Enter the name of the historical character: ")

generate_voice = input("Generate character voice? (yes/no): ")

# Skip voice generation if character name is empty
if not generate_voice in ["yes", "y"]:
    print("Voice generation skipped.")
else:
    # Call the generate_voice_preview function only if user confirms by typing the character name
    voice_design.generate_voice_preview(character_name=character_name)


# Ask user if they want to generate a podcast script
generate_script = input("Generate podcast script? (yes/no): ").lower().strip()

if generate_script in ["yes", "y"]:
    from creation_steps import discussion_script
    
    # Optional episode theme
    episode_theme = input("Enter episode theme (optional, press Enter to skip): ").strip()
    episode_theme = episode_theme if episode_theme else None

    # Optional episode setting
    episode_setting = input("Enter episode setting (optional, press Enter to skip): ").strip()
    episode_setting = episode_setting if episode_setting else None
    
    # Generate the script
    print(f"Generating podcast script for {character_name}...")
    script = discussion_script.generate_podcast_script(character_name, episode_theme, episode_setting)
    
    # Save the script
    script_path = discussion_script.save_script_to_file(script)
    print(f"Podcast script for {character_name} generated successfully!")
else:
    print("Podcast script generation skipped.")

# Ask user if they want to generate audio
generate_audio = input("Generate podcast audio? (yes/no): ").lower().strip()

if generate_audio in ["yes", "y"]:
    script_path_input = input("Enter the path to the script file (press Enter to use the default one): ")
    script_path = script_path_input if script_path_input else script_path
    
    print(f"Generating podcast audio for podcast script at {script_path}...")
    audio_path = audio.process_script_to_audio(script_path)
    print(f"Podcast audio for {script_path} generated successfully at {audio_path}")
else:
    print("Podcast audio generation skipped.")