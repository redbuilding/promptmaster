"""
prompt_composer.py
------------------
Combines structured framework output into a single coherent unified prompt.
"""

import re


def _extract_rewritten_prompt(enhanced_text: str) -> str:
    """Try to extract a dedicated 'Rewritten Prompt' section if present."""
    lines = enhanced_text.splitlines()
    out: list[str] = []
    capture = False
    for line in lines:
        # Match a header like '**Rewritten Prompt**' or 'Rewritten Prompt'
        if re.match(r"^\s*(?:\*\*)?Rewritten\s+Prompt(?:\*\*)?\s*$", line, re.IGNORECASE):
            capture = True
            continue
        if capture:
            # Stop if we hit another markdown header/section
            if re.match(r"^\s*#|^\s*\*\*\w+\*\*\s*$", line):
                break
            # Prefer blockquote lines '>' but also accept plain lines until header
            if line.strip().startswith(">"):
                out.append(re.sub(r"^\s*>\s?", "", line).rstrip())
            elif line.strip():
                out.append(line.rstrip())
            else:
                # Allow a single blank inside the block; break on double blank
                if out and out[-1] != "":
                    out.append("")
                else:
                    break
    return "\n".join(out).strip()


def _first_line_value(enhanced_text: str, names: list[str]) -> str | None:
    """Find first value after a label on its own line, case-insensitive.
    Accepts bullets and bold labels like '- **Role:** text'.
    """
    label = "|".join(names)
    pattern = rf"^(?:-\s*)?(?:\*\*)?(?:{label})(?:\*\*)?\s*[:\-]\s*(.+)$"
    m = re.search(pattern, enhanced_text, flags=re.IGNORECASE | re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def _strip_markdown(text: str) -> str:
    """Remove simple markdown emphasis and stray formatting markers."""
    if not text:
        return text
    # Remove surrounding code/emphasis markers
    t = text.strip()
    t = re.sub(r"^[`*_\s]+", "", t)
    t = re.sub(r"[`*_\s]+$", "", t)
    # Collapse internal double spaces
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def _clean_action(text: str) -> str:
    """Normalize action line: strip list numbering/bullets and markdown."""
    if not text:
        return text
    t = _strip_markdown(text)
    # Remove leading list markers like '1.' or '-' or '*'
    t = re.sub(r"^(?:\d+\.|[-*])\s+", "", t)
    # Lowercase initial if it reads better after 'Be sure to'
    return t[0].lower() + t[1:] if t and t[0].isupper() else t


def _format_tone(text: str) -> str | None:
    """Format tone into a natural sentence.
    Examples:
    - "Professional yet approachable, with a focus on data-driven insights" ->
      "Use a professional yet approachable tone with a focus on data-driven insights."
    - "tone: professional and concise" -> "Use professional and concise tone."
    - If 'tone' already appears in the text, avoid adding another 'tone'.
    """
    if not text:
        return None
    t = _strip_markdown(text).strip()
    # Strip trailing punctuation
    t = re.sub(r"[\s\.]$", "", t)
    # Remove leading article
    tl = t.lstrip()
    if tl.lower().startswith("a "):
        t = tl[2:].lstrip()
    elif tl.lower().startswith("an "):
        t = tl[3:].lstrip()
    # If already mentions 'tone', don't add another
    if re.search(r"\btone\b", t, re.IGNORECASE):
        return f"Use {t}."
    # Lowercase first letter for smoother phrasing after 'a'
    if t and t[0].isupper():
        t = t[0].lower() + t[1:]
    # If phrase contains ", with" or " with", keep it; else just append 'tone.'
    if re.search(r"\bwith\b", t):
        # Ensure it reads as '... tone with ...'
        parts = re.split(r"\bwith\b", t, maxsplit=1)
        lead = parts[0].strip().rstrip(',')
        tail = parts[1].strip()
        return f"Use a {lead} tone with {tail}."
    return f"Use a {t} tone."


def compose_unified_prompt(enhanced_text: str) -> str:
    """
    Parse the enhanced (multi-framework) prompt text and synthesize
    a single master prompt that can be used directly in an LLM.
    """
    try:
        # 1) Prefer a dedicated 'Rewritten Prompt' section if present.
        rewritten = _extract_rewritten_prompt(enhanced_text)
        if rewritten:
            return rewritten

        # 2) Fallback: extract first matching labeled lines in the enhanced text.
        role = _strip_markdown(_first_line_value(enhanced_text, ["Role", "Persona"]))
        audience = _strip_markdown(_first_line_value(enhanced_text, ["Audience"]))
        context = _strip_markdown(_first_line_value(enhanced_text, ["Context"]))
        ask = _strip_markdown(_first_line_value(enhanced_text, ["Ask"]))  # prefer Ask
        task = _strip_markdown(_first_line_value(enhanced_text, ["Task"]))  # fallback if no Ask
        tone = _strip_markdown(_first_line_value(enhanced_text, ["Tone", "Style"]))  # Style ~ Tone
        fmt = _strip_markdown(_first_line_value(enhanced_text, ["Format"]))
        action = _clean_action(_first_line_value(enhanced_text, ["Action"])) 

        # Build a unified natural-language prompt
        unified_parts = []

        if role:
            role = role.rstrip('.')
            unified_parts.append(f"Act as {role}.")
        if audience:
            unified_parts.append(f"Your audience is {audience.rstrip('.') }.")
        if context:
            unified_parts.append(f"Context: {context.rstrip('.') }.")
        if ask:
            unified_parts.append(f"{ask.rstrip('.')}.")
        elif task:
            unified_parts.append(f"{task.rstrip('.') }.")
        if action:
            unified_parts.append(f"Be sure to {action.rstrip('.') }.")
        if fmt:
            unified_parts.append(f"Deliver the output in this format: {fmt.rstrip('.') }.")
        if tone:
            tone_sentence = _format_tone(tone)
            if tone_sentence:
                unified_parts.append(tone_sentence)

        # Join into a coherent paragraph
        unified_prompt = " ".join(unified_parts)
        if not unified_prompt:
            unified_prompt = (
                "(Unable to synthesize unified prompt — missing identifiable fields.)"
            )

        return unified_prompt.strip()

    except Exception as e:
        return f"[ERROR in Unified Prompt Composer: {e}]"
