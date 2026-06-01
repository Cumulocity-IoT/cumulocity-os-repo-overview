#!/usr/bin/env python
"""
Analyze existing repos.json to identify which repos would be filtered with the new spam detection.
This helps identify potential false positives before deploying the filter.
"""

import json
import sys
sys.path.insert(0, 'md-generator')

from utils import is_spam_repo, is_cumulocity_relevant


def analyze_existing_repos():
    """Analyze repos.json to see what would be filtered"""

    try:
        with open('repos.json', 'r') as f:
            repos = json.load(f)
    except FileNotFoundError:
        print("Error: repos.json not found")
        return

    print(f"Total repositories in repos.json: {len(repos)}")
    print("=" * 80)

    spam_count = 0
    irrelevant_count = 0
    kept_count = 0

    spam_repos = []
    irrelevant_repos = []

    for repo in repos:
        # Convert to format expected by filter functions
        test_repo = {
            'name': repo['name'],
            'description': repo.get('desc'),
            'topics': repo.get('topics', []),
            'stargazers_count': repo.get('stars', 0),
            'visibility': 'public'  # All in repos.json are public
        }

        is_spam = is_spam_repo(test_repo)
        is_relevant = is_cumulocity_relevant(test_repo)

        if is_spam:
            spam_count += 1
            spam_repos.append({
                'name': repo['name'],
                'owner': repo['owner'],
                'url': repo['url'],
                'desc': repo.get('desc', 'No description'),
                'topics': repo.get('topics', []),
                'stars': repo.get('stars', 0)
            })
        elif not is_relevant:
            irrelevant_count += 1
            irrelevant_repos.append({
                'name': repo['name'],
                'owner': repo['owner'],
                'url': repo['url'],
                'desc': repo.get('desc', 'No description'),
                'topics': repo.get('topics', []),
                'stars': repo.get('stars', 0)
            })
        else:
            kept_count += 1

    print(f"\nResults:")
    print(f"  - Would be KEPT: {kept_count}")
    print(f"  - Would be FILTERED as SPAM: {spam_count}")
    print(f"  - Would be FILTERED as IRRELEVANT: {irrelevant_count}")
    print(f"  - Total filtered: {spam_count + irrelevant_count}")
    print(f"  - Percentage kept: {kept_count / len(repos) * 100:.1f}%")

    if spam_repos:
        print("\n" + "=" * 80)
        print("SPAM REPOSITORIES (would be filtered):")
        print("=" * 80)
        for repo in spam_repos[:20]:  # Show first 20
            print(f"\n  Name: {repo['name']}")
            print(f"  Owner: {repo['owner']}")
            print(f"  URL: {repo['url']}")
            print(f"  Description: {repo['desc'][:100] if repo['desc'] else 'None'}")
            print(f"  Topics: {', '.join(repo['topics'][:5]) if repo['topics'] else 'None'}")
            print(f"  Stars: {repo['stars']}")

        if len(spam_repos) > 20:
            print(f"\n  ... and {len(spam_repos) - 20} more")

    if irrelevant_repos:
        print("\n" + "=" * 80)
        print("IRRELEVANT REPOSITORIES (would be filtered):")
        print("=" * 80)
        for repo in irrelevant_repos[:10]:  # Show first 10
            print(f"\n  Name: {repo['name']}")
            print(f"  Owner: {repo['owner']}")
            print(f"  URL: {repo['url']}")
            print(f"  Description: {repo['desc'][:100] if repo['desc'] else 'None'}")
            print(f"  Topics: {', '.join(repo['topics'][:5]) if repo['topics'] else 'None'}")
            print(f"  Stars: {repo['stars']}")

        if len(irrelevant_repos) > 10:
            print(f"\n  ... and {len(irrelevant_repos) - 10} more")

    print("\n" + "=" * 80)
    print("REVIEW RECOMMENDATIONS:")
    print("=" * 80)
    print("Please review the filtered repositories above to ensure:")
    print("  1. No false positives (legitimate repos being filtered)")
    print("  2. The spam/irrelevant repos are correctly identified")
    print("\nIf you find issues, adjust the filter criteria in:")
    print("  - md-generator/utils.py -> is_spam_repo()")
    print("  - md-generator/utils.py -> is_cumulocity_relevant()")


if __name__ == '__main__':
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 15 + "EXISTING REPOS.JSON ANALYSIS" + " " * 34 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")

    analyze_existing_repos()

    print("\n" + "█" * 80 + "\n")

