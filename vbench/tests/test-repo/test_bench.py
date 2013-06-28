#!/usr/bin/python
#emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*- 
#ex: set sts=4 ts=4 sw=4 noet:

__author__ = 'Yaroslav Halchenko'
__copyright__ = 'Copyright (c) 2013 Yaroslav Halchenko'
__license__ = 'MIT'

def test_benchmarkrunner():
    from vbench.api import BenchmarkRunner
    from suite import *
    runner = BenchmarkRunner(benchmarks, REPO_PATH, REPO_URL,
                             BUILD, DB_PATH, TMP_DIR, PREPARE,
                             clean_cmd=CLEAN,
                             run_option='all', run_order='normal',
                             start_date=START_DATE,
                             module_dependencies=DEPENDENCIES)
    runner.run()
