# Prompt2Course 🎧

Audio language lesson generator (MP3) inspired by the Pimsleur methodology. Use AI to create custom dialogues and transform them into interactive lessons with spaced repetition. If you would like to use another TTS engine, please refer to [edge-tts](https://github.com/rany2/edge-tts).

Maybe you wish a more professional already created course. In this case, you should consider buying [Pimsleur's courses](https://www.pimsleur.com/).

## 🚀 Getting Started

### 1. Installation

Prepare the virtual environment and dependencies:

```bash
./setup.sh
```

Or manually:

```bash
python -m pip install -r requirements.txt
```

or

```bash
./python3/bin/python -m pip install -r requirements.txt
```

---

## 🛠️ Usage Modes

The `p2c.py` script has two main modes: **Generate Prompt** (to request lesson content from an AI) and **Generate Audio** (to transform the AI's JSON into an MP3).

### 1. Generate the Prompt for the AI

The script generates a structured prompt in English (for better performance with global models like GPT-4 and Gemini) based on your theme and level.

**Command:**
```bash
./python3/bin/python p2c.py --theme "Checking into a hotel" --level A2
```

or

```bash
./python3/bin/python p2c.py --theme "Checking into a hotel" --level A2 --native en_us --target pt_br
```

**Optional Parameters:**
- `--native`: Your native language (default: `pt_br`).
- `--target`: Language you want to learn (default: `en_us`).

**What to do:**
1. Copy the text generated in the terminal.
2. Paste it into your favorite AI chat (ChatGPT, Gemini, Claude, etc).
3. Save the JSON returned by the AI into a file (e.g., `lesson.json`).

### 2. Generate the MP3 Course

Transform the JSON returned by the AI into a narrated lesson. You can either pass a file path or the JSON string directly.

**Using a file:**
```bash
./python3/bin/python p2c.py --file lesson.json
```

**Using a JSON string:**
```bash
./python3/bin/python p2c.py --json '{"pt_br": [...], "en_us": [...], "target_words_pt_br": [...], "target_words_en_us": [...], "voices": {...}}'
```

**Full example with language flags:**
```bash
./python3/bin/python p2c.py --file lesson.json --native en_us --target pt_br
```

**Optional Parameters:**
- `--native`: Must be the same native language used in the JSON (default: `pt_br`).
- `--target`: Must be the same target language used in the JSON (default: `en_us`).

---

## 🌍 Supported Languages

The narrator's instructions during the lesson are translated in the `translations.json` file. Currently, we support:
- 🇧🇷 Brazilian Portuguese (`pt_br`)
- 🇺🇸 American English (`en_us`)

---

## 💡 Theme Suggestions

Below are some ideas for you to use with the `--theme` flag:

### ✈️ Travel (Levels A1/A2)
- "Asking for directions to reach the train station."
- "Going through immigration and explaining the reason for the trip."
- "Asking for the bill and if they accept cards."

### 💼 Business (Levels B1/B2/Business)
- "Rescheduling a last-minute meeting with a client."
- "Introducing yourself on the first day of work."
- "Negotiating project delivery deadlines."

### 🤝 Social (Any level)
- "Inviting a colleague for coffee on Friday."
- "Politely complaining to a neighbor about loud noise."
- "Discussing the plot of a movie they just watched."

---

## ⚙️ How the Methodology Works

The script processes the JSON and creates a dynamic audio lesson:
1. **Listening**: You hear the full conversation between native speakers.
2. **Construction**: The narrator guides you sentence by sentence ("How do you say: ...?").
3. **Vocabulary**: Special focus on target words (`target_words`) identified in the lesson.
4. **Spaced Repetition**: The script alternates between new sentences and constant reviews of previous items for reinforcement.
5. **Duration**: The lesson ends automatically after reaching a satisfactory repetition level.

---

## 📄 JSON Structure Example

If you want to create the file manually, it should follow this format:

```json
{
    "pt_br": [ 
        { "person_1": "Olá, como você está?" }, 
        { "person_2": "Eu estou bem, obrigado!" }
    ],
    "en_us": [ 
        { "person_1": "Hello, how are you?" }, 
        { "person_2": "I am fine, thank you!" }
    ],
    "target_words_pt_br": ["bem", "obrigado"],
    "target_words_en_us": ["fine", "thank you"],
    "voices": {
        "narrator": "pt-BR-AntonioNeural",
        "person_1": "en-US-JennyNeural",
        "person_2": "en-US-GuyNeural"
    }
}
```