from datetime import datetime

import gitbench.git as git
reload(git)

# repo_path = '/home/wesm/code/pandas'
# repo = git.GitRepo(repo_path)

# hists = repo.messages

# def churn_graph(repo):
#     omit_paths = [path for path in churn.major_axis
#                   if not path.endswith('.pyx') or not path.endswith('.py')]
#     omit_shas = [sha for sha in churn.minor_axis
#                  if 'LF' in hists[sha]]
#     omit_shas.append('dcf3490')

#     by_date = repo.get_churn(omit_shas=omit_shas, omit_paths=omit_paths)
#     by_date = by_date.drop([datetime(2011, 6, 10)])

#     # clean out days where I touched Cython
#     by_date = by_date[by_date < 5000]
#     return by_date

REPO_PATH = '/home/wesm/code/pandas'
TMP_DIR = '/home/wesm/tmp/gb_pandas'
BUILD = """
python setup.py build_ext --inplace
"""

repo = git.GitRepo(REPO_PATH)

burp = git.BenchRepo(REPO_PATH, TMP_DIR, BUILD)
