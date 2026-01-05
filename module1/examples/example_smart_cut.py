"""
Example: Smart Cut Workflow

This example shows the complete Smart Cut workflow:
1. Video analysis with T5Gemma 2
2. Edit decision making
3. Tool calling with FunctionGemma
4. Video execution

Module 1: Dual-Model Architecture Design
"""

import sys
sys.path.append('..')

from ai_director_agent import AIDirectorAgent
import json


def example_basic_smart_cut():
    """Basic Smart Cut workflow"""
    print("=" * 70)
    print("✂️ EXAMPLE 1: Basic Smart Cut")
    print("=" * 70)
    print()
    
    # Initialize agent
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=True)
    
    # Process video
    result = agent.process_video_edit(
        video_path="product_review.mp4",
        requirements="Extract best moments about product features",
        target_duration=90
    )
    
    # Show results
    print("\n📊 Smart Cut Results:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()


def example_interview_highlights():
    """Extract highlights from interview"""
    print("=" * 70)
    print("✂️ EXAMPLE 2: Interview Highlights")
    print("=" * 70)
    print()
    
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
    
    # Mock interview transcript (in real usage, from Whisper)
    mock_transcript = """
    [00:00:15] Interviewer: สวัสดีครับ วันนี้เรามีแขกรับเชิญพิเศษ
    [00:00:30] Guest: สวัสดีครับ ยินดีมากครับ
    [00:01:00] Interviewer: เล่าให้ฟังหน่อยว่า startup ของคุณทำอะไร
    [00:01:15] Guest: เราทำ AI platform สำหรับ marketing automation
    [00:01:45] Guest: ช่วยให้ SME ทำ content ได้เร็วขึ้น ถูกลง 10 เท่า
    [00:02:30] ... (silence) ...
    [00:03:00] Interviewer: ท้าทายอะไรบ้างในการพัฒนา
    [00:03:15] Guest: ท้าทายที่สุดคือ Thai language support
    [00:03:45] Guest: เพราะ model ส่วนใหญ่ train ด้วยภาษาอังกฤษ
    [00:04:30] ... (tangent about other topics) ...
    [00:06:00] Interviewer: แผนอนาคตเป็นอย่างไร
    [00:06:15] Guest: เราจะ expand ไป Southeast Asia ในปีหน้า
    [00:06:45] Guest: และเพิ่ม features สำหรับ video content
    [00:07:30] Interviewer: ขอบคุณมากครับ
    """
    
    print("📹 Input: 30-minute founder interview")
    print("🎯 Goal: 2-minute highlight reel for social media")
    print("📝 Focus: Product, challenges, vision")
    print()
    
    # Process with Smart Cut
    result = agent.process_video_edit(
        video_path="founder_interview_30min.mp4",
        requirements="Extract: product description, key challenges, future vision",
        target_duration=120
    )
    
    print("✅ Smart Cut Analysis:")
    print("-" * 70)
    print(f"Original duration: ~30 minutes")
    print(f"Target duration: {result['target_duration']}s (2 min)")
    print(f"Processing time: {result['duration_seconds']:.2f}s")
    print()
    
    print("🎬 Suggested Segments:")
    # In real implementation, this would be parsed from analysis
    segments = [
        {"time": "01:15-01:45", "content": "Product description"},
        {"time": "03:15-03:45", "content": "Thai language challenge"},
        {"time": "06:15-06:45", "content": "Future expansion plans"}
    ]
    for seg in segments:
        print(f"  • {seg['time']}: {seg['content']}")
    print()


def example_tutorial_summary():
    """Summarize long tutorial video"""
    print("=" * 70)
    print("✂️ EXAMPLE 3: Tutorial Summary")
    print("=" * 70)
    print()
    
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
    
    print("📹 Input: 45-minute coding tutorial")
    print("🎯 Goal: 3-minute summary for beginners")
    print("📝 Focus: Key concepts and steps")
    print()
    
    result = agent.process_video_edit(
        video_path="python_tutorial_45min.mp4",
        requirements="""
        Create beginner-friendly summary covering:
        - Introduction to Python
        - Basic syntax examples
        - Most important concept
        - Next steps recommendation
        """,
        target_duration=180
    )
    
    print(f"✅ Tutorial summarized in {result['duration_seconds']:.2f}s")
    print(f"📊 Compression: 45 min → 3 min (94% reduction)")
    print()


def example_webinar_key_moments():
    """Extract key moments from webinar"""
    print("=" * 70)
    print("✂️ EXAMPLE 4: Webinar Key Moments")
    print("=" * 70)
    print()
    
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
    
    scenarios = [
        {
            "video": "marketing_webinar_2hr.mp4",
            "duration": 7200,  # 2 hours
            "target": 300,  # 5 minutes
            "focus": "Key insights and Q&A highlights"
        },
        {
            "video": "product_demo_1hr.mp4",
            "duration": 3600,  # 1 hour
            "target": 180,  # 3 minutes
            "focus": "Core features and use cases"
        },
        {
            "video": "panel_discussion_90min.mp4",
            "duration": 5400,  # 90 minutes
            "target": 240,  # 4 minutes
            "focus": "Best expert opinions and debates"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎬 Scenario {i}:")
        print(f"   Video: {scenario['video']}")
        print(f"   Original: {scenario['duration']//60} minutes")
        print(f"   Target: {scenario['target']//60} minutes")
        print(f"   Focus: {scenario['focus']}")
        
        result = agent.process_video_edit(
            video_path=scenario['video'],
            requirements=scenario['focus'],
            target_duration=scenario['target']
        )
        
        compression_rate = (1 - scenario['target']/scenario['duration']) * 100
        print(f"   ✅ Compressed: {compression_rate:.1f}% reduction")
        print(f"   ⏱️ Processed in: {result['duration_seconds']:.2f}s")
    
    print()


def example_multi_language():
    """Handle videos in different languages"""
    print("=" * 70)
    print("✂️ EXAMPLE 5: Multi-Language Videos")
    print("=" * 70)
    print()
    
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
    
    languages = [
        {
            "video": "thai_presentation.mp4",
            "language": "Thai",
            "requirements": "Extract key messages about business model"
        },
        {
            "video": "english_interview.mp4",
            "language": "English",
            "requirements": "Highlight technical innovations discussed"
        },
        {
            "video": "mixed_language_panel.mp4",
            "language": "Thai+English",
            "requirements": "Keep both languages, focus on main topics"
        }
    ]
    
    for i, lang_test in enumerate(languages, 1):
        print(f"\n🌍 Language Test {i}: {lang_test['language']}")
        print(f"   Video: {lang_test['video']}")
        print(f"   Task: {lang_test['requirements']}")
        
        result = agent.process_video_edit(
            video_path=lang_test['video'],
            requirements=lang_test['requirements'],
            target_duration=120
        )
        
        print(f"   ✅ Processed successfully")
        print(f"   ⏱️ Time: {result['duration_seconds']:.2f}s")
    
    print()


def example_batch_processing():
    """Process multiple videos"""
    print("=" * 70)
    print("✂️ EXAMPLE 6: Batch Video Processing")
    print("=" * 70)
    print()
    
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
    
    # Batch of videos to process
    videos = [
        {"path": "day1_morning.mp4", "target": 60},
        {"path": "day1_afternoon.mp4", "target": 90},
        {"path": "day2_morning.mp4", "target": 60},
        {"path": "day2_afternoon.mp4", "target": 90},
        {"path": "day3_highlights.mp4", "target": 120},
    ]
    
    print(f"📦 Processing {len(videos)} videos...")
    print()
    
    results = []
    total_time = 0
    
    for i, video in enumerate(videos, 1):
        print(f"🎬 Processing {i}/{len(videos)}: {video['path']}")
        
        result = agent.process_video_edit(
            video_path=video['path'],
            requirements="Extract key moments",
            target_duration=video['target']
        )
        
        results.append(result)
        total_time += result['duration_seconds']
        
        print(f"   ✅ Complete ({result['duration_seconds']:.2f}s)")
    
    print()
    print("📊 Batch Processing Summary:")
    print(f"   Total videos: {len(videos)}")
    print(f"   Total time: {total_time:.2f}s ({total_time/60:.2f} min)")
    print(f"   Average: {total_time/len(videos):.2f}s per video")
    print()


if __name__ == "__main__":
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "✂️ SMART CUT WORKFLOW EXAMPLES" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    # Run examples
    example_basic_smart_cut()
    example_interview_highlights()
    example_tutorial_summary()
    example_webinar_key_moments()
    example_multi_language()
    example_batch_processing()
    
    print("\n🎉 All Smart Cut examples completed!\n")
