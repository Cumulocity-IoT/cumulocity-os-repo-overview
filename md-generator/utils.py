#
# Copyright (c) 2022 Software AG, Darmstadt, Germany and/or its licensors
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
    if owner == 'SoftwareAG':
        trust_level = 'Official'
    elif owner in trusted_owners:
        trust_level = 'Trusted'
    return trust_level

def filter_repo_list(repos):
    filtered_list = []
    for repo in repos:
        if repo['visibility'] == 'public':
            if "cumulocity" in repo['name'] or "c8y" in repo['name'] or "cumulocity-iot" in repo[
                'topics'] or "cumulocity" in repo['topics']:
                filtered_list.append(repo)
        # filtered_list = sorted(filtered_list, key=lambda d: d['stargazers_count'], reverse=True)
    return filtered_list
