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
import logging
import re
import time
import utils

import markdown
from mdutils.mdutils import MdUtils
from datetime import datetime



class MarkdownGenerator():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cat_list = ['Microservice', 'Widget', 'Webapp', 'Agent', 'Example', 'Client', 'Simulator', 'Documentation',
                         'Tutorial', 'Extension', 'CLI', 'Other']
        self.mdFile = None


    def read_md_file(self):
        file = self.mdFile.read_md_file('./README.md')
        return file
    
    def convert_md_to_html(self):
        with open('../README_FULL.md', 'r', encoding="utf-8", errors="ignore") as f:
            text = f.read()
            html_header = '''
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <link href="github-markdown.css" rel="stylesheet">
    <style>
	            .markdown-body {
		            box-sizing: border-box;
		            min-width: 200px;
		            max-width: 1200px;
		            margin: 0 auto;
		            padding: 45px;
	            }
    </style>
</head>
<body>
<article class="markdown-body">
%s
</article>
</body>
</html>
            '''
            html = markdown.markdown(text, extensions=['extra', 'toc'])
            md_html = html_header % html
        with open('../index.html', 'w', encoding="utf-8", errors="ignore") as f:
            f.write(md_html)

    def create_shortend_md_file(self, repos, trusted_owners):
        self.mdFile = MdUtils(file_name='../README.md', title='Cumulocity IoT Open-Source Repository Overview')
        # mdFile.new_header(level=1, title='Cumulocity IoT Open-Source Repository Overview')

        self.mdFile.new_paragraph(
            "This Repository generates on a daily basis a table of all open-source repositories for Cumulocity-IoT. "
            "It should give a brief overview of all available IoT open-source "
            "repositories for Cumulocity IoT including additional content at TechCommunity.")
        self.mdFile.new_paragraph("Number of Open-Source Repos: **" + str(len(repos)) + "**")
        self.mdFile.new_paragraph('')
        self.mdFile.new_paragraph('Link to full & filterable overview:')
        self.mdFile.new_paragraph('>**https://open-source.c8y.io/**')
        self.mdFile.new_paragraph('')
        self.mdFile.new_paragraph('Link to old view:')
        self.mdFile.new_paragraph('https://cumulocity-iot.github.io/cumulocity-os-repo-overview/')
        self.mdFile.new_paragraph('')
        #self.mdFile.create_marker('toc')

        self.mdFile.new_header(level=1, title='10 Newest Repositories')
        self.build_newest_repos_list(repos)
        #self.mdFile.new_header(level=1, title='Open-Source Repository Overview Table')
        #list = self.build_table_list(repos, trusted_owners, small_columns=True)
        #self.mdFile.new_table(4, len(repos) + 1, list)
        #self.mdFile.new_table_of_contents(depth=2, marker='##--[toc]--##')
        self.mdFile.create_md_file()

    def create_md_file(self, repos, trusted_owners, tc_references):

        # repos = self.filter_repo_list(repos)

        self.mdFile = MdUtils(file_name='../README_FULL.md', title='Cumulocity IoT Open-Source Repository Overview')
        # mdFile.new_header(level=1, title='Cumulocity IoT Open-Source Repository Overview')

        self.mdFile.new_paragraph(
            "This Repository generates on a daily basis a table of all open-source repositories for Cumulocity-IoT. "
            "It should give a brief overview of all available IoT open-source "
            "repositories for Cumulocity IoT including additional content at TechCommunity.")
        self.mdFile.new_paragraph("Number of Open-Source Repos: **" + str(len(repos)) + "**")
        self.mdFile.new_paragraph('')
        self.mdFile.create_marker('toc')

        self.mdFile.new_header(level=1, title='10 Newest Repositories')
        self.build_newest_repos_list(repos)
        self.mdFile.new_header(level=1, title='Open-Source Repository Overview Table')
        list = self.build_table_list(repos, trusted_owners, small_columns=False)
        self.mdFile.new_table(5, len(repos) + 1, list)
        self.mdFile.new_header(level=1, title='Open-Source Repository Detail Lists')
        self.mdFile.new_header(level=2, title='All Categories')
        self.build_detail_list(repos, trusted_owners, tc_references)
        for cat in self.cat_list:
            self.mdFile.new_header(level=2, title=f'{cat}s')
            self.build_detail_list(repos, trusted_owners, cat_filter=cat)
        self.mdFile.new_table_of_contents(depth=2, marker='##--[toc]--##')
        self.mdFile.create_md_file()


    def build_newest_repos_list(self, repos):
        sorted_repos = sorted(repos, key=lambda repo: repo['created_at'], reverse=True)
        counter = 0
        for repo in sorted_repos:
            if counter < 10:
                name = repo['full_name']
                desc = repo['description']
                url = repo['html_url']
                repo_string = f'[' + name + '](' + url + ')'
                self.mdFile.new_paragraph(repo_string)
                counter = counter+1
            else:
                break

    def build_detail_list(self, repos, trusted_owners, cat_filter=None, tech_community_references=None):
        for repo in repos:
            #name = repo['name']
            name = repo['full_name']
            desc = repo['description']
            topics = repo['topics']
            cat_list = utils.get_cat_list(name, topics)
            if cat_filter != None and cat_filter not in cat_list:
                continue
            # if len(cat_list) > 0:
            #    cat = " <br> ".join(str(cat) for cat in cat_list)
            # else:
            #    cat = 'Other'
            # if len(topics) > 0:
            #    topic_string = " ".join(str(topic) for topic in topics)
            lang = repo['language']
            last_updated = repo['pushed_at']
            date_time_obj = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ')
            date_string = date_time_obj.strftime('%Y-%m-%d %H:%M:%S %Z')
            stars = repo['stargazers_count']
            full_name = repo['full_name']
            default_branch = repo['default_branch']
            url = repo['html_url']
            references_list = []
            if tech_community_references:
                tc_references = tech_community_references[url]
                for reference in tc_references:
                    reference_string = '[' + reference['title'] + '](' + reference['topic_url'] + ')'
                    references_list.append(reference_string)
            owner = repo['owner']['login']
            if owner == 'SoftwareAG' or owner == 'Cumulocity-IoT':
                relation = 'Cumulocity-Org Repo'
            elif owner in trusted_owners:
                relation = 'Trusted-Contributor Repo'
            else:
                relation = 'Open-Source Repo'

            if owner == 'SoftwareAG' or owner == 'Cumulocity-IoT':
                relation = 'Cumulocity%20Org'
                relation_badge = f'[![Generic badge](https://img.shields.io/badge/relation-{relation}-blue.svg)]()'
            elif owner in trusted_owners:
                relation = 'Trusted%20Contributor'
                relation_badge = f'[![Generic badge](https://img.shields.io/badge/relation-{relation}-green.svg)]()'
            else:
                relation = 'Open%20Source'
                relation_badge = f'[![Generic badge](https://img.shields.io/badge/relation-{relation}-yellow.svg)]()'
            # relation = 'SAG-Org Repo'
            self.mdFile.new_header(level=3, title='[' + name + '](' + url + ')')
            self.mdFile.new_paragraph(f'**Description**: {desc}')
            self.mdFile.new_paragraph(f'**Owner**: {owner}')
            category_paragraph = ""
            for cat in cat_list:
                category_paragraph = category_paragraph + f'[![Generic badge](https://img.shields.io/badge/category-{cat}-blue.svg)]() '
            self.mdFile.new_paragraph(category_paragraph, wrap_width=0)
            self.mdFile.new_paragraph(f'{relation_badge}')
            self.mdFile.new_paragraph(
                f'[![GitHub license](https://badgen.net/github/license/{full_name})]({url}/blob/{default_branch}/LICENSE)',
                wrap_width=0)
            self.mdFile.new_paragraph(
                f' [![GitHub stars](https://badgen.net/github/stars/{full_name})]({url}/stargazers)', wrap_width=0)
            self.mdFile.new_paragraph(
                f'[![GitHub latest commit](https://badgen.net/github/last-commit/{full_name}/{default_branch})]({url}/commits)',
                wrap_width=0)
            self.mdFile.new_paragraph(f'**Language**: {lang}')
            self.mdFile.new_paragraph(f'**TechCommunity References**: ')
            self.mdFile.new_list(references_list)

    def build_table_list(self, repos, trusted_owners, small_columns):
        # text_list = ['Repo Name', 'Description', 'Category', 'Topics', 'Language', 'Last Updated', 'Stars',
        #             'References', 'Relation']
        if small_columns:
            text_list = ['<div style="width:100px">Repo Name</div>', '<div style="width:300px">Description</div>',
                         '<div style="width:80px">Category</div>',
                         '<div style="width:80px">Relation</div>']
        else:
            text_list = ['Repo Name', 'Description', 'Owner',
                         'Category',
                         'Relation']
        for repo in repos:
            name = repo['name']
            #name = repo['full_name']
            #name = re.sub('(?!^)([A-Z]+)', r'-\1', name)
            name_parts = name.split('-')
            for name_part in name_parts:
                if len(name_part) > 20:
                    name = re.sub('(?!^)([A-Z]+)', r'-\1', name)
                    name.replace('--', '-')
                    if '_' in name:
                        name = name.replace('_', '-')
            desc = repo['description']
            full_name = repo['full_name']
            url = repo['html_url']
            default_branch = repo['default_branch']
            if desc and u'\xa0' in desc:
                desc = desc.replace(u'\xa0', u' ')
            if desc:
                words = desc.split(" ")
                for word in words:
                    if len(word) >= 100 and word.startswith("http"):
                        shorten_url = '[link]('+word+')'
                        desc = desc.replace(word, shorten_url)

            stars = f' [![GitHub stars](https://badgen.net/github/stars/{full_name})]({url}/stargazers)'
            last_commit = f'[![GitHub latest commit](https://badgen.net/github/last-commit/{full_name}/{default_branch})]({url}/commits)'
            if desc:
                desc = stars + ' ' + last_commit + ' <br/> ' + desc
            else:
                desc = stars + ' ' + last_commit
            topics = repo['topics']
            cat_list = utils.get_cat_list(name, topics)
            # if len(cat_list) > 0:
            #    cat = " <br> ".join(str(cat) for cat in cat_list)
            # else:
            #    cat = 'Other'
            if len(topics) > 0:
                topic_string = " ".join(str(topic) for topic in topics)
            else:
                topic_string = '-'
            # lang = repo['language']
            last_updated = repo['pushed_at']
            date_time_obj = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ')
            # date_string = date_time_obj.strftime('%Y-%m-%d %H:%M:%S %Z')
            # stars = repo['stargazers_count']
            url = repo['html_url']
            # tc_references = self.tc_client.get_all_entries_for_repo(url)
            # if tc_references:
            #    references_string = "<ul><li>" + "<li> ".join('['+reference['title']+']('+reference['topic_url']+') </li>' for reference in tc_references)
            #    references_string = references_string + "</ul>"
            # else:
            #    references_string = '-'
            owner = repo['owner']['login']
            if owner == 'Cumulocity-IoT':
                relation = 'Cumulocity%20Org'
                relation_md = 'Cumulocity Org'
                relation_badge = f'[![Generic badge](https://img.shields.io/badge/relation-{relation}-blue.svg)]()'
            elif owner in trusted_owners:
                relation = 'Trusted%20Contributor'
                relation_md = 'Trusted Contributor'
                relation_badge = f'[![Generic badge](https://img.shields.io/badge/relation-{relation}-green.svg)]()'
            else:
                relation = 'Open%20Source'
                relation_md = 'Open Source'
                relation_badge = f'[![Generic badge](https://img.shields.io/badge/relation-{relation}-yellow.svg)]()'
            # relation = 'SAG-Org Repo'
            category_paragraph = ""
            for cat in cat_list:
                category_paragraph = category_paragraph + f'[![Generic badge](https://img.shields.io/badge/category-{cat}-blue.svg)]() '
            if len(cat_list) > 0:
                cat = " <br> ".join(str(cat) for cat in cat_list)
            else:
                cat = "Other"
            if small_columns:
                text_list.extend(["[" + name + "](" + url + ")", desc, cat, relation_md])
            else:
                text_list.extend(["[" + name + "](" + url + ")", desc, owner, cat, relation_md])
        return text_list
