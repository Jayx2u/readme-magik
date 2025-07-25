import os
import sys
import requests
from datetime import datetime, timezone
from collections import defaultdict

USERNAME = os.getenv("GITHUB_USERNAME")
TEMPLATE_PATH = "templates/README.md.tpl"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
MAX_COMMITS = 5


def fetch_stats():
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN must be set")
    if not USERNAME:
        raise ValueError("GITHUB_USERNAME environment variable not set")

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    events_url = f"https://api.github.com/users/{USERNAME}/events/public"

    total_stars = 0
    public_repos = 0
    language_bytes = defaultdict(int)

    # Fetch repo stats
    page = 1
    while True:
        response = requests.get(f"{repos_url}&page={page}", headers=headers)
        response.raise_for_status()
        repos = response.json()
        if not repos:
            break

        for repo in repos:
            if not repo["fork"]:
                public_repos += 1
                total_stars += repo["stargazers_count"]
                if repo["language"]:
                    language_bytes[repo["language"]] += 1

        page += 1

    # Top 3 languages
    sorted_languages = sorted(language_bytes.items(), key=lambda item: item[1], reverse=True)
    top_languages = ", ".join([lang for lang, count in sorted_languages[:3]])

    # Fetch latest commits
    latest_commits = []

    # Add 'Cache-Control: no-cache' to request fresh data
    event_headers = headers.copy()
    event_headers["Cache-Control"] = "no-cache"

    response = requests.get(events_url, headers=headers)
    response.raise_for_status()
    events = response.json()

    for event in events:
        # Filter PushEvents by the actor's login to match the USERNAME
        if event['type'] == 'PushEvent' and event['actor']['login'] == USERNAME:
            for commit in event['payload']['commits']:
                repo_name = event['repo']['name']
                repo_url = f"https://github.com/{repo_name}"

                # Truncate long commit messages
                commit_message = commit['message'].split('\n')[0]
                commit_line = f'- [`{repo_name}`]({repo_url}) - *"{commit_message}"*'
                latest_commits.append(commit_line)
                if len(latest_commits) >= MAX_COMMITS:
                    break

        if len(latest_commits) >= MAX_COMMITS:
            break

    return {
        "total_stars": total_stars,
        "public_repos": public_repos,
        "top_languages": top_languages,
        "latest_commits": "\n".join(latest_commits),
    }


def generate_readme(stats, output_path):
    with open(TEMPLATE_PATH, "r") as f:
        template = f.read()

    readme_content = template.replace("{{TOTAL_STARS}}", str(stats["total_stars"]))
    readme_content = readme_content.replace("{{PUBLIC_REPOS}}", str(stats["public_repos"]))
    readme_content = readme_content.replace("{{TOP_LANGUAGES}}", stats["top_languages"])
    readme_content = readme_content.replace("{{LATEST_COMMITS}}", stats["latest_commits"])
    readme_content = readme_content.replace("{{LAST_UPDATED}}", datetime.now(timezone.utc).strftime("%d %B %Y %H:%M:%S UTC"))

    with open(output_path, "w") as f:
        f.write(readme_content)
    print(f"README.md generated at {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Output directory not provided.")
        sys.exit(1)

    output_dir = sys.argv[1]
    output_path = os.path.join(output_dir, 'README.md')

    stats = fetch_stats()
    generate_readme(stats, output_path)