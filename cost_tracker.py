#!/usr/bin/env python3
"""
API Cost Tracker and Estimator
Monitor and estimate costs for AI Video Workflow APIs
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class APISpendingTracker:
    """Track and estimate API spending for the video workflow."""
    
    def __init__(self, tracking_file: str = "api_spending_log.json"):
        self.tracking_file = tracking_file
        self.costs = {
            "gemini_2_flash": {
                "input_per_1m_tokens": 0.075,   # $0.075 per 1M input tokens
                "output_per_1m_tokens": 0.30,   # $0.30 per 1M output tokens
                "description": "Gemini 2.0 Flash (Prompt Generation)"
            },
            "veo_3_1": {
                "per_video": 0.75,  # Estimated $0.75 per 8-second video
                "description": "Veo 3.1 Video Generation"
            },
            "gcs_storage": {
                "per_gb_month": 0.020,  # $0.020 per GB per month
                "per_operation": 0.0004,  # $0.0004 per operation
                "description": "Google Cloud Storage"
            }
        }
        
        # Load existing spending log
        self.spending_log = self.load_spending_log()
    
    def load_spending_log(self) -> List[Dict]:
        """Load spending log from file."""
        try:
            if os.path.exists(self.tracking_file):
                with open(self.tracking_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading spending log: {e}")
            return []
    
    def save_spending_log(self):
        """Save spending log to file."""
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(self.spending_log, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving spending log: {e}")
    
    def estimate_prompt_generation_cost(self, user_input: str, generated_prompts: str = None) -> Dict:
        """Estimate cost for prompt generation using Gemini."""
        
        # Rough token estimation (1 token ≈ 4 characters for English)
        input_chars = len(user_input)
        input_tokens = input_chars / 4
        
        # Estimate output tokens (generated prompts are typically longer)
        if generated_prompts:
            output_chars = len(generated_prompts)
        else:
            # Estimate: generated prompts are usually 3-5x longer than input
            output_chars = input_chars * 4
        
        output_tokens = output_chars / 4
        
        # Calculate costs
        input_cost = (input_tokens / 1_000_000) * self.costs["gemini_2_flash"]["input_per_1m_tokens"]
        output_cost = (output_tokens / 1_000_000) * self.costs["gemini_2_flash"]["output_per_1m_tokens"]
        total_cost = input_cost + output_cost
        
        return {
            "service": "Gemini 2.0 Flash",
            "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens),
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost,
            "timestamp": datetime.now().isoformat()
        }
    
    def estimate_video_generation_cost(self, num_videos: int = 4) -> Dict:
        """Estimate cost for video generation using Veo 3.1."""
        
        cost_per_video = self.costs["veo_3_1"]["per_video"]
        total_cost = num_videos * cost_per_video
        
        return {
            "service": "Veo 3.1 Video Generation",
            "num_videos": num_videos,
            "cost_per_video": cost_per_video,
            "total_cost": total_cost,
            "timestamp": datetime.now().isoformat()
        }
    
    def estimate_complete_workflow_cost(self, user_input: str, generated_prompts: str = None) -> Dict:
        """Estimate total cost for complete workflow."""
        
        prompt_cost = self.estimate_prompt_generation_cost(user_input, generated_prompts)
        video_cost = self.estimate_video_generation_cost(4)
        
        # Storage costs (minimal for most users)
        storage_cost = 0.05  # Estimated $0.05 for storage operations
        
        total_cost = prompt_cost["total_cost"] + video_cost["total_cost"] + storage_cost
        
        return {
            "breakdown": {
                "prompt_generation": prompt_cost,
                "video_generation": video_cost,
                "storage_operations": storage_cost
            },
            "total_estimated_cost": total_cost,
            "timestamp": datetime.now().isoformat()
        }
    
    def log_actual_usage(self, service: str, cost: float, details: Dict = None):
        """Log actual API usage and cost."""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "cost": cost,
            "details": details or {}
        }
        
        self.spending_log.append(log_entry)
        self.save_spending_log()
        
        print(f"✅ Logged {service}: ${cost:.4f}")
    
    def get_spending_summary(self, days: int = 30) -> Dict:
        """Get spending summary for the last N days."""
        
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_spending = [
            entry for entry in self.spending_log
            if datetime.fromisoformat(entry["timestamp"]) > cutoff_date
        ]
        
        # Group by service
        by_service = {}
        total_cost = 0
        
        for entry in recent_spending:
            service = entry["service"]
            cost = entry["cost"]
            
            if service not in by_service:
                by_service[service] = {"count": 0, "total_cost": 0}
            
            by_service[service]["count"] += 1
            by_service[service]["total_cost"] += cost
            total_cost += cost
        
        return {
            "period_days": days,
            "total_cost": total_cost,
            "by_service": by_service,
            "num_entries": len(recent_spending)
        }
    
    def print_cost_estimate(self, user_input: str):
        """Print a detailed cost estimate for user input."""
        
        print("\n" + "="*60)
        print("💰 API COST ESTIMATE")
        print("="*60)
        
        estimate = self.estimate_complete_workflow_cost(user_input)
        
        print(f"📝 Input length: {len(user_input)} characters")
        print(f"🔢 Estimated tokens: ~{len(user_input)/4:.0f} input + ~{len(user_input)*4/4:.0f} output")
        
        print(f"\n💡 COST BREAKDOWN:")
        print(f"├── Prompt Generation (Gemini): ${estimate['breakdown']['prompt_generation']['total_cost']:.4f}")
        print(f"├── Video Generation (Veo 3.1): ${estimate['breakdown']['video_generation']['total_cost']:.2f}")
        print(f"└── Storage Operations: ${estimate['breakdown']['storage_operations']:.2f}")
        
        print(f"\n🎯 TOTAL ESTIMATED COST: ${estimate['total_estimated_cost']:.2f}")
        
        # Cost per component breakdown
        prompt_cost = estimate['breakdown']['prompt_generation']['total_cost']
        video_cost = estimate['breakdown']['video_generation']['total_cost']
        
        print(f"\n📊 COST DISTRIBUTION:")
        print(f"   Prompts: {(prompt_cost/estimate['total_estimated_cost'])*100:.1f}%")
        print(f"   Videos:  {(video_cost/estimate['total_estimated_cost'])*100:.1f}%")
        
        print(f"\n⚠️  NOTE: Video generation is ~{video_cost/prompt_cost:.0f}x more expensive than prompts!")
        print("="*60)
    
    def print_spending_summary(self):
        """Print spending summary."""
        
        summary = self.get_spending_summary()
        
        print("\n" + "="*50)
        print("📈 SPENDING SUMMARY (Last 30 Days)")
        print("="*50)
        
        if summary["num_entries"] == 0:
            print("📭 No recorded spending yet")
            return
        
        print(f"💸 Total Spent: ${summary['total_cost']:.2f}")
        print(f"📊 Number of API calls: {summary['num_entries']}")
        
        print(f"\n📋 By Service:")
        for service, data in summary["by_service"].items():
            avg_cost = data["total_cost"] / data["count"]
            print(f"├── {service}:")
            print(f"│   └── {data['count']} calls, ${data['total_cost']:.2f} total, ${avg_cost:.4f} avg")
        
        print("="*50)


def analyze_cost_for_input(user_input: str):
    """Analyze and display cost estimate for given input."""
    
    tracker = APISpendingTracker()
    tracker.print_cost_estimate(user_input)
    
    # Interactive cost analysis
    print(f"\n🤔 COST OPTIMIZATION TIPS:")
    
    input_length = len(user_input)
    if input_length > 1000:
        print("📝 Consider shortening input to reduce token costs")
    
    if input_length < 200:
        print("📝 Input is cost-efficient for prompt generation")
    
    print("💡 Prompt generation is very cheap - focus on optimizing video generation")
    print("🎯 Use the interactive debugger to review videos before generating all 4")
    print("⏱️  Each video costs ~$0.75, so stopping after 1 bad video saves $2.25")


def main():
    """Interactive cost analysis."""
    
    print("💰 AI Video Workflow - Cost Analyzer")
    print("="*50)
    
    tracker = APISpendingTracker()
    
    # Show existing spending
    tracker.print_spending_summary()
    
    print("\n🔍 COST ANALYSIS OPTIONS:")
    print("1. Estimate cost for new input")
    print("2. View current pricing")
    print("3. Show spending log")
    print("4. Exit")
    
    while True:
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == "1":
            user_input = input("\nEnter your business description:\n")
            if user_input:
                analyze_cost_for_input(user_input)
            break
            
        elif choice == "2":
            print("\n💸 CURRENT API PRICING:")
            print("="*40)
            for service, pricing in tracker.costs.items():
                print(f"\n🔹 {pricing['description']}:")
                for key, value in pricing.items():
                    if key != 'description':
                        print(f"   {key}: ${value}")
            break
            
        elif choice == "3":
            if tracker.spending_log:
                print("\n📋 RECENT SPENDING LOG:")
                print("-"*40)
                for entry in tracker.spending_log[-10:]:  # Last 10 entries
                    timestamp = entry['timestamp'][:19]
                    print(f"{timestamp} | {entry['service']} | ${entry['cost']:.4f}")
            else:
                print("\n📭 No spending recorded yet")
            break
            
        elif choice == "4":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()