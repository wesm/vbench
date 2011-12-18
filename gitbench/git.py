from dateutil import parser
import subprocess
import os
import re
import sys

import pytz

import numpy as np

from pandas import *

import gitbench.config as config

class Repo(object):

    def __init__(self):
        raise NotImplementedError

class GitRepo(Repo):
    """
    Read some basic statistics about a git repository
    """

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.git = _git_command(self.repo_path)
        (self.shas, self.messages, self.timestamps) = self._parse_commit_log()

    @property
    def commit_date(self):
        from pandas.core.datetools import normalize_date
        return self.timestamps.map(normalize_date)

    def _parse_commit_log(self):
        githist = self.git + 'log --pretty=format:\"%h %ad %s\" > githist.txt'
        os.system(githist)
        githist = open('githist.txt').read()
        os.remove('githist.txt')

        shas = []
        timestamps = []
        messages = []
        for line in githist.split('\n'):
            tokens = line.split()

            stamp = parser.parse(' '.join(tokens[1:7]))
            message = ' '.join(tokens[7:])

            shas.append(tokens[0])
            timestamps.append(stamp)
            messages.append(message)

        # to UTC for now
        timestamps = _convert_timezones(timestamps)

        shas = Series(shas, timestamps)
        messages = Series(messages, shas)
        timestamps = Series(timestamps, shas)
        return shas[::-1], messages[::-1], timestamps[::-1]

    def get_churn(self, omit_shas=None, omit_paths=None):
        churn = self.get_churn_by_file()

        if omit_paths is not None:
            churn = churn.drop(omit_paths, axis='major')

        if omit_shas is not None:
            churn = churn.drop(omit_shas, axis='minor')

        # sum files and add insertions + deletions
        by_commit = churn.sum('major').sum(1)
        by_date = by_commit.groupby(self.commit_date).sum()
        return by_date

    def get_churn_by_file(self):
        hashes = self.shas.values
        prev = hashes[0]

        insertions = {}
        deletions = {}

        for cur in hashes[1:]:
            i, d = self.diff(cur, prev)
            insertions[cur] = i
            deletions[cur] = d
            prev = cur
        return Panel({'insertions' : DataFrame(insertions),
                      'deletions' : DataFrame(deletions)},
                     minor_axis=hashes)

    def diff(self, sha, prev_sha):
        cmdline = self.git.split() + ['diff', sha, prev_sha, '--numstat']
        stdout = subprocess.Popen(cmdline, stdout=subprocess.PIPE).stdout

        stdout = stdout.read()

        insertions = {}
        deletions = {}

        for line in stdout.split('\n'):
            try:
                i, d, path = line.split('\t')
                insertions[path] = int(i)
                deletions[path] = int(d)
            except Exception: # EAFP
                pass

        # statline = stdout.split('\n')[-2]

        # match = re.match('.*\s(.*)\sinsertions.*\s(.*)\sdeletions', statline)

        # insertions = int(match.group(1))
        # deletions = int(match.group(2))
        return insertions, deletions

    def checkout(self, sha):
        pass

class BenchRepo(object):
    """
    Manage an isolated copy of a repository for benchmarking
    """
    def __init__(self, conf):
        self.conf = conf

    def switch_to_revision(self, rev):
        """
        rev: git SHA
        """
        self._checkout(rev)
        self._build()

    def _checkout(self, rev):
        pass

    def _build(self):
        pass


def _convert_timezones(stamps):
    # tz = config.TIME_ZONE
    def _convert(dt):
        offset = dt.tzinfo.utcoffset(dt)
        dt = dt.replace(tzinfo=None)
        dt = dt - offset
        return dt

    return [_convert(x) for x in stamps]

def _git_command(repo_path):
    return ('git --git-dir=%s/.git --work-tree=%s ' % (repo_path, repo_path))

def get_commit_history():
    # return TimeSeries

    rungithist()

    githist = open('githist.txt').read()
    os.remove('githist.txt')

    sha_date = []
    for line in githist.split('\n'):
        sha_date.append(line.split()[:2])

    return Series(dates, shas), hists

def get_commit_churn(sha, prev_sha):
    stdout = subprocess.Popen(['git', 'diff', sha, prev_sha, '--numstat'],
                              stdout=subprocess.PIPE).stdout
    stdout = stdout.read()

    insertions = {}
    deletions = {}

    for line in stdout.split('\n'):
        try:
            i, d, path = line.split('\t')
            insertions[path] = int(i)
            deletions[path] = int(d)
        except: # EAFP
            pass

    # statline = stdout.split('\n')[-2]
    # match = re.match('.*\s(.*)\sinsertions.*\s(.*)\sdeletions', statline)
    # insertions = int(match.group(1))
    # deletions = int(match.group(2))
    return insertions, deletions

def get_code_churn(commits):
    shas = commits.index[::-1]

    prev = shas[0]

    insertions = [np.nan]
    deletions = [np.nan]

    insertions = {}
    deletions = {}

    for cur in shas[1:]:
        i, d = get_commit_churn(cur, prev)

        insertions[cur] = i
        deletions[cur] = d

        # insertions.append(i)
        # deletions.append(d)

        prev = cur

    return Panel({'insertions' : DataFrame(insertions),
                  'deletions' : DataFrame(deletions)}, minor_axis=shas)


    # return DataFrame({'insertions' : insertions,
    #                   'deletions' : deletions}, index=shas)

if __name__ == '__main__':
    repo_path = '/home/wesm/code/pandas'
    repo = GitRepo(repo_path)
    by_commit = 5

