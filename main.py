import json
import asyncio
import os
import sys
import argparse
from generator import CourseGenerator, clear_cache, AUDIO_CACHE_DIR


async def main():
    parser = argparse.ArgumentParser(
        description="Generate an audio course from a JSON file."
    )
    parser.add_argument("--file", required=True, help="Path to the JSON input file.")
    parser.add_argument(
        "--native", default="pt_br", help="Native language (default: pt_br)."
    )
    parser.add_argument(
        "--target", default="en_us", help="Target language (default: en_us)."
    )

    args = parser.parse_args()

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
