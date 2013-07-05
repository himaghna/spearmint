import os
import sys
import subprocess
import tempfile

from google.protobuf import text_format
from spearmint_pb2   import *


def log(msg):
    '''Write a msg to stderr.'''
    sys.stderr.write(msg)


def sh(cmd):
    '''Run a shell command (blocking until completion).'''
    subprocess.check_call(cmd, shell=True)


def redirect_output(path):
    '''Redirect stdout and stderr to a file.'''
    outfile    = open(path, 'w')
    sys.stdout = outfile
    sys.stderr = outfile


def check_dir(path):
    '''Create a directory if it doesn't exist.'''
    if not os.path.exists(path):
        os.mkdir(path)


def job_file_for(job):
    '''Get the path to the job file corresponding to a job object.'''
    return os.path.join(job.expt_dir, 'jobs', '%08d.pb' % (job.id))


def grid_for(job):
    return os.path.join(job.expt_dir, 'expt-grid.pkl')


def job_output_file(job):
    return os.path.join(job.expt_dir, 'output', '%08d.out' % (job.id))


def save_expt(filename, expt):
    fh = tempfile.NamedTemporaryFile(mode='w', delete=False)
    fh.write(text_format.MessageToString(expt))
    fh.close()
    cmd = 'mv "%s" "%s"' % (fh.name, filename)
    sh(cmd)


def load_expt(filename):
    fh = open(filename, 'rb')
    expt = Experiment()
    text_format.Merge(fh.read(), expt)
    fh.close()
    return expt


def save_job(job):
    fh = tempfile.NamedTemporaryFile(mode='w', delete=False)
    fh.write(job.SerializeToString())
    fh.close()

    job_file = job_file_for(job)
    cmd = 'mv "%s" "%s"' % (fh.name, job_file)
    sh(cmd)


def load_job(filename):
    fh = open(filename, 'rb')
    job = Job()
    job.ParseFromString(fh.read())
    fh.close()
    return job


