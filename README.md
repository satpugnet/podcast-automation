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

### **Narrator**
- **Calm Authority**: Establishes credibility and clarity
- **Warm & Welcoming**: Encourages listeners to feel comfortable
- **Concise Storytelling**: Quickly and clearly sets historical context
- **Neutral Observer**: Provides context without bias
- **Polished Eloquence**: Smooth and engaging voice delivery
- **Reliable Presence**: Consistent tone and familiarity episode to episode
- **Intellectual Accessibility**: Simplifies complex topics elegantly
- **Subtle Charm**: Gentle humor and warmth, enhancing listenability

---

## 📜 **Prompts & Content Generation**

The core of this project relies on carefully crafted prompts to ensure historical accuracy and engaging storytelling. 

You can find the system prompts used for generation in the `src/prompts/` directory:
- **`script_generation.hbr`**: The master prompt for creating the full episode script.
- **`historical_background_research.hbr`**: Instructions for gathering deep historical context.
- **`feedback.hbr`**: The persona for the AI editor that reviews and improves scripts.

---

## 📈 **Future Improvements & Listener Engagement**

- Special "Debates Across Time" episodes (Einstein vs. Newton, etc.)
- Listener-driven polls and Q&A segments
- Hybrid voice acting for more emotional depth
- Companion newsletter: *Time Traveler's Journal* for deeper insights and community-building
- Every new episode, post on LinkedIn and Twitter with an announcement and a summary of the historical figure to build a habit for the audience about learning about historical figures
- Tune in every Tuesday for new episodes featuring fascinating historical figures from across time
