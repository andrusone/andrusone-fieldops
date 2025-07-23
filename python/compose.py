#!/usr/bin/env python3
"""
compose.py – Multi-step prompt composition engine using OpenAI

Purpose:
    This script automates AI-assisted content generation using a configurable workflow.
    It reads topics from a text file and applies a series of templated AI prompts to
    each topic, passing results from one step to the next.

Audience:
    Engineers, content creators, and automation builders who need reliable,
    repeatable prompt workflows with minimal configuration.

Value Created:
    - Converts simple topic lists into polished multi-step AI outputs
    - Enables templated prompt reuse with system and user roles
    - Scales creative or editorial pipelines using GPT models

Usage:
    python compose.py [--topics topics.txt] [--workflow prompt_workflow.yaml] [--output-dir outputs/]

Value Realized:
    Outputs are saved to the specified output directory, named per topic,
    ready for downstream publishing or review.

Design:
    - Uses `submit_prompt.py` for OpenAI chat completions
    - Prompts are chained, with each step's output used as input for the next
    - Templates support `{topic}` and `{input}` for flexible chaining
"""

import os
import argparse
import yaml
from submit_prompt import submit_prompt

def load_topics(filepath):
    """Load topic list from file, one topic per line."""
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_workflow(filepath):
    """Load YAML-based multi-step prompt workflow."""
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_workflow_on_topic(topic, workflow):
    """
    Apply the full prompt workflow to a single topic.

    Args:
        topic (str): The topic to generate content for.
        workflow (list): List of prompt steps with 'system' and 'prompt'.

    Returns:
        str: Final output after running all steps.
    """
    data = topic
    for step in workflow:
        prompt = step["prompt"].format(topic=topic, input=data)
        response = submit_prompt(prompt, system_prompt=step.get("system"))
        data = response
    return data

def main():
    parser = argparse.ArgumentParser(description="Compose multi-step AI prompts from a topic list.")
    parser.add_argument("--topics", default="topics.txt", help="Path to the topic list file")
    parser.add_argument("--workflow", default="prompt_workflow.yaml", help="Path to the workflow YAML file")
    parser.add_argument("--output-dir", default="outputs/", help="Directory to write final outputs")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    topics = load_topics(args.topics)
    workflow = load_workflow(args.workflow)

    for topic in topics:
        final_output = run_workflow_on_topic(topic, workflow)
        output_path = os.path.join(args.output_dir, f"{topic.replace(' ', '_')}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_output)

if __name__ == "__main__":
    main()

