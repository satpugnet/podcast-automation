import os
import json
import pyperclip
from openai import OpenAI
from dotenv import load_dotenv

def generate_music_prompt(script_json_path):
    """
    Generate a music prompt for Suno.com based on the podcast script
    and copy it to the clipboard.
    
    Args:
        script_json_path (str): Path to the script JSON file
        
    Returns:
        str: The generated music prompt
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    client = OpenAI(api_key=api_key)
    
    # Load the script
    with open(script_json_path, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    historical_figure = script['historical_figure']
    time_period = script.get('time_period', '')
    intro_text = ' '.join([item['text'] for item in script['intro'] if item['speaker'] != 'SFX'])
    
    # Create system prompt
    system_prompt = """
    Create a detailed prompt for a SHORT (10-20 seconds) INSTRUMENTAL background music clip for a historical podcast intro.
    The music should NOT have any lyrics or vocals.
    
    Include:
    1. Musical style/genre that fits the historical figure and time period
    2. Instruments that would be appropriate
    3. Mood and tempo suggestions
    4. Any cultural or historical musical elements
    5. Structure for a brief musical intro
    
    Make the prompt specific for a short background music clip that can loop if needed.
    """
    
    # Create user prompt
    user_prompt = f"""
    Create a music prompt for a SHORT (10-20 seconds) INSTRUMENTAL background music clip (NO LYRICS) for a podcast episode about {historical_figure}.
    
    Time period: {time_period}
    
    Podcast introduction:
    {intro_text}
    
    The music will only play for 10-20 seconds in the background of the podcast intro.
    """
    
    # Copy the prompt to clipboard for manual review if needed
    pyperclip.copy(f"{system_prompt}\n\n{user_prompt}")
    print("\nSystem prompt and user prompt copied to clipboard! 📋")
    
    # Generate the music prompt
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.2"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Extract and copy to clipboard
    music_prompt = response.choices[0].message.content.strip()
    pyperclip.copy(music_prompt)
    
    # Save to file
    output_dir = f"output/{historical_figure.replace(' ', '_')}"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/music_prompt.txt"
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(music_prompt)
    
    print(f"Music prompt for {historical_figure} generated and copied to clipboard!")
    print(f"Saved to {output_path}")
    
    return music_prompt

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python music.py <script_path>")
        sys.exit(1)
    
    generate_music_prompt(script_json_path=sys.argv[1])





