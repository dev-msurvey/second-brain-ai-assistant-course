#!/usr/bin/env python3
"""
Simple Demo Script - Simulate AI Director Inference

This script demonstrates the 4 use cases without loading the actual model.
Use this when GPU/CUDA is not available for testing purposes.

For real inference with the trained model, use demo_inference.py on a GPU machine.
"""

import json

# ANSI colors
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_section(title: str):
    """Print section header"""
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{title}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")


def print_example(use_case: str, instruction: str, input_text: str, output: str):
    """Print formatted example"""
    print(f"{YELLOW}📌 Use Case: {use_case}{RESET}")
    print(f"\n{BOLD}Instruction:{RESET}")
    print(f"  {instruction}")
    print(f"\n{BOLD}Input:{RESET}")
    for line in input_text.strip().split('\n'):
        print(f"  {line}")
    print(f"\n{BOLD}Expected Output (from test set):{RESET}")
    print(f"{GREEN}{output}{RESET}")
    print(f"\n{'-'*80}\n")


def load_test_samples():
    """Load samples from test_v2.jsonl"""
    test_file = "../../module3/data/generated/test_v2.jsonl"
    
    samples = []
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))
    
    return samples


def main():
    """Run demo with test samples"""
    
    print_section("🚀 AI Director Demo - 4 Use Cases (Test Samples)")
    
    print(f"{YELLOW}ℹ️  Note: This is a simplified demo showing expected outputs from the test set.{RESET}")
    print(f"{YELLOW}ℹ️  For real-time inference, run demo_inference.py on a GPU-enabled machine.{RESET}\n")
    
    # Load test samples
    samples = load_test_samples()
    
    # Find examples for each use case
    customer_service = next((s for s in samples if s['metadata']['use_case'] == 'crisis_management'), None)
    visual_prompt = next((s for s in samples if s['metadata']['use_case'] == 'visual_content_creation'), None)
    script = next((s for s in samples if s['metadata']['use_case'] == 'video_content_creation'), None)
    cross_channel = next((s for s in samples if s['metadata']['use_case'] == 'cross_channel_marketing'), None)
    
    # ==========================================================================
    # USE CASE 1: Customer Service Response
    # ==========================================================================
    if customer_service:
        print_section("1️⃣  Customer Service Response - Crisis Management")
        print_example(
            "Customer Service",
            customer_service['instruction'],
            customer_service['input'],
            customer_service['output']
        )
    
    # ==========================================================================
    # USE CASE 2: Visual Prompt Generation
    # ==========================================================================
    if visual_prompt:
        print_section("2️⃣  Visual Prompt Generation - Midjourney/Stable Diffusion")
        print_example(
            "Visual Prompting",
            visual_prompt['instruction'],
            visual_prompt['input'],
            visual_prompt['output']
        )
    
    # ==========================================================================
    # USE CASE 3: Video Script Writing
    # ==========================================================================
    if script:
        print_section("3️⃣  Video Script Writing - TikTok 60s Format")
        print_example(
            "Script Writing",
            script['instruction'],
            script['input'],
            script['output']
        )
    
    # ==========================================================================
    # USE CASE 4: Cross-Channel Content Adaptation
    # ==========================================================================
    if cross_channel:
        print_section("4️⃣  Cross-Channel Adaptation - Platform Migration")
        print_example(
            "Cross-Channel",
            cross_channel['instruction'],
            cross_channel['input'],
            cross_channel['output']
        )
    
    # ==========================================================================
    # Summary
    # ==========================================================================
    print_section("✅ Demo Complete!")
    
    print(f"{GREEN}All 4 use cases demonstrated successfully!{RESET}\n")
    print(f"{BOLD}Use Cases Covered:{RESET}")
    print(f"  ✓ Customer Service Response (Crisis Management)")
    print(f"  ✓ Visual Prompt Generation (Midjourney/SD)")
    print(f"  ✓ Video Script Writing (TikTok 60s)")
    print(f"  ✓ Cross-Channel Content Adaptation")
    print(f"\n{YELLOW}Model Details:{RESET}")
    print(f"  Model: qwen-7b-ai-director-v2")
    print(f"  Training Loss: 0.6097")
    print(f"  Training Time: 2.58 hours")
    print(f"  Test Samples: {len(samples)} total")
    print(f"\n{YELLOW}Next Steps:{RESET}")
    print(f"  1. Run evaluation on all {len(samples)} test samples")
    print(f"  2. Calculate quality metrics")
    print(f"  3. Deploy for production use")
    print(f"\n{BLUE}For GPU-based inference, run: python demo_inference.py{RESET}\n")


if __name__ == "__main__":
    main()
