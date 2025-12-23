# 🕰️ **Echoes Through Time Podcast**

A fully automated podcast where an inquisitive Time Traveler named Leo meets humanity's most fascinating historical figures, blending authentic dialogue, compelling storytelling, and listener-driven exploration. Short, insightful episodes designed to bring history vividly to life. New episodes every Tuesday!

---

## ⚙️ **Automation Tech Stack**

- **Content Generation**: OpenAI GPT-4 powered scripting for authentic conversations
- **Audio Production**: ElevenLabs AI voices for text-to-speech and sound effects
- **Transcription**: ElevenLabs Scribe for accurate transcription with speaker diarization
- **Podcast Hosting & Distribution**: Transistor.fm (fully automatable)

---

## 🚀 **Getting Started (Technical)**

1. **Clone Repo**: `git clone [repo link]`
2. **Create Virtual Environment**: 
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**: `pip install -r requirements.txt`
4. **Configure APIs**: 
   - Copy `.env.example` to `.env`
   - Fill in your API keys:
     - `OPENAI_API_KEY` - Your OpenAI API key
     - `OPENAI_MODEL` - Model to use (e.g., `gpt-4`, `gpt-4-turbo`, `gpt-4o`)
     - `ELEVEN_LABS_API_KEY` - Your ElevenLabs API key
     - `NARRATOR_VOICE_ID` - ElevenLabs voice ID for the narrator
     - `LEO_VOICE_ID` - ElevenLabs voice ID for Leo (the time traveler)
     - `TRANSISTOR_FM_API_KEY` - Your Transistor.fm API key (for publishing)
     - `TRANSISTOR_FM_SHOW_ID` - Your Transistor.fm show ID
5. **Run the Generator**: `python src/main.py`
6. **Optional Arguments**:
   ```bash
   python src/main.py --character-name "Napoleon Bonaparte"
   python src/main.py --character-name "Marie Curie" --background-research-path "research.txt"
   ```

---

## 🎙️ **Podcast Structure**

**Format (~20 mins episodes, released every Tuesday):**
- **Intro (1 min)**: Quick hook, guest intro
- **Arrival Scene (1-2 mins)**: Immersive audio to set historical context
- **Conversation (15-18 mins)**: Engaging dialogue with historical figure
- **Reflection & Outro (1 min)**: Key insights, listener engagement, next-episode teaser

---

## 🌟 **Main Character Traits**

### **Time Traveler Leo**
- **Deep Curiosity**: Always seeking depth beyond surface-level facts
- **Intellectual Humility**: Listens actively, encourages genuine conversations
- **Warm Empathy**: Humanizes interactions, deeply connects with guests
- **Sharp Wit & Humor**: Keeps episodes engaging and approachable
- **Adaptable**: Easily adjusts to diverse personalities and historical contexts
- **Authentic Enthusiasm**: Drives listener engagement and retention
- **Well-Researched**: Credibly informs dialogue without overshadowing guests
- **Calm Confidence**: Anchors each conversation comfortably
- **Neutral Yet Engaged**: Encourages nuanced historical discussions
- **Reflective & Insightful**: Concisely wraps episodes with impactful insights

### **Narrator Traits**
- **Calm Authority**: Establishes credibility and clarity
- **Warm & Welcoming**: Encourages listeners to feel comfortable
- **Concise Storytelling**: Quickly and clearly sets historical context
- **Neutral Observer**: Provides context without bias
- **Polished Eloquence**: Smooth and engaging voice delivery
- **Reliable Presence**: Consistent tone and familiarity episode to episode
- **Intellectual Accessibility**: Simplifies complex topics elegantly
- **Subtle Charm**: Gentle humor and warmth, enhancing listenability

---

## 🎤 **Voice Design**

### **Leo Voice Design Prompt**
Design a voice profile for Leo, a young, enthusiastic, and adventurous time traveler with a British accent, hosting lively conversations with historical figures. Leo's voice should embody youthful excitement, boundless energy, gentle innocence, and authentic curiosity—like a spirited explorer thrilled by each new discovery. His tone is clear, friendly, and full of genuine wonder, blending playful naivety with intellectual humility and subtle humor. His British accent should be modern, educated, and approachable—not overly posh or stuffy. Listeners should feel inspired by Leo's infectious enthusiasm, making every historical adventure feel vibrant and fun.

Voice Qualities:
- High-energy & Excited
- Youthful & Playful
- Gently Naive & Innocent
- Friendly & Approachable
- Clear & Energetic
- Authentically Curious
- Warmly Humorous
- Adventurous Spirit
- Modern British Accent

---

## 📜 **Content Generation Prompts**

### **Prompt for In-Depth Research and Concise Summary of Historical Figure**

Conduct extensive and detailed research on the historical figure provided and its era for an history Podcast. Gather information from reliable historical resources, biographies, academic publications, and reputable articles. Focus your research on uncovering fascinating, lesser-known details, key life events, significant achievements, controversies, personal anecdotes, modern relevance, pivotal struggles, character traits, and the broader historical impact of this person. Try to have a particular focus on specific data that an LLM might not know directly rather than well known facts, when possible provide quantitative information and dates.

After thorough research, generate a comprehensive summary of the most compelling and podcast-friendly facts about the historical figure. Consider including elements such as:
- Brief biography and life timeline
- Personality traits
- Distinctive speech patterns
- Fascinating personal anecdotes and quirks
- Significant achievements, innovations, and contributions
- Major challenges and struggles they faced
- Lesser-known or surprising facts about their life
- Historical context and broader impact of their work
- Cultural environment and societal norms of their era
- Relevance and influence on the modern world
- Ethical dilemmas and moral considerations of their time
- Relationships with contemporaries and influential figures
- Legacy and how their reputation has evolved over time
- Quotes and memorable sayings attributed to them
- Common misconceptions about their life or work
- Physical and social environments that shaped their worldview

This guideline is flexible - focus on the most engaging aspects of this particular historical figure rather than rigidly following a specific structure.

Ensure all information is sufficiently detailed to provide meaningful and engaging podcast content. The output should directly enable another LLM to integrate these fascinating insights into a dynamic and immersive podcast conversation between Leo and the historical figure.

Historical Figure:
[Insert Historical Figure Name Here]

### **Prompt for LLM Episode Script Generation**
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
- Leo (Time Traveler): Young, innocent, and somewhat naive, with a deep curiosity and wide-eyed wonder about history. His youth and innocence should come through in his questions and reactions, sometimes showing endearing naivety about historical complexities. He's an empathetic listener, intellectually humble, warmly humorous, adaptable conversationalist, and reflective. Leo should be genuinely funny in an unintentional way, with his high energy, innocent misunderstandings, and enthusiastic curiosity often leading to humorous moments. His earnestness and occasional out-of-place modern references should create natural comedy that lightens the conversation. As a time traveler from the modern era, Leo should occasionally make anachronistic references or comparisons (like mentioning smartphones, social media, modern pop culture, etc.) that would be completely unknown to the historical figure, creating humorous moments of confusion or opportunities for Leo to explain modern concepts.
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

---

## 📈 **Future Improvements & Listener Engagement**

- Special "Debates Across Time" episodes (Einstein vs. Newton, etc.)
- Listener-driven polls and Q&A segments
- Hybrid voice acting for more emotional depth
- Companion newsletter: *Time Traveler's Journal* for deeper insights and community-building
- Every new episode, post on LinkedIn and Twitter with an announcement and a summary of the historical figure to build a habit for the audience about learning about historical figures
- Tune in every Tuesday for new episodes featuring fascinating historical figures from across time
