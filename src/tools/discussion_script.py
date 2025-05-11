import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import pyperclip


def generate_podcast_script(historical_figure, background_research=None, script_path=None):
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
    system_prompt = """
    Create a richly detailed, engaging, and immersive podcast script (~40 minutes/6000-6500 words) for the podcast "Echoes Through Time" featuring Leo, a young, curious, empathetic, and thoughtful Time Traveler with an innocent and somewhat naive perspective, engaging in a dynamic, conversational interaction with a notable historical figure. The dialogue should flow naturally, with seamless transitions from lighter, intriguing topics into deeper, introspective discussions. Ensure historical accuracy blended creatively with speculative insights, providing a vivid portrayal of the historical figure's life, personality, motivations, struggles, achievements, and broader impact on history.

    This is a pedagogical educational podcast designed for a general audience. The content should be accessible, engaging, and informative for listeners of various backgrounds and knowledge levels. The goal is to make the audience learn about the historical figure and their life in a compelling way.

    Detailed Structure:

    1. Intro (1-2 mins):
       - Begin with an intriguing narrative hook or fascinating anecdote that captures listeners' curiosity immediately.
       - Briefly introduce the historical figure, emphasizing why their story resonates today.
       - Clearly establish the time period and location for the listener's orientation.

    2. Arrival Scene (2-3 mins):
       - Set a vivid, immersive scene rich in sensory detail (visuals, sounds, atmosphere) that transports listeners directly into the historical context.
       - Depict Leo's gentle and believable arrival into the setting, smoothly transitioning into the first interaction without abruptness.
       - Explicitly mention the specific location, date, and relevant historical context to ground the audience.

    3. Conversation (32-35 mins):
       - Open the dialogue casually, establishing rapport gently and naturally before gradually deepening the discussion.
       - Avoid overly sharp or direct initial questions. Start with friendly or intriguing points of mutual interest, setting a comfortable conversational tone.
       - Gradually progress into key life events, personal anecdotes, emotional challenges, notable achievements, and formative experiences of the historical figure.
       - Encourage genuine, spontaneous exchanges and organic emotional depth, allowing for introspection, humor, and meaningful reflection.
       - Integrate historical context naturally within dialogue, enhancing listener understanding without interrupting conversational flow.
       - Have characters occasionally reference the specific time period, location, or historical events to help orient the audience throughout the conversation.
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
          * Allow frequent opportunities for the historical figure to give extended, detailed responses, especially when sharing personal stories, explaining complex ideas, or discussing significant events.
          * Give the historical figure space for more extended monologues (of a few minutes) to deeply reflect or passionately explain important topics.
          * Ensure Leo's questions range from short, spontaneous reactions to more thoughtful inquiries.
          * Maintain a conversational rhythm that ebbs and flows naturally. It should not be just back to back questions and answers.
       - IMPORTANT: Model the conversation after professional interview podcasts where the host (Leo) guides the guest (historical figure) into sharing expansively about themselves and their world. Leo should:
          * Ask open-ended questions that invite detailed responses
          * Follow up on interesting points to draw out more information
          * Provide gentle prompts that encourage the historical figure to elaborate
          * Create a safe space for the historical figure to share personal insights and reflections
          * Use active listening techniques to show engagement and encourage deeper sharing
          * Occasionally summarize or reflect on what's been shared before moving to a new topic
       - IMPORTANT: Explicitly ensure that most of the historical figure's responses are expansive, detailed, and richly informative. Avoid consistently short or superficial answers; instead, actively encourage the historical figure to delve deeply into their thoughts, motivations, and experiences.
       - Occasionally include words or expressions in the historical figure's original language where it makes sense for realism and immersion, followed by subtle translations or contextual clues for understanding.

    4. Outro (1-2 mins):
       - Concisely summarize key insights from the conversation.
       - Share an inspiring or thought-provoking takeaway.

    Tone: Warm, conversational, intellectually engaging, empathetic, subtly humorous, reflective, approachable, and authentic.

    Characterization:
    - Leo (Time Traveler): Young, innocent, and somewhat naive, with a deep curiosity and wide-eyed wonder about history. His youth and innocence should come through in his questions and reactions, sometimes showing endearing naivety about historical complexities. He's an empathetic listener, intellectually humble, warmly humorous, adaptable conversationalist, and reflective. Leo should be genuinely funny in an unintentional way, with his high energy, innocent misunderstandings, and enthusiastic curiosity leading to humorous moments. His occasional anachronistic references to modern concepts create natural comedy without overplaying his naivety. Leo should maintain appropriate maturity for the historical context while still embodying youthful curiosity. Don't make him too woke, too cringe, too childish or too goofy.
    - Narrator: An old, wise, warm and friendly grandpa figure with a calm authority and welcoming presence. His humor should be tailored to complement the historical figure being interviewed, with gentle wit and occasional playful references that would resonate with both the historical period and modern listeners. His eloquence is concise yet polished, intellectually accessible, and delivered with grandfatherly charm that makes complex historical contexts feel like familiar stories told around a fireplace.
    - Historical Figure: Should speak authentically to their character and time period, with all their complexities, flaws, and contradictions intact. Do NOT present an idealized version of the historical figure. Instead, portray them as closely as possible to their actual personality, including their biases, shortcomings, and controversial aspects. Their responses should be substantive and detailed, offering rich insights into their life, work, and era, while remaining true to their known character traits, beliefs, and attitudes. They should express views consistent with their time period and personal philosophy, even when these might be uncomfortable or controversial by modern standards. Their responses should be thorough and thoughtful, demonstrating their perspective without sanitizing or modernizing their worldview.

    Sound Effects (SFX):
    - Use sound effects and music strategically to enhance immersion without overwhelming the dialogue.
    - Each sound effect or music description must be completely self-contained and highly detailed, as it will be used as the sole input for an AI sound generation system.
    - Sound effect descriptions should paint a complete audio picture in 10-15 words, including specific sounds, their qualities, volume levels, progression, and any emotional tone.
    - For example, instead of "forest sounds," write "dense forest with rustling leaves starting softly then growing louder, distant bird calls fading in and out, and gentle wind through branches."
    - Instead of "battle sounds," write "clashing metal swords beginning quietly then intensifying, men shouting growing from whispers to screams, horses galloping on muddy ground approaching then passing by."
    - Music can also be included as SFX, such as "melancholic violin melody with soft piano accompaniment starting gently and swelling to moderate volume" or "triumphant brass fanfare with military drums beginning boldly then gradually fading."
    - Use sound effects primarily for:
       * Major scene transitions
       * Establishing new environments
       * Highlighting emotionally significant moments
       * Underscoring particularly important historical contexts
       * Setting mood through appropriate period music
       * etc...
    - Avoid generic or vague descriptions that would be difficult to generate accurately.
    - Always include an indication of the sound's duration (in seconds) and volume progression (starting soft/loud and how it changes) to guide the AI sound generation system.

    Note: You can include <break time="x.xs" /> tags in the text to specify pauses in character speech (e.g., "I never expected that. <break time="1.5s" /> How fascinating.").

    IMPORTANT: Avoid parenthetical stage directions or emotional cues in dialogue. Instead, convey emotion and tone naturally through word choice and phrasing, as the audio format doesn't support these annotations.

    Deliver a story that grips listeners in the first 30 seconds and sustains their curiosity to the end.
    Balance vivid scene-setting with rigorous historical accuracy; clarify any debated points in-dialogue.

    IMPORTANT: Format your response strictly as a JSON object with the following structure, ONLY THE JSON, NO markdown or syntax highlighting:
    {
        "title": "Episode title", // Make it SEO friendly and follow the format "<Name of historical figure> - <one line hook / payoff>"
        "description": "Brief podcast episode description for publication",
        "historical_figure": "Name of the historical figure",
        "time_period": "Time period of the conversation",
        "location": "Location of the conversation",
        "intro": [ // Usually only the Narrator/SFX speaks in the intro
            {"speaker": "Narrator", "text": "..."}, 
            {"speaker": "SFX", "text": "...", "duration": x}
        ],
        "arrival_scene": [ // Usually only the Narrator/SFX speaks in the arrival scene
            {"speaker": "Narrator", "text": "..."}, 
            {"speaker": "SFX", "text": "...", "duration": x},
        ],
        "conversation": [
            {"speaker": "Leo", "text": "..."}, 
            {"speaker": "Historical Figure", "text": "..."}, // "Historical Figure" should be replaced by the name of the historical figure
            {"speaker": "Narrator", "text": "..."}, 
            {"speaker": "SFX", "text": "...", "duration": x}
        ],
        "outro": [
            {"speaker": "Leo", "text": "..."}, 
            {"speaker": "Narrator", "text": "..."}, 
            {"speaker": "SFX", "text": "...", "duration": x}
        ]
    }
    """

    # Construct the user prompt
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
            script_path=existing_script_path
        )
        print(f"Generated script saved to: {script_path}")
    else:
        print("Usage: python discussion_script.py <historical_figure> [background_research_path] [existing_script_path]")
