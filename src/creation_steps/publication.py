import requests
import os
import json
from dotenv import load_dotenv

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

def create_episode(title, audio_url, description, image_url=None):
    print(f"Creating episode: '{title}'")
    url = "https://api.transistor.fm/v1/episodes"
    episode_data = {
        "episode": {
            "show_id": os.getenv("TRANSISTOR_FM_SHOW_ID"),
            "title": title,
            "audio_url": audio_url,
            "description": description
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

def publish_episode_status(episode_id, status="published"):
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
    
    data = {
        "episode[status]": status
    }
    
    response = requests.patch(url, headers=headers, data=data)
    response.raise_for_status()
    print(f"Episode status updated to {status}")
    return response.json()

# Main flow
def publish_episode(title, audio_path, description, image_path=None, publish_now=False):
    print(f"Beginning publication process for episode: '{title}'")
    filename = os.path.basename(audio_path)
    authorization = authorize_upload(filename)

    upload_url = authorization["data"]["attributes"]["upload_url"]
    audio_url = authorization["data"]["attributes"]["audio_url"]

    upload_audio(upload_url, audio_path)
    
    # Handle image upload if provided
    image_url = None
    if image_path:
        print(f"Image path provided: {image_path}")
        # Note: You would need to implement image upload functionality
        # This could involve uploading to S3 or another service and getting a URL
        pass

    print("Creating episode in Transistor.fm...")
    episode = create_episode(
        title=title,
        audio_url=audio_url,
        description=description,
        image_url=image_url
    )

    print("Episode created:", json.dumps(episode, indent=2))
    
    # Publish the episode if requested
    if publish_now:
        episode_id = episode["data"]["id"]
        status = "published"
        print(f"Publishing episode {episode_id}...")
        publish_result = publish_episode_status(episode_id, status)
        print("Episode published:", json.dumps(publish_result, indent=2))
    
    return episode

if __name__ == "__main__":
    print("Running publication module directly")
    publish_episode(
        title="Test Episode",
        audio_path="./old_output/Napoleon_Bonaparte/audio/podcast_Napoleon_Bonaparte.mp3",
        description="This is a test episode",
        publish_now=False
    )
