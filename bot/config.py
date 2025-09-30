import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(os.getenv("MEDIA_DIR", BASE_DIR.parent))


PHOTOS_DIR = ROOT_DIR / "images"
DOCS_DIR = ROOT_DIR / "files"


def resolve_path(path: str) -> str:
    """
    Converts the path from the product to an absolute one.
    Avoids duplications like images/images/foto.jpg.
    """
    p = Path(path)

    if p.is_absolute():
        return str(p)


    if "images" in p.parts:
        return str(ROOT_DIR / p)
    if "files" in p.parts:
        return str(ROOT_DIR / p)

    if p.suffix.lower() in ".jpg":
        return str(PHOTOS_DIR / p)
    if p.suffix.lower() == ".pdf":
        return str(DOCS_DIR / p)

    return str(ROOT_DIR / p)
