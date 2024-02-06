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

import requests
import logging
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs

class GitHubRestClient():
    """ GitHub Rest Client """
    GITHUB_URL = 'https://api.github.com'

    def __init__(self, token):
        self.logger = logging.Logger(__name__)
        self.token = token
        self.repo_list = []
        self.repo_count = 0
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
                #for repo in json_data:
                #    self.repo_list.append(repo)
                while 'next' in response.links.keys():
                    response=requests.get(response.links['next']['url'],headers=headers)
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
                #for repo in repos:
                #    self.repo_list.append(repo)
                while 'next' in response.links.keys():
                    response=requests.get(response.links['next']['url'],headers=headers)
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

    def create_fork_for_repo(self, repo):
        try:
            name = repo['name']
            owner = repo['owner']['login']
            if name is not None and owner is not None:
                url = f'{self.GITHUB_URL}/repos/{owner}/{name}/forks'
                headers = self.get_auth_header()
                headers['Accept'] = 'application/vnd.github.v3+json'
                #payload = {
                #    "name": name,
                #    "default_branch_only": True
                #}
                response = requests.request("POST", url, headers=headers)
                self.logger.debug('Response from request: ' + str(response.text))
                self.logger.debug('Response from request with code : ' + str(response.status_code))
                if response.status_code == 202:
                    self.logger.info('Response from request with code : ' + str(response.status_code))
                else:
                    self.logger.warning(f'Error while creating fork of {owner}/{name} with status_code: {response.status_code}')

        except Exception as e:
            self.logger.error('Error on retrieving GitHub Repos: %s' % (str(e)))