import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import pyperclip


def generate_podcast_script(historical_figure, background_research=None, script_path=None, previous_episodes_character_names=[]):
    """
    Generate a podcast script for the Time Traveler Podcast by sending a request to ChatGPT.
    
    Args:
        historical_figure (str): The name of the historical figure to interview
        background_research (str, optional): Background research about the historical figure
        script_path (str, optional): Path to an existing script file to use instead of generating a new one
    Returns:
        str: Path to the saved podcast script file
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    client = OpenAI(api_key=api_key)
    
    # Construct the system prompt
    with open('src/prompts/script_generation.hbr', 'r', encoding='utf-8') as file:
        system_prompt = file.read()
        system_prompt = system_prompt.format(previous_episodes_characters=', '.join(previous_episodes_character_names))

    user_prompt = f"Create a podcast script for the Time Traveler Podcast interviewing {historical_figure}."
    if background_research:
        user_prompt += f"\n\nHere is background research and factual information about {historical_figure} and their era which has been researched prior to the script being generated that can be used to enrich the script to ensure historical accuracy and educational value:\n\n{background_research}"

    # Initialize messages list for the conversation with the AI
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Copy the prompt to clipboard
    pyperclip.copy(f"{system_prompt}\n\n{user_prompt}")
    print("\nSystem prompt and user prompt copied to clipboard! 📋")
    
    # Make the initial API call
    try:
        print(f"Generating initial podcast script with {os.getenv('OPENAI_MODEL')}...")
        if not script_path:
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL"),
                messages=messages
            )
            
            # Extract and parse the response
            script_json = response.choices[0].message.content
        else:
            with open(script_path, 'r', encoding='utf-8') as file:
                script_json = file.read()
        
        # Try to parse the JSON response
        print("Parsing JSON response...")
        try:
            script = json.loads(script_json)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {script_json}")
            raise
        
        # Add the assistant's response to the messages
        messages.append({"role": "assistant", "content": script_json})
        
        # Save initial script
        iteration = 1
        character_name = script.get("historical_figure", "Unknown")
        save_script_iteration(script, character_name, iteration)
        
        # Estimate script length
        estimated_length = estimate_script_length(script)
        print(f"\nEstimated script length: {estimated_length:.1f} minutes")
        
        # Feedback loop
        while True:
            # Display script preview
            print("\nScript preview:")
            print(f"Title: {script.get('title', 'No title')}")
            print(f"Historical Figure: {script.get('historical_figure', 'Unknown')}")
            print(f"Time Period: {script.get('time_period', 'Unknown')}")
            print(f"Location: {script.get('location', 'Unknown')}")
            
            # Show a sample of the conversation
            conversation = script.get('conversation', [])
            sample_size = min(4, len(conversation))
            if sample_size > 0:
                print("\nConversation sample:")
                for i in range(sample_size):
                    print(f"{conversation[i]['speaker']}: {conversation[i]['text'][:100]}...")
            
            # Copy feedback prompt to clipboard
            with open('src/prompts/feedback.hbr', 'r', encoding='utf-8') as file:
                feedback_template = file.read()
                formatted_feedback_template = feedback_template.format(script=script_json)
                pyperclip.copy(formatted_feedback_template)
                print("\nFeedback prompt copied to clipboard! 📋")

            # Ask for feedback
            user_feedback = input("\nWould you like to provide feedback to improve the script? (leave empty to proceed with current script): ").strip()
            
            if not user_feedback:
                print("Proceeding with the current script.")
                break
            # Generate improved script based on feedback
            print("\nGenerating improved script based on your feedback...")
            
            # Add user feedback to messages
            messages.append({"role": "user", "content": f"Please improve the podcast script based on this feedback: {user_feedback}"})
            
            # Get improved script
            improved_response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL"),
                messages=messages
            )
            
            improved_script_json = improved_response.choices[0].message.content
            
            improved_script = json.loads(improved_script_json)
            print("Script improved successfully!")
            
            # Update the script and messages
            script = improved_script
            messages.append({"role": "assistant", "content": improved_script_json})
            
            # Save this iteration
            iteration += 1
            save_script_iteration(script, character_name, iteration)
            
            # Estimate script length
            estimated_length = estimate_script_length(script)
            print(f"\nEstimated script length: {estimated_length:.1f} minutes")
        
        # Save the final script and return the path
        output_file = save_script_to_file(script)
        return output_file
    
    except Exception as e:
        print(f"Error generating podcast script: {e}")
        raise

def estimate_script_length(script):
    """
    Estimate the length of a podcast script in minutes based on word count
    
    Args:
        script (dict): The podcast script to estimate
    
    Returns:
        float: Estimated length in minutes
    """
    # Average speaking rate (words per minute)
    WORDS_PER_MINUTE = 150
    
    # Count words in all sections except SFX
    total_words = 0
    sfx_time = 0
    
    # Process all script sections
    for section in ['intro', 'arrival_scene', 'conversation', 'outro']:
        for item in script.get(section, []):
            if item.get('speaker') == 'SFX':
                sfx_time += item.get('duration', 0)
            else:
                total_words += len(item.get('text', '').split())
    
    # Calculate total time (speech + SFX)
    speech_time_minutes = total_words / WORDS_PER_MINUTE
    sfx_time_minutes = sfx_time / 60
    
    return speech_time_minutes + sfx_time_minutes

def save_script_iteration(script, character_name, iteration):
    """
    Save a specific iteration of the script during the feedback process
    
    Args:
        script (dict): The podcast script to save
        character_name (str): Name of the historical figure
        iteration (int): The iteration number
    """
    # Create output directory if it doesn't exist
    os.makedirs(f"output/{character_name.replace(' ', '_')}/script_iterations", exist_ok=True)
    
    # Create filename with character name and iteration number
    output_file = f"output/{character_name.replace(' ', '_')}/script_iterations/script_iteration_{iteration}.json"
    
    # Write the script to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(script, f, indent=2, ensure_ascii=False)
    
    print(f"Iteration {iteration} for {character_name} saved to {output_file}")
    
def save_script_to_file(script, output_file=None):
    """
    Save the generated script to a JSON file
    
    Args:
        script (dict): The podcast script to save
        output_file (str, optional): Path to save the script. If None, a filename with the character name will be created.
    Returns:
        str: Path to the saved script file
    """
    # Get character name from the script
    character_name = script.get("historical_figure", "Unknown")
    
    # Create default output filename with character name if not provided
    if output_file is None:
        output_file = f"output/{character_name.replace(' ', '_')}/script.json"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the script to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(script, f, indent=2, ensure_ascii=False)
    
    print(f"Script for {character_name} saved to {output_file}")

    return output_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        historical_figure = sys.argv[1]
        background_research = None
        existing_script_path = None
        
        # Check if additional knowledge file is provided
        if len(sys.argv) > 2:
            with open(sys.argv[2], 'r', encoding='utf-8') as file:
                background_research = file.read()
        
        # Check if existing script path is provided
        if len(sys.argv) > 3:
            existing_script_path = sys.argv[3]
        
        script_path = generate_podcast_script(
            historical_figure=historical_figure, 
            background_research=background_research,
            script_path=existing_script_path,
            previous_episodes_character_names=os.listdir("output")
        )
        print(f"Generated script saved to: {script_path}")
    else:
        print("Usage: python discussion_script.py <historical_figure> [background_research_path] [existing_script_path]")
