# Spam Repository Filtering & Validation

## Overview
This document describes the spam filtering and validation mechanisms implemented to ensure only relevant Cumulocity-related repositories are included in the repository overview.

## Problem Statement
The GitHub search query `cumulocity OR c8y OR "thin-edge.io" OR apama` can return spam repositories that contain these keywords but are not actually related to Cumulocity IoT. Examples of spam repos that are now filtered:
- `https://github.com/dannicarlo/etc_c8yr` - Random pattern with c8y
- `https://github.com/jungleburn/e61_c8yw` - Random pattern with c8y
- `https://github.com/estinok/c8y_g89l` - Random pattern with c8y
- `https://github.com/cdnvid18/C8YpnxFY1.mp4` - Spam file repository
- `https://github.com/anefmilto1972/c8y794k` - Random characters with c8y

**Current Statistics:** The filter removes approximately 4% of repositories (28 out of 688 in current data), keeping 96% of legitimate repositories.

Common spam patterns detected and removed:
- Random character combinations with c8y without any code (e.g., `etc_c8yr`, `e61_c8yw`, `c8y_pbe3`, `h27_c8y9`, `c8y_g89l`)
- Generic motivational text in descriptions without tech content and no programming language
- GitHub profile repositories (repo name = owner name) with "config" descriptions
- Repositories with "apama" in name/owner but not related to Apama streaming analytics product
- Empty repositories without code, topics, stars, or meaningful content

**Special Note on "Apama" filtering:**
The word "apama" can refer to:
1. **Apama Streaming Analytics** - Software AG's CEP/streaming analytics product (RELEVANT ✅)
2. **Apama Lajeado** - A sports/social organization in Brazil (NOT RELEVANT ❌)
3. Personal usernames containing "apama" (usually NOT RELEVANT ❌)

The filter distinguishes between these by checking for Apama product indicators like:
- Topics: apama, streaming-analytics, cumulocity
- Description mentions: apama, streaming analytics, correlator, EPL
- From trusted Apama contributors: ApamaCommunity, mjj29, ben-spiller, rpeach-sag
- Demo repositories explicitly marked for deletion

## Validation Criteria

### 1. Spam Detection Patterns
The spam filter is **conservative** - it only blocks obvious spam patterns to avoid false positives. The following patterns are used to identify spam repositories:

**Key Principle:** Repositories with actual code (having a programming language) are never considered spam, as they represent real development work.

#### Pattern 1: Very specific random c8y combinations
Repositories with names matching very specific patterns like:
- `<3-6 letters>_c8y<1-4 chars>` (e.g., `etc_c8yr`, `abc_c8yw`)
- `<2-4 chars with digit>_c8y<char>` (e.g., `e61_c8yw`)
- `c8y_<2-6 random chars>` (e.g., `c8y_g89l`, `c8y794k`)
- `<letter><2-3 digits>_c8y<char>` (e.g., `h27_c8y9`)

**Note:** As per the key principle above, repositories with a programming language are automatically excluded from spam detection.

**Exception:** Repositories from trusted owners (containing 'cumulocity', 'software', 'thin-edge', 'apama') are never marked as spam.

**Exception:** Repositories with 2+ stars are never marked as spam (community validation).

#### Pattern 2: Multiple numbers in short c8y names
Repositories with:
- No description AND no topics
- Short name (< 15 characters)
- Contains 2+ numbers in the name
- Contains "c8y" or "cumulocity"

Example: `c8y123`, `c8y9d` with no description/topics

#### Pattern 3: Generic/motivational descriptions
Repositories with c8y in name but only generic motivational text in description:
- Has "c8y" in name
- Has a description but no topics
- Description contains generic spam phrases like "voyage of dreams", "brilliance of life", "hold firm to your beliefs"
- Description lacks tech-related keywords (IoT, API, device, sensor, microservice, etc.)

**Tech-related keywords checked:**
IoT, Cumulocity, device, sensor, MQTT, API, agent, microservice, cloud, platform, data, monitor, application, software, code, library, SDK, client, server, integration, thin-edge, Apama, analytics, widget, dashboard, web, REST, HTTP, protocol, management, automation, edge, CLI, tool, addon, extension, plugin, fork, patch, npm, package, module, session, provider, repository, homebrew, tap, script, template, view, support, backend, frontend, Docker, Kubernetes, deployment

Example spam: `etc_c8yr` with description "Persisting in the voyage of dreams..."
Example legitimate: `go-c8y-cli-addons` with description "Addons such as views and templates to support the go-c8y-cli tool" (contains "addons", "templates", "support", "tool", "cli")

#### Pattern 4: GitHub Profile Repositories
GitHub allows users to create a special repository with the same name as their username for their profile README. These are filtered when:
- Repository name equals owner name (e.g., `apaman695/apaman695`)
- Description contains "config" or "github profile" 
- OR: Has "apama" in username but no Apama product-related content
- OR: No description, topics, or code at all

**Exception:** Profile repos with actual Apama/Cumulocity product content are kept.

Examples of spam:
- `apamashiravi1383-hash/apamashiravi1383-hash` - Profile repo, no content
- `apaman695/apaman695` - "Config files for my GitHub profile"
- `apamaster/apamaster` - Profile with "portfolio" but no Apama content

#### Pattern 5: "Apama" False Positives
Repositories with "apama" in name or owner but not related to Apama streaming analytics product:

**First Check - Technical Repository Name:**
If the repository name contains technical terms, it's likely legitimate:
- Technical indicators: example, sample, demo, plugin, connector, epl, correlator, analytics, docker, kubernetes, integration, energy, forecast, prometheus, mqtt, containers, etc.
- Example: `apama-energy-forecast-example` contains "energy", "forecast", "example" → KEPT ✅

**Second Check - Apama Product Indicators:**
- Topics: apama, streaming-analytics, cumulocity
- Description mentions: "apama", "streaming analytics", "EPL", "correlator", "cumulocity"

**Third Check - Trusted Contributors:**
Never filtered:
- ApamaCommunity
- Cumulocity-IoT (when contains apama)
- mjj29
- ben-spiller
- rpeach-sag
- yhegen

**Filtered if:**
- Generic name like just "apama" with no technical terms
- References to "Apama Lajeado" (sports organization in Brazil)
- Profile repos with "apama" in username but no Apama content
- No description, topics, or code

Examples:
- ✅ KEPT: `yhegen/apama-energy-forecast-example` - Technical name
- ✅ KEPT: `apama-epl-containers` - Technical terms
- ✅ KEPT: `apama-streaming-analytics-docker` - Technical terms
- ❌ FILTERED: `DougsSc/apama` - "Projeto implementado para atender as necessidades de gerenciamento da Apama Lajeado - RS" (Brazilian organization)
- ❌ FILTERED: `lastho0pe/apama` - Generic name, no content
- ❌ FILTERED: `apamashiravi1383-hash/apamashiravi1383-hash` - Profile repo, no content

### 2. Relevance Validation
A repository is considered Cumulocity-relevant if it meets at least one of these criteria. **This is a permissive check** - we prefer to include rather than exclude.

#### Criterion 1: Cumulocity-related topics
Has any of these topics:
- `cumulocity-iot`, `cumulocity`, `cumulocity-agent`
- `cumulocity-widget`, `cumulocity-microservice`, `cumulocity-webapp`
- `cumulocity-extension`, `thin-edge`, `apama`, `apama-analytics-builder`

#### Criterion 2: Full "cumulocity" keyword
Contains the full word "cumulocity" in repository name OR description

#### Criterion 3: thin-edge.io related
Contains any of these in name or description: `thin-edge`, `tedge`

#### Criterion 4: "c8y" in name
Has "c8y" anywhere in the repository name (permissive - if someone named their repo with c8y, it's probably relevant)

#### Criterion 5: Apama-related
Contains "apama" or "apamaster" in name or description

#### Criterion 6: Known Cumulocity-related owners
Repository owner contains: `cumulocity`, `software`, or `thin-edge`

## Implementation

### Functions

#### `is_spam_repo(repo)`
Detects spam/irrelevant repositories based on multiple criteria.
- **Returns**: `True` if the repo is likely spam
- **Location**: `md-generator/utils.py`

#### `is_cumulocity_relevant(repo)`
Checks if a repository is truly Cumulocity-relevant.
- **Returns**: `True` if the repo passes validation checks
- **Location**: `md-generator/utils.py`

#### `filter_repo_list(repos)`
Main filtering function that combines both spam detection and relevance validation.
- **Returns**: Filtered list of relevant repositories
- **Location**: `md-generator/utils.py`

### Usage
The filtering is automatically applied in `main.py`:

```python
all_repos = gh_client.get_all_repos_for_topic('cumulocity OR c8y OR "thin-edge.io" OR apama')
repos = utils.filter_repo_list(all_repos) if all_repos else None
```

## Best Practices

### For Repository Owners
To ensure your Cumulocity-related repository is properly detected:

1. **Add relevant topics** to your repository:
   - `cumulocity-iot`
   - `cumulocity` (plus specific ones like `cumulocity-agent`, `cumulocity-widget`, etc.)

2. **Write a meaningful description** that mentions:
   - "Cumulocity" (full word is better than just "c8y")
   - What the repository does
   - IoT/device management context

3. **Use clear naming**:
   - Prefer "cumulocity" over "c8y" in repo names
   - Avoid random characters/numbers unless necessary

4. **Add a README** with proper documentation

### Examples of Good Repository Metadata

✅ **Good Example 1:**
```
Name: cumulocity-devicemanagement-agent
Description: Cumulocity Reference Agent written in Python to demonstrate most of the Device Management Capabilities
Topics: cumulocity-iot, cumulocity-agent, device-management, iot
```

✅ **Good Example 2:**
```
Name: go-c8y-cli
Description: go c8y cli tool for interacting with the Cumulocity
Topics: cumulocity-iot
```

❌ **Bad Example (Spam):**
```
Name: etc_c8yr
Description: (none)
Topics: (none)
```

## Monitoring & Maintenance

### Regular Review
Periodically review the filtered repositories to ensure:
1. No false positives (legitimate repos being filtered out)
2. No false negatives (spam repos getting through)

### Adjusting Filters
If you notice patterns of spam getting through or legitimate repos being filtered:
1. Update the patterns in `is_spam_repo()`
2. Adjust validation criteria in `is_cumulocity_relevant()`
3. Document changes in this file

### Logging
Consider adding logging to track:
- Number of repos before/after filtering
- Specific repos that were filtered out
- Reasons for filtering

## Future Improvements

Potential enhancements to consider:

1. **Machine Learning**: Train a model on known good/spam repos
2. **README Analysis**: Parse README content for relevance signals
3. **Activity Metrics**: Consider commit frequency, contributor count
4. **License Check**: Verify presence of appropriate open-source licenses
5. **Code Analysis**: Check for actual Cumulocity API usage in code
6. **Allowlist/Blocklist**: Maintain lists of known good/spam repositories

## Contact

For questions or suggestions about the spam filtering mechanism, please open an issue in the repository.

## Testing

To test the spam filtering logic, run the test suite:

```bash
cd md-generator
python test_spam_filter.py
```

This will run comprehensive tests showing:
- How spam repositories are detected and filtered
- How legitimate repositories are validated and kept
- Edge cases and their handling

Example output:
```
SPAM DETECTION TESTS
Repo: etc_c8yr
  Description: None
  Is Spam: True
  Is Relevant: False
  ✓ Would be filtered: True

LEGITIMATE REPOSITORY TESTS
Repo: cumulocity-devicemanagement-agent
  Description: Cumulocity Reference Agent...
  Is Spam: False
  Is Relevant: True
  ✓ Would be kept: True
```

## Manual Testing

To test specific repositories manually:

```python
from utils import is_spam_repo, is_cumulocity_relevant

repo = {
    'name': 'your-repo-name',
    'description': 'Your repository description',
    'topics': ['topic1', 'topic2'],
    'stargazers_count': 5,
    'visibility': 'public'
}

print(f"Is Spam: {is_spam_repo(repo)}")
print(f"Is Relevant: {is_cumulocity_relevant(repo)}")
```

