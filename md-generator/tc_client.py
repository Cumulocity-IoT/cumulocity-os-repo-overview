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

class TechCommunityClient():
    """ TechCommunity Rest Client """


    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all_entries_for_repo(self, repo_url):
        try:
            url = f'https://tech.forums.softwareag.com/search/query?term={repo_url}'
            headers = {'Accept': 'application/json'}
            self.logger.info(f'Requesting TC articles: {url}...')
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
                        topic_url = f'https://tech.forums.softwareag.com/t/{slug}/{topic_id}'
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
            return result_list
        except Exception as e:
            self.logger.error('Error on retrieving TechArticles: %s' % (str(e)))
            return None

