import os
import argparse
from dotenv import load_dotenv
from src.github_client import GitHubClient
from src.llm_orchestrator import LLMOrchestrator

# Load environment variables from .env file
load_dotenv()

def main():
    # Setup command line arguments
    parser = argparse.ArgumentParser(description="Multi-LLM Automated Code Reviewer")
    parser.add_argument("--repo", required=True, help="GitHub repository (e.g., 'owner/repo')")
    parser.add_argument("--pr", required=True, type=int, help="Pull Request number")
    parser.add_argument("--post-comment", action="store_true", help="Post the review as a PR comment")
    args = parser.parse_args()

    github = GitHubClient()
    orchestrator = LLMOrchestrator()

    print(f"🚀 Fetching diff for PR #{args.pr} in {args.repo}...")
    diff = github.get_pr_diff(args.repo, args.pr)

    if not diff.strip():
        print("⚠️ No changes found in this PR.")
        return

    print("🧠 Starting Multi-LLM Review Pipeline...")
    report = orchestrator.generate_review(diff)

    print("\n" + "="*50)
    print("FINAL REPORT:")
    print("="*50)
    print(report)

    if args.post_comment:
        print("\n📝 Posting comment to GitHub...")
        github.post_pr_comment(args.repo, args.pr, report)
        print("✅ Comment posted successfully!")

if __name__ == "__main__":
    main()