# 🕰️ **Echoes Through Time Podcast**

A fully automated podcast where an inquisitive Time Traveler named Leo meets humanity's most fascinating historical figures, blending authentic dialogue, compelling storytelling, and listener-driven exploration. Short, insightful episodes designed to bring history vividly to life. New episodes every Tuesday!

---

## ⚙️ **Tech Stack & External Services**

This project integrates with several external APIs to automate the entire podcast production pipeline:

| Service | Purpose | What It Does |
|---------|---------|--------------|
| **OpenAI GPT** | Content Generation | Generates podcast scripts, identifies speakers in transcripts, creates social media posts, and designs voice descriptions for historical figures |
| **ElevenLabs** | Audio Production | Text-to-speech for all dialogue (narrator, Leo, historical figures), AI sound effects generation, and speech-to-text transcription with speaker diarization |
| **Transistor.fm** | Podcast Hosting | Hosts and distributes the podcast to all major platforms (Spotify, Apple Podcasts, etc.), manages episode publishing and scheduling |

---

## 🚀 **Getting Started**

### Prerequisites

- Python 3.10+
- API keys for OpenAI, ElevenLabs, and Transistor.fm
- ffmpeg installed (required by pydub for audio processing)

### Installation

1. **Clone the repository**:
   ```bash
   git clone [repo link]
   cd podcast-automation
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   
   Create a `.env` file in the project root with the following keys:

   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=sk-...                    # Your OpenAI API key
   OPENAI_MODEL=gpt-4o                      # Model to use (gpt-4o, gpt-4-turbo, etc.)

   # ElevenLabs Configuration
   ELEVEN_LABS_API_KEY=...                  # Your ElevenLabs API key
   NARRATOR_VOICE_ID=...                    # ElevenLabs voice ID for the Narrator
   LEO_VOICE_ID=...                         # ElevenLabs voice ID for Leo (time traveler)

   # Transistor.fm Configuration
   TRANSISTOR_FM_API_KEY=...                # Your Transistor.fm API key
   TRANSISTOR_FM_SHOW_ID=...                # Your show's ID on Transistor.fm
   ```

---

## 🎬 **Episode Creation Flow**

The generator follows an 8-step pipeline to create a complete episode. Each step can be skipped if you provide pre-existing files.

### Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EPISODE CREATION PIPELINE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Step 1: Character Selection                                                │
│     └─► Creates output/{Character_Name}/ folder                             │
│                    ▼                                                        │
│  Step 2: Background Research                                                │
│     └─► Uses external research (e.g., ChatGPT Deep Research, Perplexity)    │
│     └─► Saves to background_research.txt                                    │
│                    ▼                                                        │
│  Step 3: Script Generation (OpenAI)                                         │
│     └─► Generates JSON script with intro, arrival, conversation, outro      │
│     └─► Interactive feedback loop for refinements                           │
│     └─► Saves iterations + final script.json                                │
│                    ▼                                                        │
│  Step 4: Voice Generation (ElevenLabs)                                      │
│     └─► Creates unique AI voice for the historical figure                   │
│     └─► Plays 3 previews, user selects preferred voice                      │
│     └─► Saves voice_id.json                                                 │
│                    ▼                                                        │
│  Step 5: Audio Generation (ElevenLabs)                                      │
│     └─► Converts script to speech (narrator, Leo, guest)                    │
│     └─► Generates AI sound effects for atmosphere                           │
│     └─► Combines segments with natural pauses and fades                     │
│     └─► Saves audio.mp3 + segments/sfx folders                              │
│                    ▼                                                        │
│  Step 6: Transcript Generation (ElevenLabs Scribe)                          │
│     └─► Transcribes audio with speaker diarization                          │
│     └─► AI identifies which speaker is who                                  │
│     └─► Saves transcript.vtt (WebVTT format)                                │
│                    ▼                                                        │
│  Step 7: Social Media Posts (OpenAI)                                        │
│     └─► Generates LinkedIn and X (Twitter) announcement posts               │
│     └─► Interactive feedback loop for refinements                           │
│     └─► Saves social_media_posts.json                                       │
│                    ▼                                                        │
│  Step 8: Episode Publication (Transistor.fm)                                │
│     └─► Uploads audio to Transistor.fm                                      │
│     └─► Creates episode with title, description, transcript                 │
│     └─► Options: publish now, save as draft, or schedule                    │
│     └─► Saves publishing_details.json                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ **Running the Generator**

### Interactive Mode (Recommended for First-Time Use)

Simply run the main script and follow the prompts:

```bash
python src/main.py
```

The generator will guide you through each step interactively.

### Command-Line Arguments

You can skip steps by providing pre-existing files via command-line arguments:

```bash
python src/main.py [OPTIONS]
```

| Argument | Description | Example |
|----------|-------------|---------|
| `--character-name` | Name of the historical figure (skips prompt) | `--character-name "Marie Curie"` |
| `--background-research-path` | Path to background research file | `--background-research-path "research.txt"` |
| `--script-path` | Path to existing script JSON (skips generation) | `--script-path "output/Marie_Curie/script.json"` |
| `--guest-voice-id` | ElevenLabs voice ID for the guest (skips voice generation) | `--guest-voice-id "abc123xyz"` |
| `--audio-path` | Path to existing audio file (skips audio generation) | `--audio-path "output/Marie_Curie/audio.mp3"` |
| `--transcript-path` | Path to existing transcript (skips transcription) | `--transcript-path "output/Marie_Curie/transcript.vtt"` |
| `--social-media-path` | Path to existing social media posts (skips generation) | `--social-media-path "output/Marie_Curie/social_media_posts.json"` |

### Examples

**Generate a complete new episode:**
```bash
python src/main.py --character-name "Leonardo da Vinci"
```

**Resume from an existing script (skip research and script generation):**
```bash
python src/main.py \
  --character-name "Leonardo da Vinci" \
  --background-research-path "output/Leonardo_da_Vinci/background_research.txt" \
  --script-path "output/Leonardo_da_Vinci/script.json"
```

**Use an existing voice and regenerate only audio:**
```bash
python src/main.py \
  --character-name "Leonardo da Vinci" \
  --background-research-path "output/Leonardo_da_Vinci/background_research.txt" \
  --script-path "output/Leonardo_da_Vinci/script.json" \
  --guest-voice-id "pNInz6obpgDQGcFmaJgB"
```

---

## 📂 **Output File Structure**

Each episode generates the following files in `output/{Character_Name}/`:

```
output/Leonardo_da_Vinci/
├── background_research.txt      # Historical research used for script
├── script.json                  # Final podcast script (JSON format)
├── script_iterations/           # All script versions during feedback loop
│   ├── script_iteration_1.json
│   ├── script_iteration_2.json
│   └── ...
├── voice_id.json                # ElevenLabs voice ID for the character
├── audio/
│   ├── segments/                # Individual speech audio files
│   │   ├── intro_0_abc123.mp3
│   │   ├── conversation_1_def456.mp3
│   │   └── ...
│   └── sfx/                     # Generated sound effects
│       ├── arrival_scene_sfx_0_xyz789.mp3
│       └── ...
├── audio.mp3                    # Final combined episode audio
├── transcript.vtt               # WebVTT transcript with speaker labels
├── social_media_posts.json      # LinkedIn and X post content
└── publishing_details.json      # Transistor.fm episode ID and publish date
```

---

## 📝 **Step-by-Step Guide**

### Step 1: Character Selection

Enter the name of the historical figure you want to interview. The generator creates a dedicated output folder for all episode files.

### Step 2: Background Research

This is a **semi-manual step**. The generator:
1. Copies a research prompt template to your clipboard
2. Creates an empty `background_research.txt` file

**You should:**
1. Paste the prompt into a research tool (ChatGPT with Deep Research, Perplexity, Claude, etc.)
2. Copy the research results into `background_research.txt`
3. Press Enter to continue

The research template asks for:
- Biography and life timeline
- Personality traits and speech patterns
- Lesser-known facts and anecdotes
- Historical context and cultural environment
- Relationships with contemporaries
- Quotes and memorable sayings

### Step 3: Script Generation

The script is generated using OpenAI with a detailed prompt that creates:
- **Intro** (~1 min): Hook and guest introduction
- **Arrival Scene** (~1-2 min): Immersive scene-setting with sound effects
- **Conversation** (~15-18 min): Dialogue between Leo and the historical figure
- **Outro** (~1 min): Reflection and episode teaser

**Interactive feedback loop:** After generation, you can review and request improvements. Each iteration is saved for reference.

### Step 4: Voice Generation

ElevenLabs generates a unique voice for the historical figure:
1. OpenAI creates a voice description based on historical accounts
2. ElevenLabs generates 3 voice previews
3. You listen to each preview and select your favorite
4. The selected voice is saved to your ElevenLabs account

**Tip:** You can skip this step for returning characters by providing `--guest-voice-id`.

### Step 5: Audio Generation

The script is converted to audio:
- Speech segments use ElevenLabs text-to-speech
- Sound effects (marked as "SFX" in the script) are generated using ElevenLabs sound effects API
- All segments are combined with natural pauses and fade effects
- Caching prevents regenerating unchanged segments

### Step 6: Transcript Generation

ElevenLabs Scribe transcribes the audio:
1. Audio is uploaded for transcription with speaker diarization
2. OpenAI identifies which speaker ID corresponds to which character
3. A WebVTT transcript is generated with proper speaker labels

### Step 7: Social Media Posts

OpenAI generates promotional posts for:
- **LinkedIn:** ~800 characters, professional yet personal
- **X (Twitter):** Max 280 characters, punchy and engaging

**Interactive feedback loop:** Review and refine the posts before saving.

### Step 8: Episode Publication

Upload and publish to Transistor.fm with options:
- **`p` - Publish now:** Episode goes live immediately
- **`d` - Save as draft:** Episode saved but not published
- **`s` - Schedule:** Set a future publication date (defaults to next Tuesday at 1 AM EDT)
- **Any other key - Skip:** Skip publication entirely

---

## 🔧 **Running Individual Tools**

Each tool can be run independently for debugging or partial regeneration:

```bash
# Generate voice for a character
python src/tools/voice_design.py "Napoleon Bonaparte"

# Generate script only
python src/tools/discussion_script.py "Napoleon Bonaparte" "path/to/research.txt"

# Generate audio from existing script
python src/tools/audio.py "output/Napoleon_Bonaparte/script.json" "voice_id_here"

# Generate transcript from audio
python src/tools/transcript.py "output/Napoleon_Bonaparte/script.json" "output/Napoleon_Bonaparte/audio.mp3"

# Generate social media posts
python src/tools/social_media.py "output/Napoleon_Bonaparte/script.json" "output/Napoleon_Bonaparte/background_research.txt"

# Publish an episode
python src/tools/publication.py "script.json" "audio.mp3" "transcript.vtt" None "scheduled" "2025-01-07 01:00:00 EDT"
```

---

## 🎙️ **Podcast Structure**

**Format (~20 min episodes, released every Tuesday):**
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
- **`script_generation.hbr`**: The master prompt for creating the full episode script
- **`historical_background_research.hbr`**: Template for gathering deep historical context
- **`feedback.hbr`**: The persona for the AI editor that reviews and improves scripts

---

## 📈 **Future Improvements & Listener Engagement**

- Special "Debates Across Time" episodes (Einstein vs. Newton, etc.)
- Listener-driven polls and Q&A segments
- Hybrid voice acting for more emotional depth
- Companion newsletter: *Time Traveler's Journal* for deeper insights and community-building
- Every new episode, post on LinkedIn and Twitter with an announcement and a summary of the historical figure to build a habit for the audience about learning about historical figures
- Tune in every Tuesday for new episodes featuring fascinating historical figures from across time
