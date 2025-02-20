
import pytest

from rocketry.tasks.maintain import Restart
from rocketry.tasks import FuncTask
from rocketry.exc import SchedulerRestart
from rocketry.core import Scheduler
from rocketry.conditions import TaskStarted



def write_file(text):
    with open("test.txt", "a") as f:
        f.write(text)

def test_restart_raises(session):
    task = Restart()
    with pytest.raises(SchedulerRestart):
        task()

def test_scheduler_restart(tmpdir, session):

    with tmpdir.as_cwd() as old_dir:
        
        FuncTask(write_file, parameters={"text": "Started"}, on_startup=True, name="startup", execution="main", session=session)
        FuncTask(write_file, parameters={"text": "Shut"}, on_shutdown=True, name="shutdown", execution="main", session=session)

        task = Restart(session=session)

        task.force_run = True

        session.config.shut_cond = TaskStarted(task=task) == 1
        session.config.restarting = "recall"
        
        session.start()

        with open("test.txt") as f:
            cont = f.read()
        assert "StartedShutStartedShut" == cont

        records = list(map(lambda e: e.dict(exclude={'created'}), task.logger.get_records()))
        assert 1 == len([record for record in records if record["action"] == "run"])
        assert 1 == len([record for record in records if record["action"] == "success"])

# TODO: Test 