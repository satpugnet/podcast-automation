import os
import json
from openai import OpenAI
from dotenv import load_dotenv

def generate_podcast_script(historical_figure, additional_knowledge=None, script_path=None):
    """
    Generate a podcast script for the Time Traveler Podcast by sending a request to ChatGPT.
    
    Args:
        historical_figure (str): The name of the historical figure to interview
        additional_knowledge (str, optional): Additional knowledge about the historical figure
        script_path (str, optional): Path to an existing script file to use instead of generating a new one
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
    Create a richly detailed, engaging, and immersive podcast script (~20 minutes) for the podcast "Echoes Through Time" featuring Leo, a young, curious, empathetic, and thoughtful Time Traveler with an innocent and somewhat naive perspective, engaging in a dynamic, conversational interaction with a notable historical figure. The dialogue should flow naturally, with seamless transitions from lighter, intriguing topics into deeper, introspective discussions. Ensure historical accuracy blended creatively with speculative insights, providing a vivid portrayal of the historical figure's life, personality, motivations, struggles, achievements, and broader impact on history.

    Detailed Structure:

    1. Intro (1 min):
       - Begin with an intriguing narrative hook or fascinating anecdote that captures listeners' curiosity immediately.
       - Briefly introduce the historical figure, emphasizing why their story resonates today.

    2. Arrival Scene (1-2 mins):
       - Set a vivid, immersive scene rich in sensory detail (visuals, sounds, atmosphere) that transports listeners directly into the historical context.
       - Depict Leo's gentle and believable arrival into the setting, smoothly transitioning into the first interaction without abruptness.

    3. Conversation (15-18 mins):
       - Open the dialogue casually, establishing rapport gently and naturally before gradually deepening the discussion.
       - Avoid overly sharp or direct initial questions. Start with friendly or intriguing points of mutual interest, setting a comfortable conversational tone.
       - Gradually progress into key life events, personal anecdotes, emotional challenges, notable achievements, and formative experiences of the historical figure.
       - Encourage genuine, spontaneous exchanges and organic emotional depth, allowing for introspection, humor, and meaningful reflection.
       - Integrate historical context naturally within dialogue, enhancing listener understanding without interrupting conversational flow.
       - Maintain dynamic exchanges, alternating seamlessly between curiosity-driven inquiries from Leo and detailed storytelling by the historical figure.
       - Occasionally, the Narrator may briefly interject to provide context, transitions, or to highlight significant moments. These should be rare and purposeful.
       - The setting can occasionally change as characters move through space or time naturally and meaningfully.
       - Balance high-level discussions with detailed information:
          * Include precise facts, dates, figures, and technical explanations where appropriate.
          * Provide specific examples, incidents, or lesser-known anecdotes illustrating broader points.
          * Explain particular methodologies or innovations pioneered by the historical figure.
          * Clarify complex concepts with concrete examples relatable to modern listeners.
          * Highlight surprising statistics or quantifiable impacts of their work.
       - Prioritize educational content throughout, ensuring listeners gain substantial knowledge of:
          * The figure's significant contributions and innovations.
          * Social, political, and cultural context of their era.
          * Challenges unique to their time.
          * Influence on subsequent historical developments.
          * Common misconceptions that should be clarified.
       - Balance entertainment with educational depth, using engaging storytelling techniques.
       - Ensure listeners consistently learn new and specific information.
       - Include at least 50 exchanges between Leo and the historical figure for depth and comprehensive coverage.
       - Vary exchange lengths naturally:
          * Brief, snappy exchanges for lighter moments or quick clarifications.
          * Allow frequent opportunities for the historical figure to give extended, detailed responses (averaging 150-300 words), especially when sharing personal stories, explaining complex ideas, or discussing significant events.
          * Give the historical figure space for occasional extended monologues (1-3 minutes) to deeply reflect or passionately explain important topics.
          * Ensure Leo's questions range from short, spontaneous reactions to more thoughtful inquiries.
          * Maintain a conversational rhythm that ebbs and flows naturally.
       - IMPORTANT: Explicitly ensure that most of the historical figure's responses are expansive, detailed, and richly informative. Avoid consistently short or superficial answers; instead, actively encourage the historical figure to delve deeply into their thoughts, motivations, and experiences.

    4. Outro (1 min):
       - Concisely summarize key insights from the conversation.
       - Share an inspiring or thought-provoking takeaway.

    Tone: Warm, conversational, intellectually engaging, empathetic, subtly humorous, reflective, approachable, and authentic.

    Characterization:
    - Leo (Time Traveler): Young, innocent, and somewhat naive, with a deep curiosity and wide-eyed wonder about history. His youth and innocence should come through in his questions and reactions, sometimes showing endearing naivety about historical complexities. He's an empathetic listener, intellectually humble, warmly humorous, adaptable conversationalist, and reflective. Leo should be genuinely funny in an unintentional way, with his high energy, innocent misunderstandings, and enthusiastic curiosity often leading to humorous moments. His earnestness and occasional out-of-place modern references should create natural comedy that lightens the conversation.
    - Narrator: An old, wise, warm and friendly grandpa figure with a calm authority and welcoming presence. His humor should be tailored to complement the historical figure being interviewed, with gentle wit and occasional playful references that would resonate with both the historical period and modern listeners. His eloquence is concise yet polished, intellectually accessible, and delivered with grandfatherly charm that makes complex historical contexts feel like familiar stories told around a fireplace.
    - Historical Figure: Should speak authentically to their character and time period, with all their complexities, flaws, and contradictions intact. Do NOT present an idealized version of the historical figure. Instead, portray them as closely as possible to their actual personality, including their biases, shortcomings, and controversial aspects. Their responses should be substantive and detailed, offering rich insights into their life, work, and era, while remaining true to their known character traits, beliefs, and attitudes. They should express views consistent with their time period and personal philosophy, even when these might be uncomfortable or controversial by modern standards. Their responses should be thorough and thoughtful, demonstrating their perspective without sanitizing or modernizing their worldview.

    IMPORTANT: Format your response strictly as a JSON object with the following structure, ONLY THE JSON, NO markdown or syntax highlighting:
    {
        "title": "Episode title", // Just put the name of the historical figure
        "description": "Brief podcast episode description for publication",
        "historical_figure": "Name of the historical figure",
        "time_period": "Time period of the conversation",
        "location": "Location of the conversation",
        "intro": "Full intro text",
        "arrival_scene": "Full arrival scene text",
        "conversation": [
            {"speaker": "Leo", "text": "..."},
            {"speaker": "Historical Figure", "text": "..."},
            {"speaker": "Narrator", "text": "..."}, // Occasional narrator interjections
            ...
        ],
        "outro": "Full outro text"
    }
    """

    # Construct the user prompt
    user_prompt = f"Create a podcast script for the Time Traveler Podcast interviewing {historical_figure}."
    if additional_knowledge:
        user_prompt += f"\n\nHere is additional research and factual information about {historical_figure} and their era that should be used to enrich the script to ensure historical accuracy and educational value:\n\n{additional_knowledge}"
    
    # Initialize messages list for the conversation with the AI
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Make the initial API call
    try:
        print("Generating initial podcast script with GPT-4o...")
        if not script_path:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7
            )
            
            # Extract and parse the response
            script_json = response.choices[0].message.content
        else:
            with open(script_path, 'r', encoding='utf-8') as file:
                script_json = file.read()
        
        # Try to parse the JSON response
        print("Parsing JSON response...")
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
            
            improved_script = json.loads(improved_script_json)
            print("Script improved successfully!")
            
            # Update the script and messages
            script = improved_script
            messages.append({"role": "assistant", "content": improved_script_json})
            
            # Save this iteration
            iteration += 1
            save_script_iteration(script, character_name, iteration)
        
        return script
    
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
    os.makedirs(f"output/{character_name.replace(' ', '_')}/script_iterations", exist_ok=True)
    
    # Create filename with character name and iteration number
    output_file = f"output/{character_name.replace(' ', '_')}/script_iterations/podcast_script_iteration_{iteration}.json"
    
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
        output_file = f"output/{character_name.replace(' ', '_')}/podcast_script.json"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the script to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(script, f, indent=2, ensure_ascii=False)
    
    print(f"Script for {character_name} saved to {output_file}")

    return output_file
