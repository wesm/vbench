import cPickle as pickle
import os

from gitbench.git import GitRepo, BenchRepo
from gitbench.db import BenchmarkDB

from datetime import datetime

class BenchmarkRunner(object):
    """

    Parameters
    ----------
    benchmarks : list of Benchmark objects
    repo_path
    build_cmd
    db_path
    run_option : {'eod', 'all', integer}
        eod: use the last revision for each calendar day
        all: benchmark every revision
        some integer N: run each N revisions
    overwrite : boolean
    """

    def __init__(self, benchmarks, repo_path, build_cmd, db_path, tmp_dir,
                 run_option='end_of_day', start_date=None,
                 overwrite=False):

        self.benchmarks = benchmarks
        self.checksums = [b.checksum for b in benchmarks]

        self.start_date = start_date
        self.run_option = run_option

        self.repo_path = repo_path
        self.db_path = db_path

        self.repo = GitRepo(self.repo_path)
        self.db = BenchmarkDB(db_path)

        # where to copy the repo
        self.tmp_dir = tmp_dir
        self.bench_repo = BenchRepo(self.tmp_dir)

    def run(self):
        revisions = self._get_revisions_to_run()

        for rev in revisions:
            results = self._run_revision(rev)

            for checksum, timing in results.iteritems():
                self.db.write_result(checksum, revision,
                                     timing.get('loops'),
                                     timing.get('timing'),
                                     timing.get('traceback'))

    def _register_benchmarks(self):
        db_checksums = set(v.checksum for v in self.db.get_benchmarks())
        for bm in self.benchmarks:
            if bm.checksum in db_checksums:
                continue
            print 'Writing new benchmark %s, %s' % (bm.name, bm.checksum)
            self.db.write_benchmark(bm)

    def _run_revision(self, rev):
        existing_results = self.db.get_rev_results(rev)
        need_to_run = [b for b in self.benchmarks
                       if b.checksum not in existing_results]

        if not need_to_run:
            print 'No benchmarks need running at %s' % rev
            return []

        print 'Running %d benchmarks for revision %s' % (len(need_to_run), rev)

        self._prepare_code(rev)

        pickle_path = pjoin(self.tmp_dir, 'benchmarks.pickle')
        results_path = pjoin(self.tmp_dir, 'results.pickle')
        if os.path.exists(results_path):
            os.remove(results_path)
        pickle.dump(need_to_run, open(pickle_path, 'w'))

        _run_benchmark_subproc(pickle_path, results_path)

        results = pickle.load(open(results_path, 'r'))
        os.remove(pickle_path)

        return results

    def _get_revisions_to_run(self):

        # TODO generalize someday to other vcs...git only for now

        rev_by_timestamp = self.repo.shas

        # assume they're in order, but check for now
        assert(rev_by_timestamp.index.is_monotonic)
        if self.start_date is not None:
            rev_by_timestamp = rev_by_timestamp.ix[self.start_date:]

        if self.run_option == 'eod':
            grouped = rev_by_timestamp.groupby(datetime.date)
            revs_to_run = grouped.apply(lambda x: x[-1]).values
        elif self.run_option == 'all':
            revs_to_run = rev_by_timestamp.values
        elif isinstance(self.run_option, int):
            revs_to_run = rev_by_timestamp.values[::self.run_option]
        else:
            raise Exception('unrecognized run_method %s' % self.run_method)

        return revs_to_run

    def _prepare_code(self, rev):
        self.bench_repo.checkout(rev)
        self.bench_repo.build()

def _run_benchmark_subproc(input_path, result_path):
    from subprocess import Popen, PIPE


