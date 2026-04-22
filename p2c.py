import json
import asyncio
import os
import sys
import argparse
from typing import Dict, Any
from generator import CourseGenerator, clear_cache, AUDIO_CACHE_DIR

def validate_lesson_json(data: Dict[str, Any], native_lang: str, target_lang: str) -> None:
    """Validates AI-generated JSON and raises clear, actionable errors."""
    errors = []

    required_keys = [
        "voices", native_lang, target_lang,
        f"target_words_{native_lang}", f"target_words_{target_lang}",
    ]
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required key: '{key}'")

    if "voices" in data:
        if "narrator" not in data["voices"]:
            errors.append("Inside 'voices', key 'narrator' is missing")

    if native_lang in data and target_lang in data:
        len_native = len(data[native_lang])
        len_target = len(data[target_lang])
        if len_native != len_target:
            errors.append(
                f"Sentence count mismatch: '{native_lang}' has {len_native}, "
                f"'{target_lang}' has {len_target}"
            )

    tw_native_key = f"target_words_{native_lang}"
    tw_target_key = f"target_words_{target_lang}"
    if tw_native_key in data and tw_target_key in data:
        if len(data[tw_native_key]) != len(data[tw_target_key]):
            errors.append(
                f"Target word count mismatch between '{native_lang}' and '{target_lang}'"
            )

    if errors:
        print("\n❌ Errors found in the AI-generated JSON:")
        for err in errors:
            print(f"   • {err}")
        print("\n💡 Tip: Ask the LLM to regenerate using the exact prompt from the README.")
        print("   Or fix the JSON file manually.")
        sys.exit(1)


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
4. Voices: Use the following Microsoft neural voices (Edge TTS) already selected for this lesson. The Narrator always speaks in the native language. "person_1" and "person_2" speak in the target language.

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
        "narrator": "{narrator_voice}",
        "person_1": "{person_1_voice}",
        "person_2": "{person_2_voice}"
    }}
}}"""


async def main():
    parser = argparse.ArgumentParser(
        description="Generate an audio course from a JSON file or create an LLM prompt."
    )
    parser.add_argument("--file", help="Path to the JSON input file.")
    parser.add_argument("--json", help="Full JSON string for the lesson.")
    parser.add_argument(
        "--native", default="pt_br", help="Native language (default: pt_br)."
    )
    parser.add_argument(
        "--target", default="en_us", help="Target language (default: en_us)."
    )
    parser.add_argument("--theme", help="Theme for the prompt generation.")
    parser.add_argument("--level", help="Level for the prompt generation.")

    args = parser.parse_args()

    # Load settings
    base_path = os.path.dirname(__file__)
    settings_path = os.path.join(base_path, "settings.json")
    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    if args.theme and args.level:
        native_voices = settings["voices"].get(args.native, settings["voices"]["pt_br"])
        target_voices = settings["voices"].get(args.target, settings["voices"]["en_us"])

        prompt = PROMPT_TEMPLATE.format(
            level=args.level,
            theme=args.theme,
            native_lang=args.native,
            target_lang=args.target,
            narrator_voice=native_voices["narrator"],
            person_1_voice=target_voices["person_1"],
            person_2_voice=target_voices["person_2"],
        )
        print("\n" + "=" * 60)
        print("COPY AND PASTE THE PROMPT BELOW INTO YOUR FAVORITE AI")
        print("(ChatGPT, Gemini, Claude, etc.) TO GENERATE YOUR LESSON JSON:")
        print("=" * 60 + "\n")
        print(prompt)
        return

    if not args.file and not args.json:
        print("Error: You must provide either --file or --json.")
        parser.print_help()
        sys.exit(1)

    if args.json:
        try:
            curso_data = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"❌ JSON syntax error in --json string (likely a missing comma or quote):")
            print(f"   {e}")
            print("\n💡 Tip: Paste the JSON into https://jsonlint.com to find the issue.")
            sys.exit(1)
        output_filename = "lesson.mp3"
    else:
        json_filepath = args.file
        if not os.path.exists(json_filepath):
            print(f"❌ Error: File '{json_filepath}' not found.")
            sys.exit(1)

        with open(json_filepath, "r", encoding="utf-8") as f:
            try:
                curso_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"❌ JSON syntax error in '{json_filepath}' (likely a missing comma or quote):")
                print(f"   {e}")
                print("\n💡 Tip: Paste the JSON into https://jsonlint.com to find the issue.")
                sys.exit(1)

        base_name = os.path.splitext(os.path.basename(json_filepath))[0]
        output_filename = f"{base_name}.mp3"

    validate_lesson_json(curso_data, args.native, args.target)

    clear_cache()
    os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

    try:
        generator = CourseGenerator(
            curso_data, args.native, args.target, output_filename
        )
        await generator.build_lesson()
    except KeyError as e:
        print(f"❌ JSON structure error: key {e} not found.")
        print("   This usually happens when the LLM didn't follow the exact format.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during generation: {type(e).__name__}: {e}")
        sys.exit(1)
    finally:
        clear_cache()


if __name__ == "__main__":
    asyncio.run(main())
