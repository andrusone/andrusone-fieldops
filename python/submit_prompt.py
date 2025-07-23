#!/usr/bin/env python3
"""
submit_prompt.py

Purpose:
    Submit a prompt to OpenAI's API for either text or image generation (Chat or DALL·E).
    Save the full response and result to disk using a unique filename.

Audience:
    Developers using openai>=1.0.0 for automated workflows.

Environment Variables:
    OPENAI_API_KEY - your OpenAI API key
    OUTPUT_PATH    - optional default output directory

Usage (CLI):
    python submit_prompt.py --prompt "A robot painting a sunset" --output-type image
    python submit_prompt.py --prompt "Explain quantum tunneling" --output-type text --output-path ./responses

Usage (imported):
    from submit_prompt import submit_prompt
    files = submit_prompt("Describe gravity", "text", "./out")
"""

import os
import json
import uuid
import argparse
import datetime
import requests
from typing import List, Optional

import openai

# ---------------------- Environment & Client ---------------------- #
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")

client = openai.OpenAI(api_key=api_key)

# ---------------------- Helpers ---------------------- #
def unique_basename() -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"response_{timestamp}_{uuid.uuid4().hex[:6]}"

def save_json(filepath: str, data: dict) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_text(filepath: str, text: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

def save_image_from_url(url: str, filepath: str) -> None:
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, "wb") as f:
        f.write(response.content)

# ---------------------- Main Callable ---------------------- #
def submit_prompt(prompt: str, output_type: str, output_path: Optional[str] = None) -> List[str]:
    """Submit a prompt to OpenAI and save result and response JSON to disk.

    Args:
        prompt (str): The user input prompt.
        output_type (str): 'text' or 'image'.
        output_path (str, optional): Output directory. Uses $OUTPUT_PATH or "." if None.

    Returns:
        List[str]: List of file paths written (text/image + json).
    """
    output_dir = output_path or os.getenv("OUTPUT_PATH") or "."
    os.makedirs(output_dir, exist_ok=True)

    basename = unique_basename()
    json_filepath = os.path.join(output_dir, f"{basename}.json")
    written_files = []

    try:
        if output_type == "text":
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            text_filepath = os.path.join(output_dir, f"{basename}.txt")
            save_text(text_filepath, content)
            written_files.append(text_filepath)
            save_json(json_filepath, response.model_dump())
            written_files.append(json_filepath)

        elif output_type == "image":
            response = client.images.generate(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            image_filepath = os.path.join(output_dir, f"{basename}.png")
            save_image_from_url(image_url, image_filepath)
            written_files.append(image_filepath)
            save_json(json_filepath, response.model_dump())
            written_files.append(json_filepath)

    except Exception as e:
        error_details = {
            "error": str(e),
            "prompt": prompt,
            "output_type": output_type
        }
        save_json(json_filepath, error_details)
        written_files.append(json_filepath)
        print(f"[ERROR] {e}. Details written to {json_filepath}")
    else:
        print(f"[SUCCESS] Files saved: {written_files}")

    return written_files

def run_chat_prompt(prompt: str, system_prompt: Optional[str] = None, model: str = "gpt-4o") -> str:
    """Run a ChatCompletion with optional system prompt. Returns response text only."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content.strip()

# ---------------------- CLI Entry ---------------------- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit a prompt to OpenAI.")
    parser.add_argument("--prompt", required=True, help="Prompt to send to the API.")
    parser.add_argument("--output-type", choices=["text", "image"], required=True, help="Expected output type.")
    parser.add_argument("--output-path", help="Directory where output will be saved.")
    args = parser.parse_args()

    submit_prompt(args.prompt, args.output_type, args.output_path)

