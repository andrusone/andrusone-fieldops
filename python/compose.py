#!/usr/bin/env python3
"""
generate_combinations.py – Structured prompt runner for profession/activity/feeling workflows

Supports:
- Loading profession-activity and feeling dictionaries
- Running a multi-step workflow with named steps
- Referencing prior step outputs via `{r:step_name}`
- Saving full response trace per run as a .dict file

Usage:
    python generate_combinations.py \
        --professions data/professions.yaml \
        --feelings data/feelings.yaml \
        --workflow test-compose.yaml
"""

import os
import re
import json
import yaml
import argparse
from submit_prompt import run_chat_prompt


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        if filepath.endswith(".json"):
            return json.load(f)
        elif filepath.endswith((".yaml", ".yml")):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file type: {filepath}")


def load_workflow(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def slugify(text):
    return text.lower().replace(" ", "_").replace(",", "").replace(":", "").replace("-", "_")


def substitute_prompt_template(template, context, response_dict):
    """
    Replace {input}, {profession}, etc. with context
    Replace {r:step_name} with the value of that step's response
    """
    def replace_token(match):
        token = match.group(1)
        if token.startswith("r:"):
            step_key = token[2:]
            return response_dict.get(step_key, f"[MISSING:{step_key}]")
        return context.get(token, f"[UNKNOWN:{token}]")

    return re.sub(r"\{([^\}]+)\}", replace_token, template)


def run_workflow(context, workflow):
    """Run each step and capture all responses into a dictionary keyed by step name."""
    responses = {}
    print (context)
    for step in workflow:
        step_name = step["name"]
        prompt = substitute_prompt_template(step["prompt"], context, responses)
        system_prompt = substitute_prompt_template(step.get("system", ""), context, responses)
        print (step_name + " - " + prompt)

        result = run_chat_prompt(prompt, system_prompt=system_prompt)
        responses[step_name] = result
    return responses


def write_dict(path, data):
    if path.endswith(".json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)


def main():
    parser = argparse.ArgumentParser(description="Run AI prompt workflows on structured profession/feeling input.")
    parser.add_argument("--professions", required=True, help="Path to professions YAML/JSON file")
    parser.add_argument("--feelings", required=True, help="Path to feelings YAML/JSON file")
    parser.add_argument("--workflow", required=True, help="Path to prompt workflow YAML file")
    parser.add_argument("--output-dir", default="outputs", help="Directory to write results (default: outputs/)")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    professions = load_data(args.professions)
    feelings = load_data(args.feelings)
    workflow = load_workflow(args.workflow)

    for profession, activities in professions.items():
        for activity in activities:
            for feeling_category, feeling_list in feelings.items():
                for feeling in feeling_list:
                    context = {
                        "profession": profession,
                        "activity": activity,
                        "feeling": feeling,
                        "feeling_category": feeling_category,
                        "input": f"A {profession} who is feeling {feeling} while {activity}"
                    }

                    responses = run_workflow(context, workflow)

                    filename_base = f"{slugify(profession)}_{slugify(activity)}_{slugify(feeling)}"
                    text_output = os.path.join(args.output_dir, f"{filename_base}.txt")
                    dict_output = os.path.join(args.output_dir, f"{filename_base}.dict.yaml")

                    # Final step output
                    last_step = workflow[-1]["name"]
                    with open(text_output, "w", encoding="utf-8") as f:
                        f.write(responses[last_step])

                    # Full response dictionary
                    write_dict(dict_output, responses)

if __name__ == "__main__":
    main()

