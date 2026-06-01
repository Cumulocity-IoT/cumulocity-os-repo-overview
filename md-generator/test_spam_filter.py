#!/usr/bin/env python
"""
Test script for spam filtering functionality.
Demonstrates how the spam filter handles various repository patterns.
"""

import sys
sys.path.insert(0, '.')

from utils import is_spam_repo, is_cumulocity_relevant, filter_repo_list


def test_spam_detection():
    """Test spam detection with known spam patterns"""
    print("=" * 80)
    print("SPAM DETECTION TESTS")
    print("=" * 80)

    # Test cases based on real spam examples
    spam_repos = [
        {
            'name': 'etc_c8yr',
            'description': None,
            'topics': [],
            'stargazers_count': 0,
            'visibility': 'public'
        },
        {
            'name': 'e61_c8yw',
            'description': '',
            'topics': [],
            'stargazers_count': 0,
            'visibility': 'public'
        },
        {
            'name': 'c8y_g89l',
            'description': None,
            'topics': [],
            'stargazers_count': 0,
            'visibility': 'public'
        },
        {
            'name': 'abc123_c8y',
            'description': 'test',
            'topics': [],
            'stargazers_count': 0,
            'visibility': 'public'
        }
    ]

    for repo in spam_repos:
        is_spam = is_spam_repo(repo)
        is_relevant = is_cumulocity_relevant(repo)
        print(f"\nRepo: {repo['name']}")
        print(f"  Description: {repo['description']}")
        print(f"  Is Spam: {is_spam}")
        print(f"  Is Relevant: {is_relevant}")
        print(f"  ✓ Would be filtered: {is_spam or not is_relevant}")


def test_legitimate_repos():
    """Test with legitimate Cumulocity repositories"""
    print("\n" + "=" * 80)
    print("LEGITIMATE REPOSITORY TESTS")
    print("=" * 80)

    legitimate_repos = [
        {
            'name': 'cumulocity-devicemanagement-agent',
            'description': 'Cumulocity Reference Agent written in Python to demonstrate most of the Device Management Capabilities',
            'topics': ['cumulocity-iot', 'cumulocity-agent', 'device-management'],
            'stargazers_count': 24,
            'visibility': 'public'
        },
        {
            'name': 'go-c8y-cli',
            'description': 'go c8y cli tool for interacting with the Cumulocity',
            'topics': ['cumulocity-iot'],
            'stargazers_count': 48,
            'visibility': 'public'
        },
        {
            'name': 'thin-edge.io',
            'description': 'The open edge framework for lightweight IoT devices',
            'topics': ['cumulocity-iot', 'edge', 'iot'],
            'stargazers_count': 285,
            'visibility': 'public'
        },
        {
            'name': 'apama-log-analyzer',
            'description': 'Python 3 script for analyzing Apama correlator log files',
            'topics': ['apama', 'cumulocity-iot'],
            'stargazers_count': 13,
            'visibility': 'public'
        },
        {
            'name': 'c8yMQTT',
            'description': 'Python3 Cumulocity Agent implementation for MQTT and Raspberry PI',
            'topics': ['cumulocity-iot', 'cumulocity-agent', 'mqtt'],
            'stargazers_count': 13,
            'visibility': 'public'
        }
    ]

    for repo in legitimate_repos:
        is_spam = is_spam_repo(repo)
        is_relevant = is_cumulocity_relevant(repo)
        print(f"\nRepo: {repo['name']}")
        print(f"  Description: {repo['description'][:60]}...")
        print(f"  Topics: {', '.join(repo['topics'][:3])}")
        print(f"  Stars: {repo['stargazers_count']}")
        print(f"  Is Spam: {is_spam}")
        print(f"  Is Relevant: {is_relevant}")
        print(f"  ✓ Would be kept: {not is_spam and is_relevant}")


def test_edge_cases():
    """Test edge cases that might be ambiguous"""
    print("\n" + "=" * 80)
    print("EDGE CASE TESTS")
    print("=" * 80)

    edge_cases = [
        {
            'name': 'c8y-test',
            'description': 'A test repository for Cumulocity IoT development',
            'topics': [],
            'stargazers_count': 0,
            'visibility': 'public',
            'note': 'c8y in name, meaningful description, no topics'
        },
        {
            'name': 'my-c8y-widget',
            'description': 'Custom widget for IoT dashboard',
            'topics': [],
            'stargazers_count': 0,
            'visibility': 'public',
            'note': 'c8y in name, IoT mentioned, no topics'
        },
        {
            'name': 'c8y123',
            'description': None,
            'topics': [],
            'stargazers_count': 5,
            'visibility': 'public',
            'note': 'c8y with numbers, no description, but has stars'
        },
        {
            'name': 'random-repo',
            'description': 'This is about cumulocity platform development',
            'topics': [],
            'stargazers_count': 0,
            'visibility': 'public',
            'note': 'No c8y/cumulocity in name, but in description'
        }
    ]

    for repo in edge_cases:
        is_spam = is_spam_repo(repo)
        is_relevant = is_cumulocity_relevant(repo)
        print(f"\nRepo: {repo['name']}")
        print(f"  Note: {repo['note']}")
        print(f"  Description: {repo['description']}")
        print(f"  Stars: {repo['stargazers_count']}")
        print(f"  Is Spam: {is_spam}")
        print(f"  Is Relevant: {is_relevant}")
        print(f"  Result: {'KEPT' if (not is_spam and is_relevant) else 'FILTERED'}")


def test_filter_function():
    """Test the main filter_repo_list function"""
    print("\n" + "=" * 80)
    print("FILTER FUNCTION TEST")
    print("=" * 80)

    test_repos = [
        # Spam repos
        {'name': 'etc_c8yr', 'description': None, 'topics': [], 'stargazers_count': 0, 'visibility': 'public'},
        {'name': 'c8y_g89l', 'description': '', 'topics': [], 'stargazers_count': 0, 'visibility': 'public'},
        # Legitimate repos
        {'name': 'cumulocity-agent', 'description': 'IoT agent for Cumulocity', 'topics': ['cumulocity-iot'], 'stargazers_count': 10, 'visibility': 'public'},
        {'name': 'go-c8y-cli', 'description': 'CLI tool for Cumulocity', 'topics': ['cumulocity-iot'], 'stargazers_count': 48, 'visibility': 'public'},
        # Private repo (should be filtered)
        {'name': 'cumulocity-private', 'description': 'Private repo', 'topics': ['cumulocity-iot'], 'stargazers_count': 5, 'visibility': 'private'},
    ]

    print(f"\nTotal repos before filtering: {len(test_repos)}")
    filtered = filter_repo_list(test_repos)
    print(f"Total repos after filtering: {len(filtered)}")
    print("\nKept repositories:")
    for repo in filtered:
        print(f"  - {repo['name']}")

    expected = 2  # Only the 2 legitimate public repos
    if len(filtered) == expected:
        print(f"\n✓ Test passed! Expected {expected} repos, got {len(filtered)}")
    else:
        print(f"\n✗ Test failed! Expected {expected} repos, got {len(filtered)}")


if __name__ == '__main__':
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "SPAM FILTER TEST SUITE" + " " * 37 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")

    test_spam_detection()
    test_legitimate_repos()
    test_edge_cases()
    test_filter_function()

    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 25 + "TESTS COMPLETED" + " " * 38 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")

