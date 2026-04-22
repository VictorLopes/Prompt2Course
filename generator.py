import os
import shutil
import hashlib
import random
import json
import edge_tts
from pydub import AudioSegment

AUDIO_CACHE_DIR = "audio_cache"
TOTAL_REPS_PHRASE = 5
TOTAL_REPS_WORD = 6


def clear_cache():
    if os.path.exists(AUDIO_CACHE_DIR):
        print("Cleaning audio cache...")
        shutil.rmtree(AUDIO_CACHE_DIR)


async def generate_tts(text, voice, prefix="audio"):
    unique_hash = hashlib.md5(f"{voice}_{text}".encode("utf-8")).hexdigest()[:12]
    filename = f"{prefix}_{unique_hash}.mp3"
    filepath = os.path.join(AUDIO_CACHE_DIR, filename)

    if not os.path.exists(filepath):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filepath)
    return AudioSegment.from_file(filepath)


def create_silence(seconds):
    return AudioSegment.silent(duration=int(seconds * 1000))


class CourseGenerator:
    def __init__(self, data, native_lang, target_lang, output_filename):
        self.data = data
        self.native_lang = native_lang
        self.target_lang = target_lang
        self.output_filename = output_filename
        self.lesson_audio = AudioSegment.silent(duration=1000)

        self.phrase_stats = {i: 0 for i in range(len(data[target_lang]))}
        self.word_stats = {
            i: 0 for i in range(len(data[f"target_words_{target_lang}"]))
        }

        self.introduced_phrases = set()
        self.introduced_words = set()
        self.word_voices = {}

        self.translations = self._load_translations()

    def _load_translations(self):
        base_path = os.path.dirname(__file__)
        translations_path = os.path.join(base_path, "translations.json")
        with open(translations_path, "r", encoding="utf-8") as f:
            all_translations = json.load(f)
        return all_translations.get(self.native_lang, all_translations["pt_br"])

    def t(self, key, **kwargs):
        return self.translations.get(key, "").format(**kwargs)

    async def add_narrator(self, text):
        voice = self.data["voices"]["narrator"]
        audio = await generate_tts(text, voice, "nar")
        self.lesson_audio += audio

    async def play_and_repeat(
        self, text, voice, item_type, item_idx, repeats=1, wait_time=2.0
    ):
        audio = await generate_tts(text, voice, "tgt")
        for _ in range(repeats):
            self.lesson_audio += audio
            self.lesson_audio += create_silence(audio.duration_seconds + wait_time)

            if item_type == "phrase":
                self.phrase_stats[item_idx] += 1
            elif item_type == "word":
                self.word_stats[item_idx] += 1

    async def build_lesson(self):
        print(f"Starting creating course: {self.output_filename}")

        await self.add_narrator(self.t("listen_conversation"))
        for i in range(len(self.data[self.target_lang])):
            target_entry = self.data[self.target_lang][i]
            person = list(target_entry.keys())[0]
            text = target_entry[person]
            voice = self.data["voices"][person]
            audio = await generate_tts(text, voice, "intro")
            self.lesson_audio += audio + create_silence(0.5)

        self.lesson_audio += create_silence(2)

        for i in range(len(self.data[self.target_lang])):
            target_entry = self.data[self.target_lang][i]
            native_entry = self.data[self.native_lang][i]

            person = list(target_entry.keys())[0]
            target_text = target_entry[person]
            native_text = native_entry[person]
            voice = self.data["voices"][person]

            self.introduced_phrases.add(i)

            await self.add_narrator(self.t("how_to_say", text=native_text))
            self.lesson_audio += create_silence(2)

            await self.play_and_repeat(target_text, voice, "phrase", i, repeats=2)

            target_words_en = self.data[f"target_words_{self.target_lang}"]
            target_words_pt = self.data[f"target_words_{self.native_lang}"]

            for w_idx, target_word in enumerate(target_words_en):
                if target_word.lower() in target_text.lower():
                    native_word = target_words_pt[w_idx]
                    self.introduced_words.add(w_idx)
                    self.word_voices[w_idx] = voice

                    await self.add_narrator(self.t("how_to_say_word", word=native_word))
                    self.lesson_audio += create_silence(1.5)
                    await self.play_and_repeat(
                        target_word, voice, "word", w_idx, repeats=2
                    )

            if i > 0:
                await self.do_review()

        await self.add_narrator(self.t("let_us_review"))

        while True:
            phrases_done = all(
                self.phrase_stats[idx] >= TOTAL_REPS_PHRASE
                for idx in self.introduced_phrases
            )
            words_done = all(
                self.word_stats[idx] >= TOTAL_REPS_WORD for idx in self.introduced_words
            )

            if phrases_done and words_done:
                break

            if len(self.lesson_audio) > 30 * 60 * 1000:
                break

            await self.do_review()

        await self.add_narrator(self.t("end_lesson"))

        print(f"Exporting final audio to '{self.output_filename}'...")
        self.lesson_audio.export(self.output_filename, format="mp3")
        print("Success!")

    async def do_review(self):
        options = []

        for idx in self.introduced_phrases:
            if self.phrase_stats[idx] < TOTAL_REPS_PHRASE:
                options.append(("phrase", idx))

        for idx in self.introduced_words:
            if self.word_stats[idx] < TOTAL_REPS_WORD:
                options.append(("word", idx))

        if not options:
            return

        item_type, idx = random.choice(options)

        if item_type == "word":
            native_word = self.data[f"target_words_{self.native_lang}"][idx]
            target_word = self.data[f"target_words_{self.target_lang}"][idx]
            voice = self.word_voices[idx]

            await self.add_narrator(self.t("remember_how_to_say_word", word=native_word))
            self.lesson_audio += create_silence(2)
            await self.play_and_repeat(target_word, voice, "word", idx, repeats=1)

        else:
            native_entry = self.data[self.native_lang][idx]
            target_entry = self.data[self.target_lang][idx]
            person = list(native_entry.keys())[0]

            native_text = native_entry[person]
            target_text = target_entry[person]
            voice = self.data["voices"][person]

            await self.add_narrator(self.t("remember_how_to_say", text=native_text))
            self.lesson_audio += create_silence(2.5)
            await self.play_and_repeat(target_text, voice, "phrase", idx, repeats=1)
