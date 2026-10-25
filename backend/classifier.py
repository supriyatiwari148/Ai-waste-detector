"""Zero-shot waste recognition with CLIP (openai/clip-vit-base-patch32).

CLIP compares the photo with a text description of every item in the catalog
(disposal_guidance.py) and tells us which description fits best. No waste-specific
training is needed, but it can still be wrong - especially on unusual photos.
"""
import io
import logging
import os
import threading

from PIL import Image, ImageOps, UnidentifiedImageError

import disposal_guidance as dg

log = logging.getLogger(__name__)

MODEL_ID = os.getenv("CLIP_MODEL_ID", "openai/clip-vit-base-patch32")
# With ~30 possible items, confidences are lower than with 6 classes, so the defaults differ.
MIN_CONFIDENCE = float(os.getenv("CLIP_MIN_CONFIDENCE", "0.30"))
MIN_MARGIN = float(os.getenv("CLIP_MIN_MARGIN", "0.08"))

Image.MAX_IMAGE_PIXELS = 25_000_000

_model = None
_processor = None
_lock = threading.Lock()
KEYS, PROMPTS = dg.labels()


class InvalidImageError(Exception):
    """The upload is not a usable image."""


class ModelUnavailableError(Exception):
    """The model could not be loaded."""


def load_model():
    global _model, _processor
    if _model is not None:
        return
    with _lock:
        if _model is not None:
            return
        try:
            from transformers import CLIPModel, CLIPProcessor

            log.info("Loading model %s ...", MODEL_ID)
            _processor = CLIPProcessor.from_pretrained(MODEL_ID)
            model = CLIPModel.from_pretrained(MODEL_ID)
            model.eval()
            _model = model
        except Exception as exc:  # noqa: BLE001
            log.exception("Model loading failed")
            raise ModelUnavailableError(str(exc)) from exc


def is_loaded():
    return _model is not None


def _open_image(data: bytes) -> Image.Image:
    try:
        Image.open(io.BytesIO(data)).verify()
        img = Image.open(io.BytesIO(data))
        if img.format not in ("JPEG", "PNG"):
            raise InvalidImageError("Only JPG and PNG images are supported.")
        return ImageOps.exif_transpose(img).convert("RGB")
    except InvalidImageError:
        raise
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, SyntaxError) as exc:
        raise InvalidImageError("This file is not a valid image.") from exc


def classify(data: bytes) -> dict:
    image = _open_image(data)
    load_model()

    import torch

    inputs = _processor(text=PROMPTS, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = _model(**inputs).logits_per_image[0]  # one score per catalog item
    probs = torch.softmax(logits, dim=-1)

    top_p, top_i = torch.topk(probs, 3)
    top = [{"label": dg.name_of(KEYS[int(i)]), "confidence": round(float(p), 4)}
           for p, i in zip(top_p, top_i)]
    best_key = KEYS[int(top_i[0])]
    best_conf = float(top_p[0])
    margin = best_conf - float(top_p[1])

    uncertain, reason = False, None
    if best_conf < MIN_CONFIDENCE:
        uncertain, reason = True, "Low confidence."
    elif margin < MIN_MARGIN:
        uncertain, reason = True, "The top two guesses are too close to call."
    elif best_key == "not_waste":
        uncertain, reason = True, "This does not look like a waste item."

    return {"label": best_key, "confidence": round(best_conf, 4), "top_predictions": top,
            "uncertain": uncertain, "uncertain_reason": reason}
