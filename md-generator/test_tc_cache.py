#!/usr/bin/env python3
#
# Copyright (c) 2024 Cumulocity GmbH, Düsseldorf, Germany and/or its licensors
#
# SPDX-License-Identifier: Apache-2.0
#
"""
Test script to demonstrate Tech Community caching optimization.
This shows how the caching mechanism reduces API requests.
"""

import logging
import json
import sys
from tc_client import TechCommunityClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


def test_tc_caching():
    """Test the TC client caching mechanism."""

    logger.info("=" * 80)
    logger.info("Tech Community Caching Test")
    logger.info("=" * 80)

    # Load some sample repos from repos.json
    try:
        with open('../repos.json', 'r') as f:
            all_repos = json.load(f)
    except FileNotFoundError:
        logger.error("repos.json not found. Please run main.py first.")
        return

    # Take first 20 repos as test sample
    test_repos = all_repos[:20]

    logger.info(f"\n📊 Testing with {len(test_repos)} repositories\n")

    # Test 1: First run (should use cache for existing repos)
    logger.info("🔍 Test 1: First run with existing cache")
    logger.info("-" * 80)

    tc_client = TechCommunityClient()

    for i, repo in enumerate(test_repos, 1):
        url = repo['url']
        last_updated = repo.get('last_updated')
        tc_refs = tc_client.get_all_entries_for_repo(url, last_updated)
        logger.info(f"  [{i}/{len(test_repos)}] {repo['full_name']}: {len(tc_refs)} TC references")

    requests_made = tc_client.get_request_count()
    cache_hits = len(test_repos) - requests_made
    cache_efficiency = (cache_hits / len(test_repos)) * 100 if len(test_repos) > 0 else 0

    logger.info("\n" + "=" * 80)
    logger.info("📈 RESULTS:")
    logger.info(f"   Total repositories checked: {len(test_repos)}")
    logger.info(f"   API requests made:          {requests_made}")
    logger.info(f"   Cache hits:                 {cache_hits}")
    logger.info(f"   Cache efficiency:           {cache_efficiency:.1f}%")
    logger.info("=" * 80)

    if cache_hits > 0:
        time_saved = cache_hits * 5  # 5 seconds per request
        logger.info(f"\n⏱️  Time saved by caching: ~{time_saved} seconds ({time_saved/60:.1f} minutes)")

    # Test 2: Force refresh
    logger.info("\n\n🔍 Test 2: Force refresh (bypassing cache)")
    logger.info("-" * 80)
    logger.info("Note: This is just for demonstration - normally you wouldn't do this!")

    tc_client2 = TechCommunityClient()
    sample_repo = test_repos[0]

    logger.info(f"Testing with: {sample_repo['full_name']}")

    # With cache
    refs1 = tc_client2.get_all_entries_for_repo(sample_repo['url'], sample_repo.get('last_updated'))
    requests1 = tc_client2.get_request_count()

    # Force refresh
    refs2 = tc_client2.get_all_entries_for_repo(sample_repo['url'], sample_repo.get('last_updated'), force_refresh=True)
    requests2 = tc_client2.get_request_count()

    logger.info(f"  First call (cached):  {requests1} API requests")
    logger.info(f"  Second call (forced): {requests2} API requests")
    logger.info(f"  Results identical:    {refs1 == refs2}")

    logger.info("\n" + "=" * 80)
    logger.info("✅ Test completed successfully!")
    logger.info("=" * 80)

    # Calculate overall potential savings
    logger.info("\n\n💡 OPTIMIZATION IMPACT:")
    logger.info("-" * 80)
    total_repos = len(all_repos)
    logger.info(f"Total repositories in repos.json: {total_repos}")

    if cache_efficiency > 0:
        potential_cache_hits = int(total_repos * (cache_efficiency / 100))
        potential_requests = total_repos - potential_cache_hits
        time_saved_total = potential_cache_hits * 5

        logger.info(f"\nWith {cache_efficiency:.1f}% cache efficiency:")
        logger.info(f"  - Expected API requests:  {potential_requests} (instead of {total_repos})")
        logger.info(f"  - Expected cache hits:    {potential_cache_hits}")
        logger.info(f"  - Time saved:             ~{time_saved_total} seconds ({time_saved_total/60:.1f} minutes)")
        logger.info(f"  - Request reduction:      {100 - (potential_requests/total_repos*100):.1f}%")

    logger.info("\n" + "=" * 80)


if __name__ == '__main__':
    test_tc_caching()

