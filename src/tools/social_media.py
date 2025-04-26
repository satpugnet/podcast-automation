import os
import json
from openai import OpenAI
from dotenv import load_dotenv

def generate_social_media_posts(script_path, background_research=None, output_path=None):
    """
    Generate social media posts for LinkedIn and X (Twitter) using ChatGPT based on podcast script.
    
    Args:
        script_path (str): Path to the podcast script JSON file
        background_research (str, optional): Background research about the historical figure
        output_path (str, optional): Path to save the generated social media posts
        
    Returns:
        dict: Generated social media posts for different platforms
        str: Path to the saved social media posts file
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    client = OpenAI(api_key=api_key)
    
    # Load the podcast script
    with open(script_path, 'r', encoding='utf-8') as file:
        script_data = json.load(file)
    
    historical_figure = script_data.get('historical_figure', script_data.get('title'))
    
    # Extract full script content
    script_content = json.dumps(script_data, ensure_ascii=False)
    
    # Construct the system prompt
    system_prompt = """
    You're helping me write concise, engaging social media posts for my personal LinkedIn and X (Twitter) accounts about a new episode of my podcast "Echoes Through Time." In this podcast, I use AI to create immersive conversations between Leo, a fictional time-traveling host, and fascinating historical figures.

    Audience: The general public, but leaning towards intellectually curious people with a bias toward tech-minded audiences.

    Writing Style: Channel the tone of writers like Tim Urban (WaitButWhy), Sam Altman, and Bartosz Ciechanowski—curious, thoughtful, slightly self-deprecating, and conversational. Add occasional parenthetical asides (that feel like little thought bubbles). Use an approachable yet intellectually engaging voice, making complex historical topics accessible without oversimplifying.

    Emphasis: Primarily highlight intriguing historical facts about the figure, but also weave in some philosophical insights, personal reflections, and contextual details of their era—without overly fixating on any single aspect.

    Each post should follow this clear structure:
    1. Announcement: Briefly state a new episode is out, clearly mentioning the episode's title "{historical_figure}".
    2. Summary: Provide a concise, engaging paragraph highlighting intriguing facts about {historical_figure}, their era, noteworthy context, and why they're historically significant. Sprinkle in thoughtful reflections and philosophical insights naturally.
    3. Invitation: Conclude with a genuine, friendly invitation to explore the episode for deeper insights. Avoid any promotional or pushy language—think more of sharing something personally fascinating rather than marketing.

    Tone should remain authentic, calm (no exclamations), intellectually stimulating, and personal, reflecting a thoughtful and cool side project I'm genuinely excited to share—nothing corporate or cringe. Do NOT use hashtags.

    Platform specifics:
    - LinkedIn: Professional yet personal (~800 characters), structured clearly into three short paragraphs.
    - X/Twitter: Punchy, casual, engaging (max 280 characters), structured into two short paragraphs—concise announcement and summary combined first, followed by a separate friendly invitation.

    Return your response strictly as JSON, no markdown, syntax highlighting, ```json or ```:

    {
        "linkedin": "...",
        "x": "..."
    }
    
    Important: Use actual line breaks in your response, not the escape sequence \\n.
    """
    # Construct the user prompt
    user_prompt = f"""
    Create social media posts for our new podcast episode featuring {historical_figure}.
    
    Here is the full script of the episode for context:
    {script_content}
    """
    
    # Add background research if provided
    if background_research:
        user_prompt += f"\n\nBackground research about {historical_figure} performed prior to the episode generation:\n{background_research}"
    
    # Initialize messages list for the conversation with the AI
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Call ChatGPT API to generate social media posts
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),  # or another appropriate model
        messages=messages
    )
    
    # Extract the generated content
    generated_content = response.choices[0].message.content
    
    # Add the assistant's response to the messages
    messages.append({"role": "assistant", "content": generated_content})
    
    # Parse the JSON response
    try:
        posts = json.loads(generated_content)
    except json.JSONDecodeError:
        print("Error: Received invalid JSON response. Please try again. generated_content: ", generated_content)
        return None, None

    # Save to file
    save_path = save_social_media_posts(posts, historical_figure, output_path)
    
    # Feedback loop
    while True:
        print("\nGenerated LinkedIn Post:")
        print(posts["linkedin"])
        print("\nGenerated X (Twitter) Post:")
        print(posts["x"])
        
        feedback_prompt = input("Would you like to provide feedback to improve the post? (press Enter to skip): ")
        if not feedback_prompt.strip():
            break
            
        # Add user feedback to messages
        messages.append({"role": "user", "content": feedback_prompt})
        
        # Get improved posts based on feedback
        print("\nGenerating improved posts based on your feedback...")
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=messages
        )
        
        # Extract the updated content
        generated_content = response.choices[0].message.content
        messages.append({"role": "assistant", "content": generated_content})
        
        # Parse the JSON response
        try:
            posts = json.loads(generated_content)
            # Update the saved file
            save_path = save_social_media_posts(posts, historical_figure, output_path)
        except json.JSONDecodeError:
            print("Error: Received invalid JSON response. Please try again.")
    
    return posts, save_path

def save_social_media_posts(posts, historical_figure, output_path=None):
    """
    Save the generated social media posts to a file.
    
    Args:
        posts (dict): Dictionary containing LinkedIn and X posts
        historical_figure (str): Name of the historical figure
        output_path (str, optional): Path to save the file
        
    Returns:
        str: Path to the saved file
    """
    # Create a default filename if not provided
    if not output_path:
        # Create output directory with character name
        output_dir = f"output/{historical_figure.replace(' ', '_')}"
        os.makedirs(output_dir, exist_ok=True)
        output_path = f"{output_dir}/social_media_posts.json"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the posts to a JSON file
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=2, ensure_ascii=False)
    
    print(f"Social media posts saved to {output_path}")
    return output_path

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python social_media.py <script_path> [background_research_path] [output_path]")
        sys.exit(1)
    
    script_path = sys.argv[1]
    
    background_research = None
    if len(sys.argv) > 2 and sys.argv[2] != "None":
        with open(sys.argv[2], 'r', encoding='utf-8') as file:
            background_research = file.read()
    
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    posts, save_path = generate_social_media_posts(
        script_path=script_path,
        background_research=background_research,
        output_path=output_path
    )
