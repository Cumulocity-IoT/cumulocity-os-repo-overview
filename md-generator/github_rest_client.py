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
import datetime

import requests
import logging
import time
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs


class GitHubRestClient():
    """ GitHub Rest Client """
    GITHUB_URL = 'https://api.github.com'

    def __init__(self, token):
        self.logger = logging.getLogger(__name__)
        self.token = token
        self.repo_list = []
        self.repo_count = 0
        self.rate_limit = 60
        self.org = None

    def get_auth_header(self):
        if self.token:
            return {'Authorization': self.token}

    def get_all_repos_for_org(self, org, page):
        self.org = org
        self._get_all_repos_for_org(page)
        return self.repo_list

    def _get_all_repos_for_org(self, page):
        try:
            self.repo_list = []
            if page == None:
                url = f'{self.GITHUB_URL}/orgs/{self.org}/repos?per_page=100'
            else:
                url = f'{self.GITHUB_URL}/orgs/{self.org}/repos?per_page=100&page={page}'
            headers = self.get_auth_header()
            headers['Accept'] = 'application/vnd.github.v3+json'
            response = requests.request("GET", url, headers=headers)
            self.logger.debug('Response from request: ' + str(response.text))
            self.logger.debug('Response from request with code : ' + str(response.status_code))
            if response.status_code == 200:
                json_data = response.json()
                self.logger.info('Response from request with code : ' + str(response.status_code))
                self.repo_list.extend(json_data)
                # for repo in json_data:
                #    self.repo_list.append(repo)
                while 'next' in response.links.keys():
                    response = requests.get(response.links['next']['url'], headers=headers)
                    self.repo_list.extend(response.json())
            else:
                self.logger.warning(
                    'Response from request: ' + str(response.text))
                self.logger.warning('Got response with status_code: ' +
                                    str(response.status_code))
        except Exception as e:
            self.logger.error('Error on retrieving GitHub Repos: %s' % (str(e)))
            return None

    def get_all_repos_for_topic(self, topic):
        try:
            self.repo_list = []
            url = f'{self.GITHUB_URL}/search/repositories?q={topic}&sort=stars&order=desc&per_page=100'
            headers = self.get_auth_header()
            headers['Accept'] = 'application/vnd.github.v3+json'
            response = requests.request("GET", url, headers=headers)
            self.logger.debug('Response from request: ' + str(response.text))
            self.logger.debug('Response from request with code : ' + str(response.status_code))
            if response.status_code == 200:
                json_data = response.json()
                self.logger.info('Response from request with code : ' + str(response.status_code))
                repos = json_data['items']
                self.repo_list.extend(repos)
                self.repo_count = json_data['total_count']
                # for repo in repos:
                #    self.repo_list.append(repo)
                while 'next' in response.links.keys():
                    response = requests.get(response.links['next']['url'], headers=headers)
                    response_json = response.json()
                    if response_json is not None and 'items' in response_json:
                        repos = response.json()['items']
                        self.repo_list.extend(repos)
            else:
                self.logger.warning(
                    'Response from request: ' + str(response.text))
                self.logger.warning('Got response with status_code: ' + str(response.status_code))
            return self.repo_list
        except Exception as e:
            self.logger.error('Error on retrieving GitHub Repos: %s' % (str(e)))
            return None

    def _create_fork_for_repo(self, repo):
        try:
            name = repo['name']
            owner = repo['owner']['login']
            size = int(repo['size'])
            if size > 0 and name is not None and owner is not None:
                url = f'{self.GITHUB_URL}/repos/{owner}/{name}/forks'
                headers = self.get_auth_header()
                headers['Accept'] = 'application/vnd.github.v3+json'
                # payload = {
                #    "name": name,
                #    "default_branch_only": True
                # }
                if self.rate_limit > 0:
                    self.logger.info(f'Forking the repo {owner}/{name} ... ')
                    response = requests.request("POST", url, headers=headers)
                    self.rate_limit = int(response.headers['x-RateLimit-Remaining'])
                    self.logger.info(f'Rate limit remaining: {self.rate_limit}')
                    if response.status_code == 202:
                        self.logger.info('Forking successful with status code : ' + str(response.status_code))
                    else:
                        self.logger.warning(
                            f'Error while creating fork of {owner}/{name} with status_code: {response.status_code}')

        except Exception as e:
            self.logger.error('Error on retrieving GitHub Repos: %s' % (str(e)))

    def get_all_forked_repos(self):
        try:
            existing_repos = []
            url = f'{self.GITHUB_URL}/users/cumulocity-open-source/repos?per_page=100'
            headers = self.get_auth_header()
            headers['Accept'] = 'application/vnd.github.v3+json'
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                repos = response.json()
                existing_repos.extend(repos)
                while 'next' in response.links.keys():
                    response = requests.get(response.links['next']['url'], headers=headers)
                    repos = response.json()
                    existing_repos.extend(repos)
                return existing_repos
            else:
                self.logger.warning(f'Error on retrieving GitHub Repos: {response.status_code}')
        except Exception as e:
            self.logger.error('Error on retrieving GitHub Repos: %s' % (str(e)))

    def create_forks_for_new_repos(self, repos):
        existing_repos = self.get_all_forked_repos()
        if existing_repos is not None:
            for repo in repos:
                repo_name = repo['name']
                is_fork = repo['fork']
                repo_already_forked = False
                if is_fork:
                    continue
                for existing_repo in existing_repos:
                    existing_repo_name = existing_repo['name']
                    if existing_repo_name == repo_name:
                        repo_already_forked = True
                        break
                if not repo_already_forked:
                    self._create_fork_for_repo(repo)
                    time.sleep(10)

