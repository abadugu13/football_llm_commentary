import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F

import IPython
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

# This will download all the models used by Tortoise from the HuggingFace hub.
tts = TextToSpeech()
voice_samples, conditioning_latents = load_voices("tom")
def generate_audio(text, preset="fast", voice_samples=None, conditioning_latents=None):
    gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset=preset)
    torchaudio.save('generated.wav', gen.squeeze(0).cpu(), 24000)
    return load_audio('generated.wav', 24000)

