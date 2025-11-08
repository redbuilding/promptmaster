import os
from datetime import datetime
from config import OUTPUT_DIR

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_prompt_to_markdown(text: str):
    """Save provided Markdown content as-is to a timestamped file."""
    ensure_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"enhanced_prompt_{timestamp}.md")

    try:
        with open(filename, "w", encoding="utf-8") as f:
            # Write the content as-is; caller is responsible for headers.
            f.write(text)
        print(f"\n✅ Saved prompt to: {filename}\n")
    except Exception as e:
        print(f"[ERROR] Could not save file: {e}")
