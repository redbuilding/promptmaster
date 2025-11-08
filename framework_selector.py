def select_frameworks(user_prompt: str):
    """
    Simple heuristic selector for prompt frameworks.
    Extend this logic with pattern recognition or a small model later.
    """
    text = user_prompt.lower()
    frameworks = []

    # Analysis / reasoning
    if any(k in text for k in ["analyze", "why", "compare", "evaluate", "recommend", "reason", "steps"]):
        frameworks += ["CoT", "DEEP", "SCOR"]
    # Self-consistency for higher confidence
    if any(k in text for k in ["multiple solutions", "self-consistency", "try several", "best answer"]):
        frameworks += ["CoT+SC"]
    # Writing / content creation
    if any(k in text for k in ["write", "create", "story", "copy", "draft", "blog", "article", "post"]):
        frameworks += ["CRAFT", "TACT", "FEARS", "PEEL"]
    # Summarization / clarity
    if any(k in text for k in ["summarize", "overview", "simplify", "explain", "condense"]):
        frameworks += ["ICED", "Prompt Sandwich"]
    # Data / analysis with structure
    if any(k in text for k in ["data", "table", "insight", "metric", "analyze data", "dataset"]):
        frameworks += ["DIET", "TREE"]
    # Editing / improvement
    if any(k in text for k in ["improve", "refine", "revise", "edit", "polish"]):
        frameworks += ["CUP", "ICED", "LEAP"]
    # Tool-using agent styles
    if any(k in text for k in ["act", "observe", "tool", "search", "browse", "action plan", "react"]):
        frameworks += ["ReACT"]
    # Communication alignment
    if any(k in text for k in ["audience", "purpose", "message", "persona"]):
        frameworks += ["RAP", "RTCO"]
    # Instructional / teaching / steps
    if any(k in text for k in ["teach", "lesson", "tutorial", "steps", "guide", "instruct", "expectation"]):
        frameworks += ["RAISE", "SCQA"]
    # Decision / selection tasks
    if any(k in text for k in ["decide", "choose", "select", "evaluate options", "tradeoffs"]):
        frameworks += ["APE", "SCOR"]
    # Dialogue / conversational agent
    if any(k in text for k in ["chatbot", "dialogue", "conversation", "role-play", "assistant"]):
        frameworks += ["PAIR"]
    # Strategy / creative mapping
    if any(k in text for k in ["motivation", "brainstorm", "parameters", "product", "strategy", "map"]):
        frameworks += ["MAPP"]
    # Coaching / goal setting
    if any(k in text for k in ["coach", "goal", "reality", "options", "way forward", "plan"]):
        frameworks += ["GROW"]
    # General structural prompt when unclear
    if any(k in text for k in ["outline", "structure", "format", "role", "context", "output"]):
        frameworks += ["RTCO"]

    # Default fallback
    if not frameworks:
        frameworks = ["CRISPE"]

    # Deduplicate while preserving order, then cap to at most 3
    unique = list(dict.fromkeys(frameworks))
    return unique[:3]
