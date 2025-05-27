# Let's continue expanding the solution based on the user's request:
# - Post CI summary as a GitHub PR comment
# - Optional: Send result to Slack or Datadog (via webhook or API)
# - Include extra metadata (job URLs, timestamps, etc.)

# Updated Python script that:
# 1. Builds the markdown summary
# 2. Posts it to the GitHub PR as a comment
# (Assumes environment variables: GITHUB_TOKEN, GITHUB_REPOSITORY, GITHUB_PR_NUMBER)

enhanced_script = """
import os
import json
import requests

def load_job_data(name):
    try:
        with open(f"artifacts/{name}_result.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"status": "skipped", "message": "No data"}

# Load all job metadata
build = load_job_data("build")
sonar = load_job_data("sonar")
veracode = load_job_data("veracode")
publish = load_job_data("publish")

# Summary table
summary = [
    "| Stage     | Status   | Details |",
    "|-----------|----------|---------|",
    f"| Build     | {'✅' if build['status'] == 'success' else '❌'} | Coverage: {build.get('coverage', '-')}, Duration: {build.get('duration', '-')}s |",
    f"| SonarQube | {'✅' if sonar['status'] == 'success' else '❌'} | {sonar.get('message', '')} |",
    f"| Veracode  | {'✅' if veracode['status'] == 'success' else '❌'} | {veracode.get('message', '')} |",
    f"| Publish   | {'✅' if publish['status'] == 'success' else '⏭️ Skipped'} | {publish.get('message', '')} |",
]
summary_md = "\\n".join(summary)

# Recommendation
def recommend():
    if build['status'] != 'success':
        return "🛑 Fix build issues before merging."
    if sonar['status'] != 'success':
        return "🔍 Address quality issues reported by SonarQube."
    if veracode['status'] != 'success':
        return "🔐 Review security scan failures before deploying."
    return "🚀 All checks passed. You may promote this to staging or merge."

recommendation = recommend()

# GitHub PR comment posting
github_token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("GITHUB_PR_NUMBER")

if github_token and repo and pr_number:
    comment = f"## 🤖 CI Summary for PR #{pr_number}\\n\\n{summary_md}\\n\\n📌 **Recommendation**: {recommendation}"
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(url, headers=headers, json={"body": comment})
    if response.status_code == 201:
        print("✅ Summary posted to PR.")
    else:
        print(f"❌ Failed to post comment: {response.status_code} {response.text}")
else:
    print("\\n--- CI SUMMARY ---\\n")
    print(summary_md)
    print(f"\\n📌 Recommendation: {recommendation}")
    print("⚠️ GITHUB_TOKEN or PR context missing. Skipping PR comment.")
"""

# Return the enhanced version to the user
from IPython.display import Markdown
import textwrap

Markdown(f"### Updated Python Script (scripts/generate_ci_summary.py)\n```python\n{textwrap.dedent(enhanced_script)}\n```")
