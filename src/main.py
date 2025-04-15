import argparse
import os
from tools import voice_design
from tools import discussion_script
from tools import audio
from tools import publication
from tools import transcript
from tools import background_search
from tools import social_media
import json


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"{text.center(60)}")
    print("=" * 60)


def print_step(number, title):
    """Print a step header."""
    print_header(f"STEP {number}: {title}")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Time Traveler Podcast Generator")
    parser.add_argument("--character-name", help="Name of the historical character")
    parser.add_argument("--background-research-path", help="Path to the background research file")
    parser.add_argument("--script-path", help="Path to an existing script file")
    parser.add_argument("--guest-voice-id", help="Voice ID for the historical character")
    parser.add_argument("--audio-path", help="Path to an existing audio file")
    parser.add_argument("--transcript-path", help="Path to an existing transcript file")
    parser.add_argument("--social-media-path", help="Path to an existing social media posts file")
    args = parser.parse_args()

    character_name = None
    background_research_path = None
    script_path = None
    guest_voice_id = None
    audio_path = None
    transcript_path = None
    social_media_path = None

    # Welcome message
    print("\n" + "=" * 60)
    print("TIME TRAVELER PODCAST GENERATOR".center(60))
    print("=" * 60)
    print("Create engaging podcasts with historical figures".center(60))
    print("\n")

    # =============================================
    # ========= STEP 1: CHARACTER SELECTION ======
    # =============================================
    print_step(1, "CHARACTER SELECTION")

    character_name = args.character_name
    if not character_name:
        character_name = input("🧠 Enter the name of the historical character: ")
    
    print(f"✅ Historical character selected: {character_name}")

    # =============================================
    # ========= STEP 2: BACKGROUND RESEARCH ======
    # =============================================
    print_step(2, "BACKGROUND RESEARCH")
    
    background_research_path = args.background_research_path
    if not background_research_path:
        print(f"🔄 Preparing background research template for {character_name}...")
        background_search.print_background_search_template(character_name)
        background_research_path = input("📚 Enter background research file path: ").strip()
    
    print(f"🔄 Loading background research from {background_research_path}...")
    with open(background_research_path, 'r', encoding='utf-8') as file:
        background_research = file.read()
        
    print(f"✅ Background research loaded successfully from {background_research_path}")

    # =============================================
    # ========= STEP 3: SCRIPT GENERATION ========
    # =============================================
    print_step(3, "SCRIPT GENERATION")

    script_path = args.script_path
    if script_path:
        print(f"ℹ️ Using script provided via command line: {script_path}")
    else:
        script_path = input("📄 Enter path to existing script file (optional, press Enter to generate new script): ")
        script_path = None if script_path == "" else script_path

        if script_path:
            print(f"ℹ️ Using existing script: {script_path}")
        
        # Generate the script
        print(f"🔄 Generating podcast script for {character_name}...")
        script_path = discussion_script.generate_podcast_script(historical_figure=character_name, background_research=background_research, script_path=script_path)
        print(f"✅ Podcast script generated successfully and saved at path: {script_path}")
    
    print(f"🔄 Loading script data from {script_path}...")
    with open(script_path, 'r', encoding='utf-8') as file:
        script_data = json.load(file)

    print(f"✅ Podcast script generated successfully and saved at path: {script_path}")

    # =============================================
    # ========= STEP 4: VOICE GENERATION =========
    # =============================================
    print_step(4, "VOICE GENERATION")
    
    guest_voice_id = args.guest_voice_id
    if not guest_voice_id:
        if input("🎙️ Generate character voice? (yes/no): ").lower().strip() in ["yes", "y"]:
            print(f"🔄 Generating voice for {character_name}...")
            guest_voice_id, voice_file_path = voice_design.generate_voice(character_name=character_name)
            print(f"✅ Voice generated successfully! Voice ID: {guest_voice_id}")
        else:
            print("⏭️ Voice generation skipped.")
            guest_voice_id = input("🗣️ No voice ID found. Please enter the voice ID for the historical figure: ")
    
    print(f"✅ Voice ID set to: {guest_voice_id}, Voice ID saved at path: {voice_file_path}")

    # =============================================
    # ========= STEP 5: AUDIO GENERATION =========
    # =============================================
    print_step(5, "AUDIO GENERATION")

    audio_path = args.audio_path
    if audio_path:
        print(f"ℹ️ Using audio provided via command line: {audio_path}")
    else:
        input("🔊 Generating podcast audio, press Enter to continue...")

        print(f"🔄 Generating podcast audio for script at {script_path}...")
        audio_path = audio.process_script_to_audio(script_path, guest_voice_id)
    
    print(f"✅ Podcast audio generated successfully and saved at path: {audio_path}")

    # =============================================
    # ======= STEP 6: TRANSCRIPT GENERATION ======
    # =============================================
    print_step(6, "TRANSCRIPT GENERATION")

    transcript_path = args.transcript_path
    if transcript_path:
        print(f"ℹ️ Using transcript provided via command line: {transcript_path}")
    else:
        input("📝 Generating podcast transcript, press Enter to continue...")
        print(f"🔄 Generating transcript for {script_data['title']}...")
        transcript_path = transcript.generate_vtt_from_audio(script_data, audio_path)
    
    print(f"✅ Transcript generated successfully and saved at path: {transcript_path}")

    # =============================================
    # ======= STEP 7: SOCIAL MEDIA POSTS =========
    # =============================================
    print_step(7, "SOCIAL MEDIA POSTS")
    
    social_media_path = args.social_media_path
    if social_media_path:
        print(f"ℹ️ Using social media posts provided via command line: {social_media_path}")
    else:
        input("📱 Generating social media posts, press Enter to continue...")
        print(f"🔄 Generating social media posts for {script_data['title']}...")
        posts, social_media_path = social_media.generate_social_media_posts(
            script_path=script_path,
            background_research=background_research
        )
    
    print(f"✅ Social media posts generated successfully and saved at path: {social_media_path}")

    # =============================================
    # ======= STEP 8: EPISODE PUBLICATION ========
    # =============================================
    print_step(8, "EPISODE PUBLICATION")
       
    image_path = input("🖼️ Enter the path to the episode image (optional, press Enter to skip): ")
    image_path = image_path if image_path else None
    
    publish_option = input("⏱️ Choose publication option - publish now (p), save as draft (d), or skip (any other key): ").lower().strip()
    publish_now = publish_option == "p"
    save_as_draft = publish_option == "d"
    
    if not (publish_now or save_as_draft):
        print("⏭️ Episode publication skipped.")
        return
    
    print(f"🔄 Publishing episode '{script_data['title']}'...")
    episode = publication.publish_episode(
        script_path=script_path,
        audio_path=audio_path,
        transcript_path=transcript_path,
        image_path=image_path,
        publish_now=publish_now
    )
    print(f"🎉 Episode '{script_data['title']}' published successfully!")

    # =============================================
    # ============= COMPLETION MESSAGE ===========
    # =============================================
    print_header("PODCAST GENERATION COMPLETE")
    print("🎉 Thank you for using Time Traveler Podcast Generator! 🎉".center(60))
    print("🚀 Your journey through history continues... ⏳".center(60))


if __name__ == "__main__":
    main()