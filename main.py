#!/usr/bin/env python3
import sys
from framework_selector import select_frameworks
from prompt_rewriter import rewrite_prompt
from utils import save_prompt_to_markdown
from prompt_composer import compose_unified_prompt  # NEW IMPORT


def main():
    print("\n🤖 Prompt Framework Enhancer — Unified Edition\n")
    try:
        user_prompt = input("Enter your prompt: ").strip()
        if not user_prompt:
            print("[ERROR] Empty prompt. Exiting.")
            sys.exit(1)

        frameworks = select_frameworks(user_prompt)
        print(f"\n🔍 Selected Frameworks: {', '.join(frameworks)}")

        enhanced_prompt = rewrite_prompt(user_prompt, frameworks)
        if enhanced_prompt:
            print("\n--- Enhanced Prompt ---\n")
            print(enhanced_prompt)

            # ✅ Compose a unified prompt only if meaningful
            unified_prompt = compose_unified_prompt(enhanced_prompt)
            is_unified_meaningful = bool(unified_prompt) and not str(unified_prompt).startswith("(")

            if is_unified_meaningful and len(frameworks) > 1:
                print("\n--- Unified Prompt ---\n")
                print(unified_prompt)

            # Save to markdown (include Unified section only if meaningful)
            combined_output = "# Enhanced Prompt\n\n" + enhanced_prompt
            if is_unified_meaningful and len(frameworks) > 1:
                combined_output += "\n\n# Unified Prompt\n\n" + unified_prompt + "\n"
            save_prompt_to_markdown(combined_output)
        else:
            print("[ERROR] Could not generate enhanced prompt.")
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    main()
