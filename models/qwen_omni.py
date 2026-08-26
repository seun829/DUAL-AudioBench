"""
Qwen2.5-Omni-7B wrapper (local inference via transformers).
Sends one audio file + one text question, returns the model's text answer.

Requires: pip install transformers accelerate qwen-omni-utils soundfile torch
Hardware: ~16GB+ VRAM for the 7B in bf16. Use the 3B if the GX10 is busy.

NOTE: Qwen2.5-Omni landed in transformers in 2025 — if the class import fails,
pip install -U transformers, or check the model card on HuggingFace for the
current class names.
"""

import torch
from transformers import Qwen2_5OmniForConditionalGeneration, Qwen2_5OmniProcessor
from qwen_omni_utils import process_mm_info

MODEL_ID = "Qwen/Qwen2.5-Omni-7B"

# lazy globals so the model loads once, not per question
_model = None
_processor = None


def _load():
    """Load the processor/model once and disable speech generation."""

    global _model, _processor
    if _model is None:
        _model = Qwen2_5OmniForConditionalGeneration.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        _model.disable_talker()  # text answers only; saves ~2GB VRAM
        _processor = Qwen2_5OmniProcessor.from_pretrained(MODEL_ID)


def ask(audio_path: str, question: str) -> str:
    """Send one accumulated replay WAV and instruction to local Qwen."""
    _load()

    conversation = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant. Answer concisely based on the audio."}],
        },
        {
            "role": "user",
            "content": [
                {"type": "audio", "audio": audio_path},
                {"type": "text", "text": question},
            ],
        },
    ]

    text = _processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
    audios, images, videos = process_mm_info(conversation, use_audio_in_video=False)
    inputs = _processor(
        text=text, audio=audios, images=images, videos=videos,
        return_tensors="pt", padding=True,
    ).to(_model.device)

    with torch.no_grad():
        out_ids = _model.generate(**inputs, max_new_tokens=256, return_audio=False)

    answer = _processor.batch_decode(
        out_ids[:, inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )[0]
    return answer.strip()


def ask_text(prompt: str) -> str:
    """Transcript-control entry point used by ReplayModelAgent."""
    _load()
    conversation = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are a concise customer-service agent.",
                }
            ],
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        },
    ]
    text = _processor.apply_chat_template(
        conversation, add_generation_prompt=True, tokenize=False
    )
    inputs = _processor(
        text=text,
        return_tensors="pt",
        padding=True,
    ).to(_model.device)
    with torch.no_grad():
        out_ids = _model.generate(**inputs, max_new_tokens=256, return_audio=False)
    answer = _processor.batch_decode(
        out_ids[:, inputs["input_ids"].shape[1] :],
        skip_special_tokens=True,
    )[0]
    return answer.strip()


if __name__ == "__main__":
    # smoke test: python models/qwen_omni.py sample.wav "What color was the router?"
    import sys
    print(ask(sys.argv[1], sys.argv[2]))
