import os
import json
from openai import OpenAI
from dotenv import load_dotenv

def generate_podcast_script(historical_figure, episode_theme=None, episode_setting=None):
    """
    Generate a podcast script for the Time Traveler Podcast by sending a request to ChatGPT.
    
    Args:
        historical_figure (str): The name of the historical figure to interview
        episode_theme (str, optional): Specific theme or focus for the episode
        episode_setting (str, optional): Specific setting or location for the episode
        
    Returns:
        dict: A structured podcast script with sections for intro, arrival scene, conversation, and outro
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    client = OpenAI(api_key=api_key)
    
    # Construct the system prompt
    system_prompt = """
    Create a richly detailed, engaging, and immersive podcast script (~20 minutes) featuring Leo, a curious, empathetic, and thoughtful Time Traveler, engaging in a dynamic, conversational interaction with a notable historical figure. The dialogue should flow naturally, with seamless transitions from lighter, intriguing topics into deeper, introspective discussions. Ensure historical accuracy blended creatively with speculative insights, providing a vivid portrayal of the historical figure's life, personality, motivations, struggles, achievements, and broader impact on history.

    Detailed Structure:

    1. Intro (1 min):
       - Begin with an intriguing narrative hook or fascinating anecdote that captures listeners' curiosity immediately.
       - Briefly introduce the historical figure, emphasizing why their story resonates today.

    2. Arrival Scene (1-2 mins):
       - Set a vivid, immersive scene rich in sensory detail (visuals, sounds, atmosphere) that transports listeners directly into the historical context.
       - Depict Leo's gentle and believable arrival into the setting, smoothly transitioning into the first interaction without abruptness.

    3. Conversation (15-18 mins):
       - Open the dialogue casually, establishing rapport and easing into the conversation naturally before gradually deepening the discussion.
       - Avoid overly sharp or direct initial questions. Instead, start with relatable or intriguing points of mutual interest to set a comfortable conversational tone.
       - Progress fluidly through key events, personal anecdotes, emotional challenges, notable achievements, and formative experiences of the historical figure.
       - Encourage genuine, spontaneous exchanges and organic emotional depth, allowing for introspection, humor, and meaningful reflection.
       - Integrate historical context naturally within dialogue, enhancing listener understanding without interrupting conversational flow.
       - Maintain dynamic exchanges, alternating seamlessly between curiosity-driven inquiries from Leo and thoughtful storytelling by the historical figure.

    4. Outro (1 min):
       - Provide a concise yet reflective summary highlighting core insights from the conversation.
       - Share an inspiring or thought-provoking takeaway for listeners.
       - Briefly tease the next episode's historical figure or theme to sustain audience anticipation.

    Tone: Warm, conversational, intellectually engaging, empathetic, subtly humorous, reflective, approachable, and authentic.

    Characterization:
    - Leo (Time Traveler): Deeply curious, empathetic listener, intellectually humble, warmly humorous, adaptable conversationalist, reflective and balanced in neutrality.
    - Narrator: Calm authority, welcoming presence, concise yet polished eloquence, intellectually accessible and subtly charming.

    IMPORTANT: Format your response strictly as a JSON object with the following structure:
    {
        "title": "Episode title",
        "historical_figure": "Name of the historical figure",
        "time_period": "Time period of the conversation",
        "location": "Location of the conversation",
        "intro": "Full intro text",
        "arrival_scene": "Full arrival scene text",
        "conversation": [
            {"speaker": "Leo", "text": "..."},
            {"speaker": "Historical Figure", "text": "..."},
            ...
        ],
        "outro": "Full outro text"
    }
    """
    
    # Construct the user prompt
    user_prompt = f"Create a podcast script for the Time Traveler Podcast interviewing {historical_figure}."
    if episode_theme:
        user_prompt += f" The episode should focus on {episode_theme}."
    if episode_setting:
        user_prompt += f" The conversation should take place in {episode_setting}."
    
    # Initialize messages list for the conversation with the AI
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Make the initial API call
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        
        # Extract and parse the response
        script_json = response.choices[0].message.content
        
        # Try to parse the JSON response
        try:
            script = json.loads(script_json)
            
            # Add the assistant's response to the messages
            messages.append({"role": "assistant", "content": script_json})
            
            # Save initial script
            iteration = 1
            character_name = script.get("historical_figure", "Unknown")
            save_script_iteration(script, character_name, iteration)
            
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
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.7
                )
                
                improved_script_json = improved_response.choices[0].message.content
                
                try:
                    improved_script = json.loads(improved_script_json)
                    print("Script improved successfully!")
                    
                    # Update the script and messages
                    script = improved_script
                    messages.append({"role": "assistant", "content": improved_script_json})
                    
                    # Save this iteration
                    iteration += 1
                    save_script_iteration(script, character_name, iteration)
                    
                except json.JSONDecodeError:
                    print("Could not parse the improved script. Keeping the previous version.")
                    # Try to extract JSON from the text
                    import re
                    json_match = re.search(r'({[\s\S]*})', improved_script_json)
                    if json_match:
                        try:
                            improved_script = json.loads(json_match.group(1))
                            script = improved_script
                            messages.append({"role": "assistant", "content": improved_script_json})
                            print("Script improved successfully after extraction!")
                            
                            # Save this iteration
                            iteration += 1
                            save_script_iteration(script, character_name, iteration)
                        except json.JSONDecodeError:
                            print("Failed to extract valid JSON. Keeping the previous version.")
                    else:
                        print("No JSON found in the response. Keeping the previous version.")
            
            return script
            
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the text
            import re
            json_match = re.search(r'({[\s\S]*})', script_json)
            if json_match:
                try:
                    script = json.loads(json_match.group(1))
                    return script
                except json.JSONDecodeError:
                    raise ValueError("Failed to parse JSON from the API response")
            else:
                raise ValueError("No JSON found in the API response")
    
    except Exception as e:
        print(f"Error generating podcast script: {e}")
        raise

def save_script_iteration(script, character_name, iteration):
    """
    Save a specific iteration of the script during the feedback process
    
    Args:
        script (dict): The podcast script to save
        character_name (str): Name of the historical figure
        iteration (int): The iteration number
    """
    # Create output directory if it doesn't exist
    os.makedirs("output/iterations", exist_ok=True)
    
    # Create filename with character name and iteration number
    output_file = f"output/iterations/{character_name.replace(' ', '_')}/podcast_script_iteration_{iteration}.json"
    
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
    """
    # Get character name from the script
    character_name = script.get("historical_figure", "Unknown")
    
    # Create default output filename with character name if not provided
    if output_file is None:
        output_file = f"output/podcast_script_{character_name.replace(' ', '_')}.json"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the script to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(script, f, indent=2, ensure_ascii=False)
    
    print(f"Script for {character_name} saved to {output_file}")
