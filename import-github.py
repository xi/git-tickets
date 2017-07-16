#!/usr/bin/env python3

"""Import tickets from github.

Usage:
	python3 import-github.py 'user/repo'
"""

import os
import sys
import datetime

import requests

TOKEN = None


def fetch(url):
	headers = {}
	if TOKEN:
		headers['Authorization'] = 'token %s' % TOKEN

	r = requests.get(url, headers=headers)
	r.raise_for_status()
	return r.json()


def convert_date(s):
	dt = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
	return dt.strftime('%a %b %d %H:%M:%S %Y')


def get_max_number(repo):
	issues = fetch('https://api.github.com/repos/%s/issues?count=1' % repo)
	if issues:
		return issues[0]['number']
	else:
		return 0


def fetch_issue(repo, number):
	url = 'https://api.github.com/repos/%s/issues/%i' % (repo, number)
	issue = fetch(url)

	if 'pull_request' in issue:
		issue = fetch(issue['pull_request']['url'])

	comments = []
	if issue['comments'] > 0:
		comments = fetch(issue['comments_url'])

	return issue, comments


def render_issue(issue):
	date = convert_date(issue['created_at'])
	s = 'From %s %s\n' % (issue['user']['login'], date)
	if issue.get('title'):
		s += 'Subject: %s\n' % issue['title']
		s += 'Author: %s\n' % issue['user']['login']
	if issue.get('state'):
		s += 'State: %s\n' % issue['state']
	if issue.get('labels'):
		s += 'Labels: %s\n' % ','.join(l['name'] for l in issue['labels'])
	if issue.get('assignee'):
		s += 'Assignee: %s\n' % issue['assignee']['login']
	if issue.get('head'):
		s += 'Branch: %s\n' % issue['head']['ref']
	if issue.get('body'):
		s += '\n'
		s += issue['body'].replace('\r', '').strip()
		s += '\n'
	return s


def import_issue(repo, number, force=False):
	path = str(number)

	if force or not os.path.exists(path):
		issue, comments = fetch_issue(repo, number)

		l = [render_issue(issue)]
		for comment in comments:
			l.append(render_issue(comment))

		with open(path, 'w') as fh:
			fh.write('\n\n'.join(l))

		print('wrote #%i' % number)


if __name__ == '__main__':
	repo = sys.argv[1]
	max_number = get_max_number(repo)

	for number in range(1, max_number + 1):
		import_issue(repo, number)
