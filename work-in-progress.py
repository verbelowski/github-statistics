# As the name suggests, work in progress.

import os
from github import Github
from datetime import datetime, timedelta

TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "verbelowski"

g = Github(TOKEN)
user = g.get_user(USERNAME)

stars = sum(repo.stargazers_count for repo in user.get_repos())
forks = sum(repo.forks_count for repo in user.get_repos())


events = user.get_events()
all_time_contribs = sum(1 for _ in events)

repos_with_contribs = sum(1 for repo in user.get_repos() if repo.get_commits(author=user).totalCount > 0)

lines_changed = 0
for repo in user.get_repos():
    try:
        for commit in repo.get_commits(author=user):
            stats = commit.stats
            lines_changed += stats.additions + stats.deletions
    except:
        continue

views = {}
for repo in user.get_repos():
    try:
        traffic = repo.get_views_traffic()
        views[repo.name] = traffic['count']
    except:
        continue

print("=== STATYSTYKI OGÓLNE ===")
print(f"Stars: {stars}")
print(f"Forks: {forks}")
print(f"All-time contributions (ostatnie 300 eventów): {all_time_contribs}")
print(f"Lines of code changed: {lines_changed}")
print(f"Repositories with contributions: {repos_with_contribs}")
print(f"Repository views (past 2 weeks): {views}")

lang_stats = {}
for repo in user.get_repos():
    try:
        langs = repo.get_languages()
        for lang, size in langs.items():
            lang_stats[lang] = lang_stats.get(lang, 0) + size
    except:
        continue

print("\n=== STATYSTYKI JĘZYKOWE ===")
for lang, size in lang_stats.items():
    print(f"{lang}: {size} bytes")
