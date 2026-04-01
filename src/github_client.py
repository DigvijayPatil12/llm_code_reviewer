import os
from github import Github

class GitHubClient:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN is missing from environment variables.")
        self.client = Github(token)

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        """Fetches the diff of all files changed in a PR."""
        repo = self.client.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        
        diff_content = ""
        for file in pr.get_files():
            diff_content += f"### File: {file.filename}\n```diff\n{file.patch}\n```\n\n"
        return diff_content

    def get_full_repo_content(self, repo_name: str, limit_files: int = 12) -> str:
        """Scans the repo for core logic files to build a context window."""
        repo = self.client.get_repo(repo_name)
        contents = repo.get_contents("")
        repo_text = ""
        count = 0
        
        # Priority extensions for analysis
        valid_exts = ('.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.php')
        
        while contents and count < limit_files:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                # Don't go too deep into hidden folders or node_modules
                if not file_content.name.startswith(('.', 'node_modules', 'venv', 'env')):
                    contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.name.endswith(valid_exts):
                    try:
                        repo_text += f"\n\n--- FILE: {file_content.path} ---\n"
                        repo_text += file_content.decoded_content.decode("utf-8")[:3000] 
                        count += 1
                    except:
                        continue
        return repo_text