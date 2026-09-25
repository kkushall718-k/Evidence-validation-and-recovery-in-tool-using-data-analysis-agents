"""Save a dedicated personal OpenAI key locally without displaying it."""

from getpass import getpass
from pathlib import Path
import os


def main():
    path = Path(__file__).resolve().parent / ".secrets" / "openai_api_key"
    key = getpass("Personal OpenAI API key (hidden): ").strip()
    if not key or any(c.isspace() for c in key):
        raise SystemExit("No valid key entered. Nothing was saved.")
    path.parent.mkdir(mode=0o700, exist_ok=True)
    os.chmod(path.parent, 0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as stream:
        stream.write(key)
    os.chmod(path, 0o600)
    print(
        "Personal key saved locally. Its value will not be printed or included in the submission."
    )


if __name__ == "__main__":
    main()
