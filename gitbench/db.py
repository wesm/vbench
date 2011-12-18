import pandas as ps

from sqlalchemy import Table, Column, MetaData, create_engine, ForeignKey
from sqlalchemy import types as sqltypes
from sqlalchemy import sql
from sqlalchemy import exceptions as exc

from gitbench.benchmark import Benchmark

class BenchmarkDB(object):
    """
    Persist gitbench results in a sqlite3 database
    """

    def __init__(self, dbpath):
        self.dbpath = dbpath

        self._engine = create_engine('sqlite:///%s' % dbpath)
        self._metadata = MetaData()
        self._metadata.bind = self._engine

        self._benchmarks = Table('benchmarks', self._metadata,
            Column('checksum', sqltypes.String(32), primary_key=True),
            Column('name', sqltypes.String(200), nullable=False),
            Column('description', sqltypes.Text)
        )
        self._results = Table('results', self._metadata,
            Column('checksum', sqltypes.String(32),
                   ForeignKey('benchmarks.checksum'), primary_key=True),
            Column('revision', sqltypes.String(50), primary_key=True),
            Column('ncalls', sqltypes.String(50)),
            Column('timing', sqltypes.Float),
            Column('traceback', sqltypes.Text),
        )

        self._ensure_tables_created()

    # _instances = {}
    # @classmethod
    # def get_instance(cls, dbpath):
    #     if dbpath not in cls._instances:
    #         cls._instances[dbpath] = BenchmarkDB(dbpath)
    #     return cls._instances[dbpath]

    def _ensure_tables_created(self):
        self._benchmarks.create(self._engine, checkfirst=True)
        self._results.create(self._engine, checkfirst=True)

    @property
    def conn(self):
        return self._engine.connect()

    def write_benchmark(self, bm, overwrite=False):
        """

        """
        ins = self._benchmarks.insert()
        ins = ins.values(name=bm.name, checksum=bm.checksum,
                         description=bm.description)
        result = self.conn.execute(ins)

    def delete_benchmark(self, checksum):
        """

        """
        pass

    def write_result(self, checksum, revision, ncalls, timing,
                     traceback=None, overwrite=False):
        """

        """
        ins = self._results.insert()
        ins = ins.values(checksum=checksum,
                         revision=revision, ncalls=ncalls,
                         timing=timing, traceback=traceback)
        result = self.conn.execute(ins)
        print result

    def delete_result(self, checksum, revision):
        """

        """
        pass

    def get_benchmarks(self):
        stmt = sql.select([self._benchmarks])
        return list(self.conn.execute(stmt))

    def get_rev_results(self, rev):
        tab = self._results
        stmt = sql.select([tab],
                          sql.and_(tab.c.revision == rev))
        results = list(self.conn.execute(stmt))
        return dict((v.checksum, v) for v in results)

    def get_benchmark_results(self, checksum):
        """

        """
        tab = self._results
        stmt = sql.select([tab],
                          sql.and_(tab.c.bmk_checksum == checksum))
        return self.conn.execute(stmt)
