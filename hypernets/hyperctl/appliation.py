import json
import os
from pathlib import Path
from typing import Dict, Optional
import copy
import psutil
from tornado import ioloop

from hypernets import __version__ as hyn_version
from hypernets.hyperctl.batch import Batch, ShellJob
from hypernets.hyperctl.executor import create_executor_manager
from hypernets.hyperctl.scheduler import JobScheduler
from hypernets.hyperctl.server import create_batch_manage_webapp
from hypernets.hyperctl.utils import load_json, http_portal
from hypernets.utils import logging

logging.set_level('DEBUG')

logger = logging.getLogger(__name__)


class BatchApplication:

    def __init__(self, batch: Batch,
                 server_host="localhost",
                 server_port=8060,
                 scheduler_exit_on_finish=False,
                 scheduler_interval=5000,
                 backend_type='local',
                 backend_conf=None,
                 version=None,
                 **kwargs):

        self.batch = batch

        self.job_scheduler:JobScheduler = self._create_scheduler(backend_type, backend_conf,
                                                                 server_host, server_port,
                                                                 scheduler_exit_on_finish,
                                                                 scheduler_interval)
        # create http server
        self.http_server = create_batch_manage_webapp(server_host, server_port, batch, self.job_scheduler)

    def _create_scheduler(self, backend_type, backend_conf, server_host, server_port,
                          scheduler_exit_on_finish, scheduler_interval):
        executor_manager = create_executor_manager(backend_type, backend_conf, server_host, server_port)
        return JobScheduler(self.batch, scheduler_exit_on_finish, scheduler_interval, executor_manager)

    def start(self):

        logger.info(f"batches_data_path: {self.batch.batches_data_dir.absolute()}")
        logger.info(f"batch name: {self.batch.name}")

        # check jobs status
        for job in self.batch.jobs:
            if job.status != job.STATUS_INIT:
                if job.status == job.STATUS_RUNNING:
                    logger.warning(f"job '{job.name}' status is {job.status} in the begining,"
                                   f"it may have run and will not run again this time, "
                                   f"you can remove it's status file and working dir to retry the job")
                else:
                    logger.info(f"job '{job.name}' status is {job.status} means it's finished, skip to run ")
                continue

        # prepare batch data dir
        if self.batch.data_dir_path().exists():
            logger.info(f"batch {self.batch.name} already exists, run again")
        else:
            os.makedirs(self.batch.data_dir_path(), exist_ok=True)

        # write batch config
        batch_config_file_path = self.batch.config_file_path()
        batch_as_config = self.to_config()
        with open(batch_config_file_path, 'w', newline='\n') as f:
            json.dump(batch_as_config, f, indent=4)
        logger.debug(f"write config to file {batch_config_file_path}")

        # write pid file
        with open(self.batch.pid_file_path(), 'w', newline='\n') as f:
            f.write(str(os.getpid()))

        # prepare to start scheduler and web http
        self.job_scheduler.start()

        # start web server
        server_portal = http_portal(self.server_host, self.server_port)
        logger.info(f"start api server at: {server_portal}")
        self.http_server.listen(self.server_port).start()

        # run in io loop
        ioloop.IOLoop.instance().start()

    def to_config(self):
        jobs_config = []
        for job in self.batch.jobs:
            jobs_config.append(job.to_config())

        batch_as_config = {
            "jobs": jobs_config,
            "name": self.batch.name,
            "server": {
                "host": self.server_host,
                "port": self.server_port
            },
            "scheduler": {
                "interval": self.job_scheduler.interval,
                "exit_on_finish": self.job_scheduler.exit_on_finish
            },
            "version": hyn_version
        }
        return batch_as_config

    def summary_batch(self):
        batch = self.batch

        batch_summary = batch.summary()
        batch_summary['portal'] = http_portal(self.server_host, self.server_port)
        return batch_summary

    @staticmethod
    def load(batch_spec_dict: Dict, batches_data_dir):

        batch_spec_dict = copy.copy(batch_spec_dict)

        def flat_args(config_key: str):
            if config_key in batch_spec_dict:
                sub_config: Dict = batch_spec_dict.pop(config_key)
                sub_init_kwargs = {f"{config_key}_{k}": v for k, v in sub_config.items()}
                batch_spec_dict.update(sub_init_kwargs)

        batch_name = batch_spec_dict.pop('name')
        jobs_dict = batch_spec_dict.pop('jobs')

        batch = Batch(batch_name, batches_data_dir)
        for job_dict in jobs_dict:

            if job_dict.get('output_dir') is None:
                job_dict['output_dir'] = (batch.data_dir_path() / job_dict['name']).as_posix()
            if job_dict.get('working_dir') is None:
                job_dict['working_dir'] = job_dict['output_dir']
            batch.add_job(**job_dict)

        flat_args("server")
        flat_args("scheduler")
        flat_args("backend")

        # web application
        app = BatchApplication(batch, **batch_spec_dict)

        return app

    @property
    def server_host(self):
        return self.http_server.host

    @property
    def server_port(self):
        return self.http_server.port
