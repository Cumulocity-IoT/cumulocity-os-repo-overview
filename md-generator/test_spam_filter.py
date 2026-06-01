#!/usr/bin/env python3
"""
Comprehensive spam filter test suite.
Tests all spam detection patterns, legitimate repos, edge cases, logging, and special cases.
"""

import sys
import logging
sys.path.insert(0, '.')

from utils import is_spam_repo, is_cumulocity_relevant, filter_repo_list


def test_spam_patterns():
    """Test all 6 spam patterns with known examples"""
    print("=" * 80)
    print("SPAM PATTERN TESTS")
    print("=" * 80)

    spam_test_cases = [
        {
            'name': 'Pattern 1: Random C8Y Pattern',
            'repo': {
                'name': 'etc_c8yr',
                'full_name': 'dannicarlo/etc_c8yr',
                'owner': {'login': 'dannicarlo'},
                'description': 'No matter how winding the road',
                'topics': [],
                'language': None,
                'visibility': 'public',
                'stargazers_count': 0,
                'created_at': '2024-01-01T10:00:00Z',
                'pushed_at': '2024-01-01T10:00:00Z'
            }
        },
        {
            'name': 'Pattern 1: Another C8Y Pattern',
            'repo': {
                'name': 'e61_c8yw',
                'full_name': 'jungleburn/e61_c8yw',
                'owner': {'login': 'jungleburn'},
                'description': 'Voyage of dreams',
                'topics': [],
                'language': None,
                'visibility': 'public',
                'stargazers_count': 0,
                'created_at': '2024-01-01T10:00:00Z',
                'pushed_at': '2024-01-01T10:00:00Z'
            }
        },
        {
            'name': 'Pattern 2: Short name with numbers',
            'repo': {
                'name': 'c8y_g89l',
                'full_name': 'someone/c8y_g89l',
                'owner': {'login': 'someone'},
                'description': None,
                'topics': [],
                'language': None,
                'visibility': 'public',
                'stargazers_count': 0,
                'created_at': '2024-01-01T10:00:00Z',
                'pushed_at': '2024-01-01T10:00:00Z'
            }
        },
        {
            'name': 'Pattern 4: GitHub Profile Repo',
            'repo': {
                'name': 'apamashiravi1383-hash',
                'full_name': 'apamashiravi1383-hash/apamashiravi1383-hash',
                'owner': {'login': 'apamashiravi1383-hash'},
                'description': 'Config files for my GitHub profile',
                'topics': ['config'],
                'language': None,
                'visibility': 'public',
                'stargazers_count': 0,
                'created_at': '2024-01-01T10:00:00Z',
                'pushed_at': '2024-01-01T10:00:00Z'
            }
        },
        {
            'name': 'Pattern 5: False Positive Apama',
            'repo': {
                'name': 'apama_jardam',
                'full_name': 'kasymman/apama_jardam',
                'owner': {'login': 'kasymman'},
                'description': '',
                'topics': [],
                'language': None,
                'visibility': 'public',
                'stargazers_count': 0,
                'created_at': '2024-01-01T10:00:00Z',
                'pushed_at': '2024-01-01T10:00:01Z'
            }
        },
    ]

    for test_case in spam_test_cases:
        repo = test_case['repo']
        is_spam, reason = is_spam_repo(repo)
        print(f"\n{test_case['name']}: {repo['full_name']}")
        print(f"  Expected: SPAM")
        print(f"  Is Spam: {is_spam}")
        print(f"  Reason: {reason}")
        print(f"  ✅ PASS" if is_spam else f"  ❌ FAIL - Should be filtered!")


def test_legitimate_repos():
    """Test with legitimate Cumulocity repositories"""
    print("\n" + "=" * 80)
    print("LEGITIMATE REPOSITORY TESTS")
    print("=" * 80)

    legitimate_repos = [
        {
            'name': 'cumulocity-devicemanagement-agent',
            'full_name': 'SoftwareAG/cumulocity-devicemanagement-agent',
            'owner': {'login': 'SoftwareAG'},
            'description': 'Cumulocity Reference Agent written in Python to demonstrate most of the Device Management Capabilities',
            'topics': ['cumulocity-iot', 'cumulocity-agent', 'device-management'],
            'language': 'Python',
            'stargazers_count': 24,
            'visibility': 'public',
            'created_at': '2023-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z'
        },
        {
            'name': 'go-c8y-cli',
            'full_name': 'reubenmiller/go-c8y-cli',
            'owner': {'login': 'reubenmiller'},
            'description': 'go c8y cli tool for interacting with the Cumulocity',
            'topics': ['cumulocity-iot'],
            'language': 'Go',
            'stargazers_count': 48,
            'visibility': 'public',
            'created_at': '2023-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z'
        },
        {
            'name': 'thin-edge.io',
            'full_name': 'thin-edge/thin-edge.io',
            'owner': {'login': 'thin-edge'},
            'description': 'The open edge framework for lightweight IoT devices',
            'topics': ['cumulocity-iot', 'edge', 'iot'],
            'language': 'Rust',
            'stargazers_count': 285,
            'visibility': 'public',
            'created_at': '2023-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z'
        },
        {
            'name': 'c8y-decoding-event-demo',
            'full_name': 'frankyfish/c8y-decoding-event-demo',
            'owner': {'login': 'frankyfish'},
            'description': 'Remove this repo when things are done',
            'topics': [],
            'language': 'Java',
            'visibility': 'public',
            'stargazers_count': 0,
            'created_at': '2024-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T11:00:00Z'
        },
    ]

    for repo in legitimate_repos:
        is_spam, reason = is_spam_repo(repo)
        is_relevant = is_cumulocity_relevant(repo)
        print(f"\nRepo: {repo['full_name']}")
        print(f"  Description: {repo['description'][:60]}...")
        print(f"  Language: {repo.get('language', 'None')}")
        print(f"  Stars: {repo['stargazers_count']}")
        print(f"  Is Spam: {is_spam}")
        print(f"  Is Relevant: {is_relevant}")
        result = "KEPT" if (not is_spam and is_relevant) else "FILTERED"
        print(f"  ✅ {result}" if result == "KEPT" else f"  ❌ {result}")


def test_order_book_case():
    """Test the Order-book-on-apama special case"""
    print("\n" + "=" * 80)
    print("ORDER-BOOK-ON-APAMA SPECIAL CASE TESTS")
    print("=" * 80)

    # Test 1: With full description
    test_repo = {
        'name': 'Order-book-on-apama',
        'full_name': 'crazyvaskya/Order-book-on-apama',
        'owner': {'login': 'crazyvaskya'},
        'description': 'Order book simulator based on Apama streaming analytics',
        'topics': [],
        'language': None,
        'visibility': 'public',
        'stargazers_count': 0,
        'created_at': '2024-01-01T10:00:00Z',
        'pushed_at': '2024-01-01T10:04:21Z'  # 261 seconds later
    }

    print("\n  Test 1: With description (has 'apama' and 'streaming' keywords)")
    is_spam, reason = is_spam_repo(test_repo)
    print(f"    Is Spam: {is_spam}")
    print(f"    ✅ PASS" if not is_spam else f"    ❌ FAIL - Should NOT be filtered")

    # Test 2: Without description (technical name should save it)
    test_repo['description'] = ''
    print("\n  Test 2: Without description (technical name 'order-book' should save it)")
    is_spam, reason = is_spam_repo(test_repo)
    print(f"    Is Spam: {is_spam}")
    print(f"    ✅ PASS" if not is_spam else f"    ❌ FAIL - Should NOT be filtered")

    # Test 3: With topics
    test_repo['topics'] = ['apama']
    test_repo['description'] = 'Order book simulator based on Apama streaming analytics'
    print("\n  Test 3: With topics")
    is_spam, reason = is_spam_repo(test_repo)
    print(f"    Is Spam: {is_spam}")
    print(f"    ✅ PASS" if not is_spam else f"    ❌ FAIL - Should NOT be filtered")


def test_yhegen_repos():
    """Test yhegen's Apama repos (should not be filtered)"""
    print("\n" + "=" * 80)
    print("YHEGEN APAMA REPOS TESTS")
    print("=" * 80)

    yhegen_repo = {
        'name': 'apama-energy-forecast-example',
        'full_name': 'yhegen/apama-energy-forecast-example',
        'owner': {'login': 'yhegen'},
        'description': '',
        'topics': [],
        'language': None,
        'visibility': 'public',
        'stargazers_count': 0,
        'created_at': '2024-01-01T10:00:00Z',
        'pushed_at': '2024-01-01T10:00:00Z'
    }

    print(f"\nRepo: {yhegen_repo['full_name']}")
    print(f"  Note: Technical name 'energy-forecast-example' should save it")
    is_spam, reason = is_spam_repo(yhegen_repo)
    print(f"  Is Spam: {is_spam}")
    print(f"  ✅ PASS - Kept" if not is_spam else f"  ❌ FAIL - Should NOT be filtered")


def test_edge_cases():
    """Test edge cases that might be ambiguous"""
    print("\n" + "=" * 80)
    print("EDGE CASE TESTS")
    print("=" * 80)

    edge_cases = [
        {
            'name': 'c8y-test',
            'full_name': 'someone/c8y-test',
            'owner': {'login': 'someone'},
            'description': 'A test repository for Cumulocity IoT development',
            'topics': [],
            'language': None,
            'stargazers_count': 0,
            'visibility': 'public',
            'created_at': '2024-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z',
            'note': 'c8y in name, meaningful description, no topics'
        },
        {
            'name': 'my-c8y-widget',
            'full_name': 'someone/my-c8y-widget',
            'owner': {'login': 'someone'},
            'description': 'Custom widget for IoT dashboard',
            'topics': [],
            'language': None,
            'stargazers_count': 0,
            'visibility': 'public',
            'created_at': '2024-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z',
            'note': 'c8y in name, IoT mentioned, no topics'
        },
        {
            'name': 'c8y123',
            'full_name': 'someone/c8y123',
            'owner': {'login': 'someone'},
            'description': None,
            'topics': [],
            'language': None,
            'stargazers_count': 5,
            'visibility': 'public',
            'created_at': '2024-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z',
            'note': 'c8y with numbers, no description, but has 5 stars (should be kept)'
        },
        {
            'name': 'random-repo',
            'full_name': 'someone/random-repo',
            'owner': {'login': 'someone'},
            'description': 'This is about cumulocity platform development',
            'topics': [],
            'language': None,
            'stargazers_count': 0,
            'visibility': 'public',
            'created_at': '2024-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z',
            'note': 'No c8y/cumulocity in name, but in description'
        }
    ]

    for repo in edge_cases:
        is_spam, reason = is_spam_repo(repo)
        is_relevant = is_cumulocity_relevant(repo)
        result = 'KEPT' if (not is_spam and is_relevant) else 'FILTERED'
        print(f"\nRepo: {repo['full_name']}")
        print(f"  Note: {repo['note']}")
        print(f"  Description: {repo['description']}")
        print(f"  Stars: {repo['stargazers_count']}")
        print(f"  Is Spam: {is_spam}")
        print(f"  Is Relevant: {is_relevant}")
        print(f"  Result: {result}")


def test_filter_function():
    """Test the main filter_repo_list function"""
    print("\n" + "=" * 80)
    print("FILTER FUNCTION TEST")
    print("=" * 80)

    test_repos = [
        # Spam repos (should be filtered)
        {'name': 'etc_c8yr', 'full_name': 'dannicarlo/etc_c8yr', 'owner': {'login': 'dannicarlo'},
         'description': None, 'topics': [], 'language': None, 'stargazers_count': 0, 'visibility': 'public',
         'created_at': '2024-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z'},
        {'name': 'c8y_g89l', 'full_name': 'someone/c8y_g89l', 'owner': {'login': 'someone'},
         'description': '', 'topics': [], 'language': None, 'stargazers_count': 0, 'visibility': 'public',
         'created_at': '2024-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z'},

        # Legitimate repos (should be kept)
        {'name': 'cumulocity-agent', 'full_name': 'SoftwareAG/cumulocity-agent', 'owner': {'login': 'SoftwareAG'},
         'description': 'IoT agent for Cumulocity', 'topics': ['cumulocity-iot'], 'language': 'Python',
         'stargazers_count': 10, 'visibility': 'public',
         'created_at': '2023-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z'},
        {'name': 'go-c8y-cli', 'full_name': 'reubenmiller/go-c8y-cli', 'owner': {'login': 'reubenmiller'},
         'description': 'CLI tool for Cumulocity', 'topics': ['cumulocity-iot'], 'language': 'Go',
         'stargazers_count': 48, 'visibility': 'public',
         'created_at': '2023-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z'},

        # Private repo (should be filtered silently)
        {'name': 'cumulocity-private', 'full_name': 'someone/cumulocity-private', 'owner': {'login': 'someone'},
         'description': 'Private repo', 'topics': ['cumulocity-iot'], 'language': 'Python',
         'stargazers_count': 5, 'visibility': 'private',
         'created_at': '2023-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z'},
    ]

    print(f"\nTotal repos before filtering: {len(test_repos)}")
    filtered = filter_repo_list(test_repos)
    print(f"Total repos after filtering: {len(filtered)}")
    print("\nKept repositories:")
    for repo in filtered:
        print(f"  - {repo['full_name']}")

    expected = 2  # Only the 2 legitimate public repos
    if len(filtered) == expected:
        print(f"\n✅ Test passed! Expected {expected} repos, got {len(filtered)}")
    else:
        print(f"\n❌ Test failed! Expected {expected} repos, got {len(filtered)}")


def test_logging_functionality():
    """Test spam filtering with logging enabled"""
    print("\n" + "=" * 80)
    print("LOGGING FUNCTIONALITY TEST")
    print("=" * 80)

    # Configure logging for this test
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s %(name)s: %(message)s',
        force=True
    )

    test_repos = [
        # Spam repos
        {
            'name': 'etc_c8yr',
            'full_name': 'dannicarlo/etc_c8yr',
            'owner': {'login': 'dannicarlo'},
            'description': 'No matter how winding the road',
            'topics': [],
            'language': None,
            'visibility': 'public',
            'stargazers_count': 0,
            'created_at': '2024-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z'
        },
        {
            'name': 'apamashiravi1383-hash',
            'full_name': 'apamashiravi1383-hash/apamashiravi1383-hash',
            'owner': {'login': 'apamashiravi1383-hash'},
            'description': 'Config files for my GitHub profile',
            'topics': ['config'],
            'language': None,
            'visibility': 'public',
            'stargazers_count': 0,
            'created_at': '2024-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z'
        },
        # Valid repos
        {
            'name': 'apama-energy-forecast-example',
            'full_name': 'yhegen/apama-energy-forecast-example',
            'owner': {'login': 'yhegen'},
            'description': '',
            'topics': [],
            'language': None,
            'visibility': 'public',
            'stargazers_count': 0,
            'created_at': '2024-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T10:00:00Z'
        },
        {
            'name': 'c8y-decoding-event-demo',
            'full_name': 'frankyfish/c8y-decoding-event-demo',
            'owner': {'login': 'frankyfish'},
            'description': 'Remove this repo when things are done',
            'topics': [],
            'language': 'Java',
            'visibility': 'public',
            'stargazers_count': 0,
            'created_at': '2024-01-01T10:00:00Z',
            'pushed_at': '2024-01-01T11:00:00Z'
        },
    ]

    print("\nFiltering with logging enabled (you should see log messages):")
    filtered = filter_repo_list(test_repos)

    print(f"\n✅ Logging test complete - {len(filtered)} repos kept out of {len(test_repos)}")


def test_comprehensive():
    """Comprehensive test of all known spam and legitimate repos"""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE SPAM VS LEGITIMATE TEST")
    print("=" * 80)

    test_cases = [
        # SPAM REPOS
        {'name': 'etc_c8yr', 'full_name': 'dannicarlo/etc_c8yr', 'owner': {'login': 'dannicarlo'},
         'description': 'No matter how winding the road', 'topics': [], 'language': None,
         'visibility': 'public', 'stargazers_count': 0,
         'created_at': '2024-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z',
         'expected': 'FILTERED', 'category': 'SPAM'},

        {'name': 'e61_c8yw', 'full_name': 'jungleburn/e61_c8yw', 'owner': {'login': 'jungleburn'},
         'description': 'Voyage of dreams', 'topics': [], 'language': None,
         'visibility': 'public', 'stargazers_count': 0,
         'created_at': '2024-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z',
         'expected': 'FILTERED', 'category': 'SPAM'},

        {'name': 'apamashiravi1383-hash', 'full_name': 'apamashiravi1383-hash/apamashiravi1383-hash',
         'owner': {'login': 'apamashiravi1383-hash'},
         'description': 'Config files for my GitHub profile', 'topics': ['config'], 'language': None,
         'visibility': 'public', 'stargazers_count': 0,
         'created_at': '2024-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z',
         'expected': 'FILTERED', 'category': 'SPAM'},

        {'name': 'apama_jardam', 'full_name': 'kasymman/apama_jardam', 'owner': {'login': 'kasymman'},
         'description': '', 'topics': [], 'language': None,
         'visibility': 'public', 'stargazers_count': 0,
         'created_at': '2024-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:01Z',
         'expected': 'FILTERED', 'category': 'SPAM'},

        # LEGITIMATE REPOS
        {'name': 'Order-book-on-apama', 'full_name': 'crazyvaskya/Order-book-on-apama',
         'owner': {'login': 'crazyvaskya'},
         'description': 'Order book simulator based on Apama streaming analytics',
         'topics': [], 'language': None, 'visibility': 'public', 'stargazers_count': 0,
         'created_at': '2024-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:04:21Z',
         'expected': 'KEPT', 'category': 'LEGITIMATE'},

        {'name': 'apama-energy-forecast-example', 'full_name': 'yhegen/apama-energy-forecast-example',
         'owner': {'login': 'yhegen'},
         'description': '', 'topics': [], 'language': None,
         'visibility': 'public', 'stargazers_count': 0,
         'created_at': '2024-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z',
         'expected': 'KEPT', 'category': 'LEGITIMATE'},

        {'name': 'c8y-decoding-event-demo', 'full_name': 'frankyfish/c8y-decoding-event-demo',
         'owner': {'login': 'frankyfish'},
         'description': 'Remove this repo when things are done', 'topics': [], 'language': 'Java',
         'visibility': 'public', 'stargazers_count': 0,
         'created_at': '2024-01-01T10:00:00Z', 'pushed_at': '2024-01-01T11:00:00Z',
         'expected': 'KEPT', 'category': 'LEGITIMATE'},

        {'name': 'cumulocity-agent', 'full_name': 'SoftwareAG/cumulocity-agent',
         'owner': {'login': 'SoftwareAG'},
         'description': 'Official agent', 'topics': ['cumulocity-iot'], 'language': 'Python',
         'visibility': 'public', 'stargazers_count': 10,
         'created_at': '2023-01-01T10:00:00Z', 'pushed_at': '2024-01-01T10:00:00Z',
         'expected': 'KEPT', 'category': 'LEGITIMATE'},
    ]

    results = {'PASS': 0, 'FAIL': 0}

    for test in test_cases:
        is_spam, reason = is_spam_repo(test)
        actual = 'FILTERED' if is_spam else 'KEPT'
        status = '✅' if actual == test['expected'] else '❌'

        if actual == test['expected']:
            results['PASS'] += 1
        else:
            results['FAIL'] += 1

        print(f"\n{status} [{test['category']}] {test['full_name']}")
        print(f"   Expected: {test['expected']}, Actual: {actual}")
        if is_spam and reason:
            print(f"   Reason: {reason}")

    print("\n" + "=" * 80)
    print(f"RESULTS: {results['PASS']} PASS, {results['FAIL']} FAIL")
    print("=" * 80)

    if results['FAIL'] == 0:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"⚠️  {results['FAIL']} test(s) failed!")
        return False


if __name__ == '__main__':
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 15 + "COMPREHENSIVE SPAM FILTER TEST SUITE" + " " * 27 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")

    # Run all test suites
    test_spam_patterns()
    test_legitimate_repos()
    test_order_book_case()
    test_yhegen_repos()
    test_edge_cases()
    test_filter_function()
    test_logging_functionality()
    all_passed = test_comprehensive()

    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 25 + "ALL TESTS COMPLETED" + " " * 34 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")

    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)

