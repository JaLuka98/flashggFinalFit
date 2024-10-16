# coding: utf-8

"""
Law example tasks to demonstrate HTCondor workflows at CERN.

In this file, some really basic tasks are defined that can be inherited by
other tasks to receive the same features. This is usually called "framework"
and only needs to be defined once per user / group / etc.
"""


import os
import math

import luigi
import law


# the htcondor workflow implementation is part of a law contrib package
# so we need to explicitly load it
law.contrib.load("htcondor")


class Task(law.Task):
    """
    Base task that we use to force a version parameter on all inheriting tasks, and that provides
    some convenience methods to create local file and directory targets at the default data path.
    """

    version = law.Parameter()
    
    # scheduler_messages = {}


    def store_parts(self):
        return (self.__class__.__name__, self.version)

    def local_path(self, *path):
        # LAW_DATA_PATH is defined in setup.sh
        # parts = [os.getenv("ANALYSIS_PATH"), self.__class__.__name__] + [str(part) for part in path]
        parts = ("$ANALYSIS_PATH",) + self.store_parts() + path
        # print(parts)
        return os.path.join(*parts)

    def local_target(self, *path, **kwargs):
        return law.LocalFileTarget(self.local_path(*path), **kwargs)


class HTCondorWorkflow(law.htcondor.HTCondorWorkflow):
    """
    Batch systems are typically very heterogeneous by design, and so is HTCondor. Law does not aim
    to "magically" adapt to all possible HTCondor setups which would certainly end in a mess.
    Therefore we have to configure the base HTCondor workflow in law.contrib.htcondor to work with
    the CERN HTCondor environment. In most cases, like in this example, only a minimal amount of
    configuration is required.
    """

    max_runtime = law.DurationParameter(
        default=1.0,
        unit="h",
        significant=False,
        description="maximum runtime; default unit is hours; default: 1",
    )
    transfer_logs = luigi.BoolParameter(
        default=True,
        significant=False,
        description="transfer job logs to the output directory; default: True",
    )
    
    htcondor_job_kwargs_submit = {"spool": True}
    
    def htcondor_create_job_manager(self, **kwargs):
        job_manager = super().htcondor_create_job_manager(**kwargs)
        job_manager.job_grouping_submit = True
        job_manager.chunk_size_submit = 0  # all in one
        return job_manager
    
    def htcondor_output_directory(self):
        # the directory where submission meta data should be stored
        return law.LocalDirectoryTarget(self.local_path())

    def htcondor_bootstrap_file(self):
        # each job can define a bootstrap file that is executed prior to the actual job
        # configure it to be shared across jobs and rendered as part of the job itself
        bootstrap_file = law.util.rel_path(__file__, "bootstrap.sh")
        return law.JobInputFile(bootstrap_file, share=True, render_job=True)

    def htcondor_job_config(self, config, job_num, branches):
        # render_variables are rendered into all files sent with a job
        config.render_variables["analysis_path"] = os.getenv("ANALYSIS_PATH")

        # configure to run in a "el7" container
        # https://batchdocs.web.cern.ch/local/submit.html#os-selection-via-containers
        # config.custom_content.append(("MY.WantOS", "el7"))
        
        # Specify on exit hold
        config.custom_content.append(("on_exit_hold", "(ExitBySignal == True) || (ExitCode != 0)"))
        
        # Specify a periodic release mechanism
        config.custom_content.append(("periodic_release", "(NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > 600)"))

        # maximum runtime
        # config.custom_content.append(("+MaxRuntime", int(math.floor(self.max_runtime * 3600)) - 1))

        # Specify Job Flavor
        config.custom_content.append(("+JobFlavour", "\"longlunch\""))

        # the CERN htcondor setup requires a "log" config, but we can safely set it to /dev/null
        # if you are interested in the logs of the batch system itself, set a meaningful value here
        config.custom_content.append(("log", "/dev/null"))

        return config
    
    def htcondor_use_local_scheduler(self):
        return True
    
    