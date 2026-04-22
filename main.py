import json
import asyncio
import os
import sys
import argparse
from generator import CourseGenerator, clear_cache, AUDIO_CACHE_DIR

PROMPT_TEMPLATE = """You are a linguist specialized in creating language courses with a focus on audio and spaced repetition (Pimsleur style). 

Your task is to generate a language lesson script in strict JSON format, focused on level {level} and on the theme {theme}.

### COURSE GUIDELINES:
1. Difficulty Level: The vocabulary, grammar, and expressions used in the dialogue must strictly correspond to level {level}.
2. Dialogue Size: The dialogue should be short, natural, and direct, containing between 4 to 8 sentences maximum. It should sound like a real daily conversation.
3. Target Words:
   - Choose 3 to 5 key words or expressions from the dialogue that are the most challenging or important for level {level}.
   - The arrays `target_words_{native_lang}` and `target_words_{target_lang}` must have EXACTLY the same size.
   - The word at index 0 of one array must be the exact translation of the word at index 0 of the other array.
   - Use words in their infinitive or base form unless a specific conjugation is the focus of the lesson.
4. Voices: Define standard Microsoft neural voices (Edge TTS) compatible with the chosen languages. The Narrator always speaks in the native language. "person_1" and "person_2" speak in the target language.

### LANGUAGES:
- Native Language: {native_lang}
- Target Language: {target_lang}

### REQUIRED OUTPUT FORMAT:
You must return ONLY a valid JSON, without any additional text, explanations, or markdown formatting blocks before or after. Use the exact structure below:

{{
    "{native_lang}": [ 
        {{ "person_1": "Translated sentence 1" }}, 
        {{ "person_2": "Translated sentence 2" }}
    ],
    "{target_lang}": [ 
        {{ "person_1": "Original sentence 1" }}, 
        {{ "person_2": "Original sentence 2" }}
    ],
    "target_words_{native_lang}": ["word1", "word2", "word3"],
    "target_words_{target_lang}": ["word1", "word2", "word3"],
    "voices": {{
        "narrator": "Narrator voice in native language",
        "person_1": "Person 1 voice in target language",
        "person_2": "Person 2 voice in target language"
    }}
}}"""


async def main():
    parser = argparse.ArgumentParser(
        description="Generate an audio course from a JSON file or create an LLM prompt."
    )
    parser.add_argument("--file", help="Path to the JSON input file.")
    parser.add_argument(
        "--native", default="pt_br", help="Native language (default: pt_br)."
    )
    parser.add_argument(
        "--target", default="en_us", help="Target language (default: en_us)."
    )
    parser.add_argument("--theme", help="Theme for the prompt generation.")
    parser.add_argument("--level", help="Level for the prompt generation.")

    args = parser.parse_args()

    if args.theme and args.level:
        prompt = PROMPT_TEMPLATE.format(
            level=args.level,
            theme=args.theme,
            native_lang=args.native,
            target_lang=args.target,
        )
        print(prompt)
        return

    if not args.file:
        parser.print_help()
        sys.exit(1)

    json_filepath = args.file

    if not os.path.exists(json_filepath):
        print(f"Error: The file '{json_filepath}' was not found.")
        sys.exit(1)

    with open(json_filepath, "r", encoding="utf-8") as f:
        try:
            curso_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: The file '{json_filepath}' is not a valid JSON.")
            sys.exit(1)

    base_name = os.path.splitext(os.path.basename(json_filepath))[0]
    output_filename = f"{base_name}.mp3"

    clear_cache()
    os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

    try:
        generator = CourseGenerator(
            curso_data, args.native, args.target, output_filename
        )
        await generator.build_lesson()
    finally:
        clear_cache()


if __name__ == "__main__":
    asyncio.run(main())
