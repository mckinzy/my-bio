#!/usr/bin/env python3
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "prompts" / "profile_prompt_loop.md"
OUTPUT = ROOT / "generated" / "profile_loop_output.md"

if not TEMPLATE.exists():
    raise SystemExit(f"Missing template: {TEMPLATE}")

prompt = TEMPLATE.read_text(encoding="utf-8")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(prompt, encoding="utf-8")
print(f"Prompt loop generated at {OUTPUT}")
print("Run the preview server with: ./scripts/serve.sh")
