import os
import requests
from datetime import datetime, timezone
from collections import defaultdict

USERNAME = "Jayx2u"
TEMPLATE_PATH = "templates/README.md.tpl"
OUTPUT_PATH = "README.md"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_stats():
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN must be set")

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"

    total_stars = 0
    public_repos = 0
    language_bytes = defaultdict(int)

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

    # Top 3 Languages
    sorted_languages = sorted(language_bytes.items(), key=lambda item: item[1], reverse=True)
    top_languages = ", ".join([lang for lang, count in sorted_languages[:3]])

    return {
        "total_stars": total_stars,
        "public_repos": public_repos,
        "top_languages": top_languages,
    }

def generate_readme(stats):
    with open(TEMPLATE_PATH) as f:
        template: f.read()

    readme_content = readme_content.replace("{{TOTAL_STARS}}", str(stats["total_stars"]))
    readme_content = readme_content.replace("{{PUBLIC_REPOS}}", str(stats["public_repos"]))
    readme_content = readme_content.replace("{{PUBLIC_LANGUAGES}}", stats["top_languages"])
    readme_content = readme_content.replace("{{LAST_UPDATED}}", datetime.now(timezone.utc).strftime("%d %B %Y"))

    with open(OUTPUT_PATH, "w") as f:
        f.write(readme_content)

if __name__ == "__main__":
    stats = fetch_stats()
    generate_readme(stats)

