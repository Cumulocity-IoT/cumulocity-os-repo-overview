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

import logging

import os
from github_rest_client import GitHubRestClient
from markdown_generator import MarkdownGenerator

def start():
    token = os.getenv('GEN_GITHUB_TOKEN')

    gh_client = GitHubRestClient(token)
    repos = gh_client.get_all_repos_for_org('SoftwareAG', None)
    repos = gh_client.get_all_repos_for_topic('cumulocity-iot')
    logging.info(f'GitHub Repos in Org: {repos}')
    md_gen = MarkdownGenerator()
    md_gen.create_md_file(repos)

if __name__ == '__main__':
    start()