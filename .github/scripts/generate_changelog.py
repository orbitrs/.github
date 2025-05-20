#!/usr/bin/env python3
"""
Generate a changelog from git commit history.
This script will generate a changelog from the git commit history.
It groups commits by type (feature, fix, etc) based on conventional commits format.
"""

import re
import subprocess
from datetime import datetime
from collections import defaultdict
import sys

# Define the types of commits we want to group
COMMIT_TYPES = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "docs": "Documentation",
    "style": "Style",
    "refactor": "Refactoring",
    "perf": "Performance",
    "test": "Tests",
    "build": "Build",
    "ci": "CI",
    "chore": "Chores",
    "revert": "Reverts",
}

# Regex to match conventional commits
COMMIT_PATTERN = r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(?:\(([^\)]+)\))?: (.+)$"

def get_latest_tag():
    """Get the latest tag or return None if no tags exist."""
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return tag
    except subprocess.CalledProcessError:
        return None

def get_commit_range():
    """Get the commit range for the changelog."""
    latest_tag = get_latest_tag()
    if latest_tag:
        return f"{latest_tag}..HEAD"
    return "HEAD"

def parse_commits(commit_range):
    """Parse commits from the given range."""
    output = subprocess.check_output(
        ["git", "log", "--pretty=format:%s|%h|%an|%ad", "--date=short", commit_range]
    ).decode()
    
    commits_by_type = defaultdict(list)
    other_commits = []
    
    for line in output.split("\n"):
        if not line.strip():
            continue
            
        parts = line.split("|")
        if len(parts) < 4:
            continue
            
        subject, commit_hash, author, date = parts
        
        match = re.match(COMMIT_PATTERN, subject)
        if match:
            commit_type, scope, message = match.groups()
            scope_text = f"**{scope}:** " if scope else ""
            commits_by_type[commit_type].append({
                "message": f"{scope_text}{message}",
                "hash": commit_hash,
                "author": author,
                "date": date
            })
        else:
            other_commits.append({
                "message": subject,
                "hash": commit_hash,
                "author": author,
                "date": date
            })
    
    return commits_by_type, other_commits

def generate_changelog():
    """Generate the changelog content."""
    commit_range = get_commit_range()
    commits_by_type, other_commits = parse_commits(commit_range)
    
    today = datetime.now().strftime("%Y-%m-%d")
    latest_tag = get_latest_tag() or "Unreleased"
    version = latest_tag.lstrip("v") if latest_tag != "Unreleased" else "Unreleased"
    
    # Start building the changelog
    changelog = [
        "# Changelog\n",
        "All notable changes to this project will be documented in this file.\n",
        "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).\n\n",
    ]
    
    # Add the latest version
    changelog.append(f"## [{version}] - {today}\n")
    
    # Add commits by type
    for commit_type, commits in commits_by_type.items():
        if not commits:
            continue
            
        section_title = COMMIT_TYPES.get(commit_type, commit_type.capitalize())
        changelog.append(f"### {section_title}\n")
        
        for commit in commits:
            changelog.append(f"- {commit['message']} ([{commit['hash'][:7]}](https://github.com/orbitrs/orbit/commit/{commit['hash']}))\n")
        
        changelog.append("\n")
    
    # Add other commits if there are any
    if other_commits:
        changelog.append("### Other Changes\n")
        for commit in other_commits:
            changelog.append(f"- {commit['message']} ([{commit['hash'][:7]}](https://github.com/orbitrs/orbit/commit/{commit['hash']}))\n")
        changelog.append("\n")
    
    return "".join(changelog)

if __name__ == "__main__":
    print(generate_changelog())
