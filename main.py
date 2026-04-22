import json
import asyncio
import os
import sys
from generator import CourseGenerator, clear_cache, AUDIO_CACHE_DIR

NATIVE_LANG = "pt_br"
TARGET_LANG = "en_us"


async def main():
    if len(sys.argv) < 2:
        print("Error: You need to specify a JSON input file.")
        print("Usage: python main.py <filename.json>")
        sys.exit(1)

    json_filepath = sys.argv[1]

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
            curso_data, NATIVE_LANG, TARGET_LANG, output_filename
        )
        await generator.build_lesson()
    finally:
        clear_cache()


if __name__ == "__main__":
    asyncio.run(main())
