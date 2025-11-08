import re
from config import MODEL_PROVIDER
from providers.ollama_provider import OllamaProvider
from framework_loader import load_frameworks


def get_provider():
    if MODEL_PROVIDER.lower() == "ollama":
        return OllamaProvider()
    else:
        raise ValueError(f"Unsupported model provider: {MODEL_PROVIDER}")


def clean_duplicate_headings(text: str) -> str:
    # Remove duplicate framework headings (e.g., "**CRAFT**" repeated twice)
    text = re.sub(r"(\*\*[A-Z]+\*\*)\s*\1", r"\1", text)
    # Normalize Markdown heading style
    text = re.sub(r"#+\s*\*\*([A-Z]+)\*\*", r"**\1**", text)
    return text.strip()


def rewrite_prompt(user_prompt: str, frameworks: list):
    """Use provider to rewrite the prompt using framework definitions."""
    provider = get_provider()
    all_frameworks = load_frameworks()

    # Include only the selected frameworks’ definitions
    framework_descriptions = []
    for fw in frameworks:
        info = all_frameworks.get(fw)
        if info:
            framework_descriptions.append(
                f"- **{fw}**: {info['description']} (Example: {info['example']})"
            )
        else:
            framework_descriptions.append(f"- **{fw}**: No definition available.")

    framework_text = "\n\n---\n\n".join(framework_descriptions)

    # Note: We intentionally generate per-framework prompts instead of a single
    # composite prompt to ensure each section is structured and complete.

    try:
        all_outputs = []
        for fw in frameworks:
            fw_info = all_frameworks.get(fw)
            fw_description = (
                f"- **{fw}**: {fw_info['description']} (Example: {fw_info['example']})"
                if fw_info
                else f"- **{fw}**: No definition."
            )
            fw_prompt = (
                f"You are an expert prompt engineer.\n"
                f"Apply the following framework to rewrite the user's prompt.\n\n"
                f"{fw_description}\n\n"
                f"User prompt:\n{user_prompt}\n\n"
                f"Output a clearly labeled **{fw}** section with Markdown bullets."
            )
            try:
                fw_output = provider.generate(fw_prompt)
                if fw_output:
                    all_outputs.append(f"**{fw}**\n{fw_output.strip()}\n")
            except Exception as e:
                print(f"[WARN] Could not generate using {fw}: {e}")

        response = "\n\n".join(all_outputs)
        response = clean_duplicate_headings(response)
        if not response:
            raise ValueError("Empty response from model.")
        return response
    except Exception as e:
        print(f"[ERROR] {e}")
        return None
