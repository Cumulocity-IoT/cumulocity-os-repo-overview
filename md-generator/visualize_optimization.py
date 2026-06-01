#!/usr/bin/env python3
"""
Visual comparison of API requests before and after optimization.
Creates a simple bar chart to show the improvement.
"""

def print_bar_chart():
    """Print a visual comparison of API requests."""

    print("=" * 80)
    print("TECH COMMUNITY API OPTIMIZATION - VISUAL COMPARISON")
    print("=" * 80)
    print()

    # Data
    total_repos = 906
    before_requests = 906
    after_requests = 20  # Typical for subsequent runs
    cache_hits = total_repos - after_requests

    # Before optimization
    print("📊 BEFORE OPTIMIZATION:")
    print("-" * 80)
    print(f"Total repositories: {total_repos}")
    print(f"API requests:       {before_requests}")
    bar_before = "█" * 90 + f" {before_requests} requests"
    print(f"  {bar_before}")
    print(f"Time required:      ~75 minutes")
    print()

    # After optimization
    print("📊 AFTER OPTIMIZATION:")
    print("-" * 80)
    print(f"Total repositories: {total_repos}")
    print(f"API requests:       {after_requests}")
    print(f"Cache hits:         {cache_hits}")
    bar_after = "█" * 2 + f" {after_requests} requests"
    bar_cache = "░" * 88 + f" {cache_hits} cache hits"
    print(f"  {bar_after}")
    print(f"  {bar_cache}")
    print(f"Time required:      ~2 minutes")
    print()

    # Improvement
    print("✨ IMPROVEMENT:")
    print("-" * 80)
    reduction = ((before_requests - after_requests) / before_requests) * 100
    time_saved = 75 - 2
    print(f"Request reduction:  {reduction:.1f}%")
    print(f"Time saved:         {time_saved} minutes per run")
    print(f"Efficiency:         {(cache_hits/total_repos*100):.1f}% cache hits")
    print()

    # Annual impact
    print("📅 ANNUAL IMPACT (Daily Runs):")
    print("-" * 80)
    requests_saved_per_run = before_requests - after_requests
    requests_saved_per_year = requests_saved_per_run * 365
    time_saved_per_year = time_saved * 365
    print(f"Requests saved:     {requests_saved_per_year:,} per year")
    print(f"Time saved:         {time_saved_per_year:,} minutes ({time_saved_per_year/60:.0f} hours)")
    print(f"Server load:        Reduced by ~{reduction:.0f}%")
    print()

    print("=" * 80)
    print()

    # Legend
    print("LEGEND:")
    print("  █ = API request (costs 5 seconds + server resources)")
    print("  ░ = Cache hit (instant, no server load)")
    print()

    # Visual timeline
    print("⏱️  EXECUTION TIME COMPARISON:")
    print("-" * 80)
    print()
    print("Before (906 API requests × 5 seconds):")
    timeline_before = "|" + "▓" * 75 + "| 75 minutes"
    print(f"  {timeline_before}")
    print()
    print("After (20 API requests × 5 seconds + 886 instant cache hits):")
    timeline_after = "|" + "▓" * 2 + "| 2 minutes"
    print(f"  {timeline_after}")
    print()

    print("=" * 80)


if __name__ == '__main__':
    print_bar_chart()

