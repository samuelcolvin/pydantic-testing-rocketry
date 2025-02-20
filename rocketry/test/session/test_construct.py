
import datetime
import os
from textwrap import dedent

import pytest

from rocketry import Session
from rocketry.parse import parse_condition, parse_time
from rocketry.session import Config
from rocketry.tasks import FuncTask
from rocketry.core import Task, Scheduler, BaseCondition, BaseArgument, Parameters

def assert_default(session:Session):
    for cls in (Task, Scheduler, BaseCondition, BaseArgument, Parameters):
        assert cls.session is session


def test_empty():
    session = Session()
    session.set_as_default()
    assert session.parameters.to_dict() == {}
    assert session.returns.to_dict() == {}
    assert session.tasks == set()

    config = session.config

    assert isinstance(config, Config)
    assert not config.silence_task_prerun
    assert not config.silence_cond_check
    assert config.task_pre_exist == 'raise'
    assert config.timeout == datetime.timedelta(minutes=30)
    #assert config.task_execution == 'main'

    assert session.env is None
    assert_default(session)

def test_timeout_parse():
    session = Session(config={"timeout": 0.1})
    assert session.config.timeout == datetime.timedelta(seconds=0.1)

    session = Session(config={"timeout": "0.1 seconds"})
    assert session.config.timeout == datetime.timedelta(seconds=0.1)

    session = Session(config={"timeout": datetime.timedelta(seconds=0.1)})
    assert session.config.timeout == datetime.timedelta(seconds=0.1)