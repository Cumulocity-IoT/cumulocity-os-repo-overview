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
import os
from datetime import datetime
import json
import logging
import time
import utils

from github_rest_client import GitHubRestClient
from markdown_generator import MarkdownGenerator
from tc_client import TechCommunityClient

trusted_owners = ['TyrManuZ', 'reubenmiller', 'ButKor', 'janhommes', 'hnaether-sag', 'elpinjo', 'sagIoTPower',
                  'mbay-ODW']

logger = logging.getLogger(__name__)


def start():
    log_console_formatter = logging.Formatter('%(asctime)s %(threadName)s %(levelname)s %(name)s %(message)s')
    # Set default log format
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    token = os.getenv('GEN_GITHUB_TOKEN')

    gh_client = GitHubRestClient(token)
    # repos = gh_client.get_all_repos_for_org('SoftwareAG', None)
    repos = gh_client.get_all_repos_for_topic('cumulocity')
    if repos:
        logger.info(f'Number of GitHub Repos found: {len(repos)}')
        logger.info(f'Retrieving tech community articles...')
        tech_community_references = {}
        tc_client = TechCommunityClient()
        for repo in repos:
            url = repo['html_url']
            tc_references = tc_client.get_all_entries_for_repo(url)
            tech_community_references[url] = tc_references
            time.sleep(5)
        logger.info(f'Retrieving tech community articles finished!')

        store_repos_in_json_file(repos, tech_community_references)
        # gh_client.store_repos_in_json_file(repos)
        # logging.info(f'GitHub Repos found: {repos}')
        gh_client.create_forks_for_new_repos(repos)

        md_gen = MarkdownGenerator()
        md_gen.create_md_file(repos, trusted_owners, tc_references)
        md_gen.create_shortend_md_file(repos, trusted_owners)
        md_gen.convert_md_to_html()


def store_repos_in_json_file( repos, tech_community_references):
    optimized_repos = []
    for repo in repos:
        name = repo['name']
        owner = repo['owner']['login']
        desc = repo['description']
        topics = repo['topics']
        lang = repo['language']
        last_updated = repo['pushed_at']
        date_time_obj = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ')
        date_string = date_time_obj.strftime('%Y-%m-%d %H:%M:%S %Z')
        stars = repo['stargazers_count']
        full_name = repo['full_name']
        default_branch = repo['default_branch']
        url = repo['html_url']
        license = ''
        if repo['license'] is not None:
            license = repo['license']['name']
        trusted_level = utils.get_trust_level(owner, trusted_owners)
        tc_references = []
        try:
            tc_references = tech_community_references[url]
        except KeyError as e:
            logger.info(f'Could not find any TC Reference for repo {url}')
        cat_list = utils.get_cat_list(name, topics)
        optimized_repos.append({"name": name, "owner": owner, "desc": desc, "topics": topics, "lang": lang, "license": license, "last_updated": date_string, "stars": stars, "full_name": full_name, "default_branch": default_branch, "url": url, "tc_references": tc_references, "os-categories": cat_list, "trust_level": trusted_level})

    with open('../repos.json', 'w') as fp:
        json.dump(optimized_repos, fp, indent=4)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start()
