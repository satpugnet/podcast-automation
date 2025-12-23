import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

headers = {
    "x-api-key": os.getenv("TRANSISTOR_FM_API_KEY"),
    "Content-Type": "application/json"
}

def authorize_upload(filename):
    print(f"Authorizing upload for file: {filename}")
    url = "https://api.transistor.fm/v1/episodes/authorize_upload"
    params = {"filename": filename}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    print("Upload authorization successful")
    return response.json()

def upload_audio(upload_url, filepath):
    print(f"Starting upload of audio file: {filepath}")
    with open(filepath, 'rb') as file:
        response = requests.put(upload_url, data=file, headers={"Content-Type": "audio/mpeg"})
        response.raise_for_status()
        print("Audio file uploaded successfully.")

def create_episode(title, audio_url, description, transcript_text, image_url=None, keywords=None):
    print(f"Creating episode: '{title}'")
    url = "https://api.transistor.fm/v1/episodes"
    episode_data = {
        "episode": {
            "show_id": os.getenv("TRANSISTOR_FM_SHOW_ID"),
            "title": title,
            "audio_url": audio_url,
            "description": description,
            "transcript_text": transcript_text,
            "keywords": keywords
        }
    }
    
    # Add optional parameters if provided
    if image_url:
        episode_data["episode"]["image_url"] = image_url
        print(f"Using custom image: {image_url}")

    print(f"Creating episode with data: {episode_data}")

    response = requests.post(url, headers=headers, json=episode_data)
    response.raise_for_status()
    return response.json()

def publish_episode_status(episode_id, status="published", published_at=None):
    """
    Publish, schedule, or unpublish an episode.
    
    Args:
        episode_id (str): The ID of the episode to update
        status (str): One of 'published', 'scheduled', or 'draft'
        published_at (str, optional): Episode publishing date and time in podcast's time zone
    
    Returns:
        dict: The updated episode data
    """
    print(f"Updating episode {episode_id} status to: {status}")
    url = f"https://api.transistor.fm/v1/episodes/{episode_id}/publish"
    
    episode_data = {
        "episode": {
            "status": status
        }
    }
    
    # Add published_at if provided
    if published_at:
        episode_data["episode"]["published_at"] = published_at
        print(f"Setting publication date to: {published_at}")

    print(f"Updating episode {episode_id} status to: {episode_data}")
    
    response = requests.patch(url, headers=headers, json=episode_data)
    response.raise_for_status()
    print(f"Episode status updated to {status}")
    return response.json()

def get_next_tuesday_1am():
    """
    Returns the next Tuesday at 1:00 AM as a formatted string in EDT.
    Format: "YYYY-MM-DD HH:MM:SS EDT"
    """
    now = datetime.now()
    days_until_tuesday = (1 - now.weekday()) % 7  # 1 is Tuesday
    if days_until_tuesday == 0 and now.hour >= 1:
        days_until_tuesday = 7  # If it's already Tuesday after 1am, get next Tuesday
    
    next_tuesday = now + timedelta(days=days_until_tuesday)
    next_tuesday = next_tuesday.replace(hour=1, minute=0, second=0, microsecond=0)
    
    return next_tuesday.strftime("%Y-%m-%d %H:%M:%S EDT")

# Main flow
# published_at format is YYYY-MM-DD HH:MM:SS EDT
def publish_episode(script_path, audio_path, transcript_path=None, image_path=None, publish_status="draft", published_at=None):
    # Load the script to extract title and description
    with open(script_path, 'r', encoding='utf-8') as file:
        script = json.load(file)
    
    print(f"Beginning publication process for episode: '{script['title']}'")
    filename = os.path.basename(audio_path)
    authorization = authorize_upload(filename)

    upload_url = authorization["data"]["attributes"]["upload_url"]
    audio_url = authorization["data"]["attributes"]["audio_url"]

    upload_audio(upload_url, audio_path)

    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript_text = f.read()
    
    # Handle image upload if provided
    image_url = None
    if image_path:
        print(f"Image path provided: {image_path}")
        # Note: You would need to implement image upload functionality
        # This could involve uploading to S3 or another service and getting a URL
        pass

    print("Creating episode in Transistor.fm...")
    episode = create_episode(
        title=script["title"],
        audio_url=audio_url,
        description=script["description"],
        transcript_text=transcript_text,
        image_url=image_url
    )

    print("Episode created:", json.dumps(episode, indent=2))
    
    # Publish the episode if requested
    episode_id = episode["data"]["id"]
    if publish_status == "published":
        print(f"Publishing episode {episode_id}...")
        publish_result = publish_episode_status(episode_id, "published")
        print("Episode published:", json.dumps(publish_result, indent=2))
    elif publish_status == "scheduled":
        # Use provided published_at or default to next Tuesday at 1am
        if not published_at:
            published_at = get_next_tuesday_1am()
        print(f"Scheduling episode {episode_id} for {published_at}...")
        publish_result = publish_episode_status(episode_id, "scheduled", published_at)
        print("Episode scheduled:", json.dumps(publish_result, indent=2))

    # Save the publication details to a file
    output_dir = f"output/{script['historical_figure'].replace(' ', '_')}"
    details_path = os.path.join(output_dir, "publishing_details.json")
    os.makedirs(output_dir, exist_ok=True)
    with open(details_path, 'w') as f:
        json.dump({
            "episode_id": episode_id,
            "published_at": published_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S EDT")
        }, f, indent=4)
    
    print(f"Publishing details saved to {details_path}")
    return episode

if __name__ == "__main__":
    import sys
    
    print("Running publication module directly")
    
    if len(sys.argv) < 3:
        print("Usage: python publication.py <script_path> <audio_path> <transcript_path> [image_path] [publish_status] [published_at]")
        sys.exit(1)
    
    script_path = sys.argv[1]
    audio_path = sys.argv[2]
    transcript_path = sys.argv[3]
    image_path = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "None" else None
    publish_status = sys.argv[5] if len(sys.argv) > 5 else "draft"
    published_at = sys.argv[6] if len(sys.argv) > 6 else None
    
    result = publish_episode(
        script_path=script_path,
        audio_path=audio_path,
        transcript_path=transcript_path,
        image_path=image_path,
        publish_status=publish_status,
        published_at=published_at
    )
    
    print(f"Publication process completed. Result: {json.dumps(result, indent=2)}")
