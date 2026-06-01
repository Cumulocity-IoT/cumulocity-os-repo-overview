#
# Copyright (c) 2024 Cumulocity GmbH, Düsseldorf, Germany and/or its licensors
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

""" Defining all Categories of Open-Source repos based on the name and topcis of a repo """
def get_cat_list(name, topics):
    cat_list = []
    if 'cumulocity-microservice' in topics or 'microservice' in name or 'microservice' in topics:
        cat = 'Microservice'
        cat_list.append(cat)
    if 'cumulocity-widget' in topics or 'widget' in name or 'widget' in topics or 'widgets' in topics:
        cat = 'Widget'
        cat_list.append(cat)
    if 'cumulocity-webapp' in name or 'cumulocity-webapp' in topics or 'webapp' in name or 'webapp' in topics:
        cat = 'WebApp'
        cat_list.append(cat)
    if 'cumulocity-agent' in name or 'cumulocity-agent' in topics or 'agent' in name or 'agent' in topics:
        cat = 'Agent'
        cat_list.append(cat)
    if 'cumulocity-example' in topics or 'example' in name or 'example' in topics:
        cat = 'Example'
        cat_list.append(cat)
    if 'cumulocity-client' in topics or 'client' in name or 'api' in name or 'api' in topics:
        cat = 'Client'
        cat_list.append(cat)
    if 'cumulocity-simulator' in topics or 'simulator' in name or 'simulator' in topics:
        cat = 'Simulator'
        cat_list.append(cat)
    if 'cumulocity-documentation' in topics or 'docs' in name or 'documentation' in topics:
        cat = 'Documentation'
        cat_list.append(cat)
    if 'cumulocity-tutorial' in topics or 'tutorial' in name or 'tutorial' in topics:
        cat = 'Tutorial'
        cat_list.append(cat)
    if 'cumulocity-extension' in topics or 'extension' in topics or 'remote-access' in name or 'remote-access' in topics:
        cat = 'Extension'
        cat_list.append(cat)
    if 'cli' in name or 'cumulocity-cli' in name or 'cumulocity-cli' in topics or 'cli' in topics:
        cat = 'CLI'
        cat_list.append(cat)
    if 'cumulocity-package' in topics:
        cat = 'UI Plugin'
        cat_list.append(cat)
    if 'cumulocity-blueprint' in topics:
        cat = 'Blueprint'
        cat_list.append(cat)
    if 'streaming-analytics' in name or 'apama' in name or 'apama-analytics-builder' in topics or 'apama' in topics:
        cat = 'Streaming Analytics'
        cat_list.append(cat)
    if len(cat_list) == 0:
        cat_list.append('Other')
    return cat_list

def get_trust_level(owner, trusted_owners):
    trust_level = "Unofficial"
    if owner == 'SoftwareAG' or owner == 'Cumulocity-IoT':
        trust_level = 'Official'
    elif owner in trusted_owners:
        trust_level = 'Trusted'
    return trust_level

def is_spam_repo(repo):
    """
    Detect spam/irrelevant repositories based on multiple criteria.
    Returns True if the repo is likely spam.
    
    This is a conservative filter - only blocks obvious spam patterns.
    """
    import re
    
    name = repo.get('name', '').lower()
    desc = repo.get('description', '') or ''
    desc_lower = desc.lower()
    topics = repo.get('topics', [])
    owner = repo.get('owner', {}).get('login', '') if isinstance(repo.get('owner'), dict) else repo.get('owner', '')
    stars = repo.get('stargazers_count', 0)
    language = repo.get('language') or repo.get('lang')
    
    # Exception: Official/Trusted owners are never spam
    trusted_patterns = ['cumulocity', 'software', 'thin-edge', 'apamacommunity']
    if owner and any(pattern in owner.lower() for pattern in trusted_patterns):
        return False
    
    # Exception: Repos with a programming language have actual code, so not spam
    # UNLESS it's a profile repo (repo name = owner name)
    if language and name != owner.lower():
        return False
    
    # Exception: Repos with stars are likely legitimate (community validation)
    if stars >= 2:
        return False
    
    # Spam pattern: GitHub profile repos (repo name = owner name)
    # These are usually just README profile pages, not actual projects
    if name == owner.lower():
        # Profile repos often have "config" in description or topics
        if 'config' in desc_lower or 'config' in str(topics).lower():
            return True
        # Profile repos with "apama" in username but no Apama-related content
        if 'apama' in owner.lower():
            has_apama_content = (
                'apama' in desc_lower or
                'streaming analytics' in desc_lower or
                'cumulocity' in desc_lower or
                any('apama' in t for t in topics)
            )
            if not has_apama_content:
                return True
        # Profile repo with no content at all
        if not desc and not topics and not language:
            return True

    # Spam pattern: "apama" in name but not related to Apama product
    if 'apama' in name or 'apama' in owner.lower():
        # Exception: Known good Apama contributors
        trusted_apama_users = ['apamacommunity', 'mjj29', 'ben-spiller', 'rpeach-sag', 'yhegen']
        if owner.lower() in trusted_apama_users:
            return False
        
        # Check if repo name itself is descriptive/technical (indicates real project)
        # Examples: apama-energy-forecast-example, apama-streaming-analytics-*, apama-epl-*
        technical_name_indicators = [
            'example', 'sample', 'demo', 'tutorial', 'guide',
            'plugin', 'connector', 'transport', 'codec', 'block',
            'epl', 'correlator', 'analytics', 'builder', 'streaming',
            'integration', 'docker', 'kubernetes', 'connectivity',
            'energy', 'forecast', 'prometheus', 'grafana', 'mqtt',
            'containers', 'test', 'template', 'framework', 'library'
        ]
        
        # If repo name contains technical indicators beyond just "apama", likely legitimate
        name_parts = name.replace('-', ' ').replace('_', ' ').lower().split()
        technical_parts = [part for part in name_parts if part in technical_name_indicators]
        if len(technical_parts) >= 1:  # At least 1 technical term
            return False
        
        # Check if repo is actually about Apama product
        apama_indicators = [
            'apama' in desc_lower,
            'streaming analytics' in desc_lower,
            'cumulocity' in desc_lower,
            'correlator' in desc_lower,
            'epl' in desc_lower,
            any('apama' in str(t).lower() for t in topics),
            any('cumulocity' in str(t).lower() for t in topics)
        ]
        
        # Apama Lajeado is a place in Brazil, not the product
        if 'lajeado' in desc_lower:
            return True
        
        # If no Apama product indicators and no content, probably spam
        if not any(apama_indicators) and not desc and not topics and not language:
            return True

    # Helper function to check if description is tech/IoT/Cumulocity-related
    def has_relevant_description(description):
        if not description or len(description) < 10:
            return False
        desc_low = description.lower()
        
        # Check for tech/IoT keywords
        tech_keywords = [
            'iot', 'cumulocity', 'device', 'sensor', 'mqtt', 'api', 'agent',
            'microservice', 'cloud', 'platform', 'data', 'monitor', 'application',
            'software', 'code', 'library', 'sdk', 'client', 'server', 'integration',
            'thin-edge', 'apama', 'analytics', 'widget', 'dashboard', 'web',
            'rest', 'http', 'protocol', 'management', 'automation', 'edge',
            'cli', 'tool', 'addon', 'extension', 'plugin', 'fork', 'patch',
            'npm', 'package', 'module', 'session', 'provider', 'repository',
            'homebrew', 'tap', 'script', 'template', 'view', 'support',
            'backend', 'frontend', 'docker', 'kubernetes', 'deployment'
        ]
        
        # If description contains any tech keywords, it's likely relevant
        if any(keyword in desc_low for keyword in tech_keywords):
            return True
            
        # Check for generic spam phrases (motivational/generic text)
        spam_phrases = [
            'voyage of dreams', 'creating your own legend', 'brilliance of life',
            'hold firm to your beliefs', 'bright', 'future', 'accumulates wealth',
            'winding the road', 'brilliant tomorrow', 'fearless journey',
            'every wave braved', 'every effort', 'no matter how'
        ]
        
        # If it contains spam phrases and no tech keywords, probably spam
        spam_phrase_count = sum(1 for phrase in spam_phrases if phrase in desc_low)
        if spam_phrase_count >= 2:
            return False
            
        return False  # No tech keywords found
    
    # Spam pattern 1: Random prefix/suffix with c8y pattern (e.g., etc_c8yr, e61_c8yw, c8y_g89l)
    # These are very specific spam patterns
    spam_name_patterns = [
        r'^[a-z]{3,6}_c8y[a-z0-9]{1,4}$',  # etc_c8yr, abc_c8yw
        r'^[a-z0-9]{2,4}_c8y[a-z]{0,2}$',  # e61_c8yw
        r'^c8y_[a-z0-9]{2,6}$',             # c8y_g89l (but not c8y_something_meaningful)
        r'^[a-z][0-9]{2,3}_c8y[a-z0-9]$'   # h27_c8y9
    ]
    
    for pattern in spam_name_patterns:
        if re.match(pattern, name):
            # If it has topics, likely legitimate
            if topics:
                return False
            # Check if description is actually tech-related
            if desc and has_relevant_description(desc):
                return False
            # Clear spam: matches pattern AND (no content OR irrelevant content)
            return True
    
    # Spam pattern 2: No description, no topics, suspicious short name with numbers
    if not desc and not topics and len(name) < 15:
        # Count how many numbers in the name
        num_count = sum(1 for c in name if c.isdigit())
        # If more than 2 numbers in a short name with c8y, likely spam
        if num_count >= 2 and ('c8y' in name or 'cumulocity' in name):
            return True
    
    # Spam pattern 3: Generic description with suspicious name
    # Repos with c8y in name but only generic motivational text
    if 'c8y' in name and desc and not topics:
        if not has_relevant_description(desc):
            return True
        
    return False


def is_cumulocity_relevant(repo):
    """
    Check if a repository is truly Cumulocity-relevant.
    Returns True if the repo passes validation checks.

    This is a permissive check - we want to include rather than exclude.
    """
    name = repo.get('name', '').lower()
    desc = repo.get('description', '') or ''
    desc_lower = desc.lower()
    topics = repo.get('topics', [])
    owner = repo.get('owner', {}).get('login', '') if isinstance(repo.get('owner'), dict) else repo.get('owner', '')

    # Criteria 1: Has Cumulocity-related topics (strong indicator)
    cumulocity_topics = ['cumulocity-iot', 'cumulocity', 'cumulocity-agent',
                         'cumulocity-widget', 'cumulocity-microservice',
                         'cumulocity-webapp', 'cumulocity-extension',
                         'thin-edge', 'apama', 'apama-analytics-builder']

    if any(topic in topics for topic in cumulocity_topics):
        return True

    # Criteria 2: Full word "cumulocity" in name or description
    if 'cumulocity' in name or 'cumulocity' in desc_lower:
        return True

    # Criteria 3: thin-edge or tedge (related to thin-edge.io)
    if 'thin-edge' in name or 'tedge' in name or 'thin-edge' in desc_lower:
        return True

    # Criteria 4: "c8y" in name (be permissive)
    # If someone named their repo with c8y, it's probably relevant
    if 'c8y' in name:
        return True

    # Criteria 5: Apama-related
    if 'apama' in name or 'apama' in desc_lower or 'apamaster' in name:
        return True

    # Criteria 6: From known Cumulocity-related owners
    trusted_owner_patterns = ['cumulocity', 'software', 'thin-edge']
    if owner and any(pattern in owner.lower() for pattern in trusted_owner_patterns):
        return True

    return False


def filter_repo_list(repos):
    """
    Filter repository list to include only public, Cumulocity-relevant repositories
    while excluding spam/irrelevant repos.
    """
    filtered_list = []
    for repo in repos:
        if repo.get('visibility') == 'public':
            # First check: basic relevance
            if "cumulocity" in repo['name'] or "c8y" in repo['name'] or \
               "cumulocity-iot" in repo['topics'] or "cumulocity" in repo['topics'] or \
               "thin-edge" in repo['name'] or "apama" in repo['name']:

                # Second check: exclude spam
                if is_spam_repo(repo):
                    continue

                # Third check: validate relevance
                if is_cumulocity_relevant(repo):
                    filtered_list.append(repo)

    return filtered_list
