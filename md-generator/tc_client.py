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
import requests
import logging
import json
import os
from datetime import datetime

class TechCommunityClient():
    """ TechCommunity Rest Client with caching support """


    def __init__(self, cache_file='../repos.json', cache_days=7):
        """
        Initialize the Tech Community client with caching support.

        Args:
            cache_file: Path to the repos.json file for caching
            cache_days: Number of days to consider cached data valid (default: 7)
        """
        self.logger = logging.getLogger(__name__)
        self.cache_file = cache_file
        self.cache_days = cache_days
        self.cache = self._load_cache()
        self.request_count = 0


    def _load_cache(self):
        """Load existing TC references from repos.json for caching."""
        cache = {}
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    repos = json.load(f)
                    for repo in repos:
                        url = repo.get('url')
                        tc_refs = repo.get('tc_references', [])
                        last_updated = repo.get('last_updated')
                        if url:
                            cache[url] = {
                                'tc_references': tc_refs,
                                'last_updated': last_updated,
                                'cached_at': datetime.now().isoformat()
                            }
                    self.logger.info(f'Loaded {len(cache)} cached TC references from {self.cache_file}')
            except Exception as e:
                self.logger.warning(f'Could not load cache from {self.cache_file}: {e}')
        return cache

    def _is_cache_valid(self, repo_url, repo_last_updated):
        """
        Check if cached data is still valid.

        Args:
            repo_url: The repository URL
            repo_last_updated: The last update timestamp from GitHub

        Returns:
            True if cache is valid, False otherwise
        """
        if repo_url not in self.cache:
            return False

        cached_data = self.cache[repo_url]
        cached_repo_updated = cached_data.get('last_updated')

        # If repo was updated after we cached it, cache is invalid
        if cached_repo_updated and repo_last_updated:
            if repo_last_updated > cached_repo_updated:
                self.logger.debug(f'Cache invalid for {repo_url}: repo updated since last cache')
                return False

        # Cache is valid
        return True

    def get_all_entries_for_repo(self, repo_url, repo_last_updated=None, force_refresh=False):
        """
        Get all Tech Community entries for a repository.
        Uses caching to minimize API requests.

        Args:
            repo_url: The repository URL to search for
            repo_last_updated: The last update timestamp from GitHub (optional)
            force_refresh: Force a fresh API call even if cached (default: False)

        Returns:
            List of Tech Community references or empty list
        """
        # Check cache first (unless force_refresh is True)
        if not force_refresh and self._is_cache_valid(repo_url, repo_last_updated):
            cached_refs = self.cache[repo_url]['tc_references']
            self.logger.info(f'Using cached TC references for {repo_url} ({len(cached_refs)} entries)')
            return cached_refs

        # Make API request
        return self._fetch_from_api(repo_url)

    def _fetch_from_api(self, repo_url):
        """Fetch Tech Community entries from API."""
        try:
            self.request_count += 1
            url = f'https://community.cumulocity.com/search/query?term={repo_url}'
            headers = {'Accept': 'application/json'}
            self.logger.info(f'[Request #{self.request_count}] Requesting TC articles: {url}...')
            response = requests.request("GET", url, headers=headers)
            result_list = []
            if response.status_code == 200:
                self.logger.info(f'Response from TC request: {response.status_code} - {response.text}')
                json_data = response.json()
                if 'topics' in json_data:
                    topics = json_data['topics']
                    for topic in topics:
                        slug = topic['slug']
                        topic_id = topic['id']
                        title = topic['title']
                        topic_url = f'https://community.cumulocity.com/t/{slug}/{topic_id}'
                        tech_result = {
                            'slug': slug,
                            'topic_id': topic_id,
                            'topic_url': topic_url,
                            'title': title
                        }
                        result_list.append(tech_result)
            else:
                self.logger.warning(
                      'Response from TC request: '+str(response.status_code)+'- ' + str(response.text))

            # Update cache
            self.cache[repo_url] = {
                'tc_references': result_list,
                'last_updated': datetime.now().isoformat(),
                'cached_at': datetime.now().isoformat()
            }

            return result_list
        except Exception as e:
            self.logger.error('Error on retrieving TechArticles: %s' % (str(e)))
            return []

    def get_request_count(self):
        """Get the number of API requests made in this session."""
        return self.request_count


