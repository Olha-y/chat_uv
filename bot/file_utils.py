import asyncio
from functools import wraps
from io import BytesIO
from PIL import Image
from constants import (
    MAX_WIDTH,
    MAX_HEIGHT,
    MAX_SIZE_BYTES,
    DEFAULT_QUALITY,
    MIN_QUALITY,
    QUALITY_STEP,
)


def run_in_thread(func):
    """Decorator for running a synchronous function in a background thread."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper


def resize_image(
    image: Image.Image,
    max_width: int = MAX_WIDTH,
    max_height: int = MAX_HEIGHT,
) -> Image.Image:
    """
    Returns a copy of the image scaled to fit within (max_width, max_height),
    preserving the aspect ratio. Does not mutate the original (uses image.copy()).
    """
    img_copy = image.copy()
    img_copy.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    return img_copy


def compress_image(
    image: Image.Image,
    max_size_bytes: int = MAX_SIZE_BYTES,
    initial_quality: int = DEFAULT_QUALITY,
    min_quality: int = MIN_QUALITY,
    step: int = QUALITY_STEP,
) -> BytesIO:
    """
    Compresses the passed PIL.Image to JPEG in BytesIO, trying to fit into max_size_bytes.
    Returns BytesIO (position at start, property .name = "image.jpg").
    """
    buffer = BytesIO()
    quality = initial_quality

    # JPEG does not support alpha - convert to RGB (safer, does not break the save)
    img_rgb = image.convert("RGB")

    while True:
        buffer.seek(0)
        buffer.truncate(0)
        img_rgb.save(
            buffer,
            format="JPEG",
            quality=quality,
            optimize=True,
            progressive=True,
        )

        current_size = buffer.tell()  # size in bites
        if current_size <= max_size_bytes or quality <= min_quality:
            break

        quality -= step

    buffer.seek(0)
    buffer.name = "image.jpg"  # required for some APIs that read the filename
    return buffer


@run_in_thread
def process_image(
    path: str,
    max_size_bytes: int = MAX_SIZE_BYTES,
    max_width: int = MAX_WIDTH,
    max_height: int = MAX_HEIGHT,
    initial_quality: int = DEFAULT_QUALITY,
    min_quality: int = MIN_QUALITY,
    step: int = QUALITY_STEP,
) -> BytesIO:
    """
    Full pipeline: opens image from path, resizes and returns compressed JPEG BytesIO.
    Parameters have defaults, given in constants.
    """
    with Image.open(path) as img:
        resized = resize_image(img, max_width=max_width, max_height=max_height)
        compressed = compress_image(
            resized,
            max_size_bytes=max_size_bytes,
            initial_quality=initial_quality,
            min_quality=min_quality,
            step=step,
        )
        return compressed
