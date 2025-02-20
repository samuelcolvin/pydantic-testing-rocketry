
import pytest
from rocketry.time.interval import (
    TimeOfDay,
    TimeOfHour,
    TimeOfMonth,
    TimeOfWeek,
    TimeOfYear
)

MS_IN_SECOND = int(1e+6)
MS_IN_MINUTE = int(1e+6 * 60)
MS_IN_HOUR   = int(1e+6 * 60 * 60)
MS_IN_DAY    = int(1e+6 * 60 * 60 * 24)

def pytest_generate_tests(metafunc):
    if metafunc.cls is not None:

        method_name = metafunc.function.__name__
        cls = metafunc.cls
        params = []
        if method_name == "test_closed":
            params = cls.scen_closed
        elif method_name == "test_open":
            return
        elif method_name == "test_open_left":
            params = cls.scen_open_left
        elif method_name == "test_open_right":
            params = cls.scen_open_right
        elif method_name == "test_time_point":
            params = cls.scen_time_point
        elif method_name == "test_value_error":
            params = cls.scen_value_error
        else:
            return
        
        argnames = [arg for arg in metafunc.fixturenames if arg in ('start', 'end', "expected_start", "expected_end", "time_point")]

        idlist = []
        argvalues = []
        argvalues = []
        for scen in params:
            idlist.append(scen.pop("id", f'{scen.get("start")}, {scen.get("end")}'))
            argvalues.append(tuple(scen[name] for name in argnames))
        metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")

class ConstructTester:

    def test_closed(self, start, end, expected_start, expected_end):
        time = self.cls(start, end)
        assert not time.is_full()
        assert expected_start == time._start
        assert expected_end == time._end

    def test_open(self):
        time = self.cls(None, None)
        assert time.is_full()
        assert 0 == time._start
        assert self.max_ms == time._end

    def test_open_left(self, end, expected_end, **kwargs):
        time = self.cls(None, end)
        assert not time.is_full()
        assert 0 == time._start
        assert expected_end == time._end

    def test_open_right(self, start, expected_start, **kwargs):
        time = self.cls(start, None)
        assert not time.is_full()
        assert expected_start == time._start
        assert self.max_ms == time._end

    def test_time_point(self, start, expected_start, expected_end, **kwargs):
        time = self.cls(start, time_point=True)
        assert not time.is_full()
        assert expected_start == time._start
        assert expected_end == time._end

        time = self.cls.at(start)
        assert not time.is_full()
        assert expected_start == time._start
        assert expected_end == time._end

    def test_value_error(self, start, end):
        with pytest.raises(ValueError):
            time = self.cls(start, end)

class TestTimeOfHour(ConstructTester):

    cls = TimeOfHour

    max_ms = MS_IN_HOUR

    scen_closed = [
        {
            "start": "15:00",
            "end": "45:00",
            "expected_start": 15 * MS_IN_MINUTE,
            "expected_end": 45 * MS_IN_MINUTE,
        },
        {
            "start": 15,
            "end": 45,
            "expected_start": 15 * MS_IN_MINUTE,
            "expected_end": 46 * MS_IN_MINUTE - 1,
        },
    ]

    scen_open_left = [
        {
            "end": "45:00",
            "expected_end": 45 * MS_IN_MINUTE
        }
    ]
    scen_open_right = [
        {
            "start": "45:00",
            "expected_start": 45 * MS_IN_MINUTE
        }
    ]
    scen_time_point = [
        {
            "start": "12:00",
            "expected_start": 12 * MS_IN_MINUTE,
            "expected_end": 13 * MS_IN_MINUTE,
        }
    ]

    scen_value_error = [
        {
            "start": 60,
            "end": None
        }
    ]

class TestTimeOfDay(ConstructTester):

    cls = TimeOfDay

    max_ms = 24 * MS_IN_HOUR

    scen_closed = [
        {
            "start": "10:00",
            "end": "12:00",
            "expected_start": 10 * MS_IN_HOUR,
            "expected_end": 12 * MS_IN_HOUR,
        },
        {
            "start": 10,
            "end": 12,
            "expected_start": 10 * MS_IN_HOUR,
            "expected_end": 13 * MS_IN_HOUR - 1,
        },
    ]

    scen_open_left = [
        {
            "end": "12:00",
            "expected_end": 12 * MS_IN_HOUR
        }
    ]
    scen_open_right = [
        {
            "start": "12:00",
            "expected_start": 12 * MS_IN_HOUR
        }
    ]
    scen_time_point = [
        {
            "start": "12:00",
            "expected_start": 12 * MS_IN_HOUR,
            "expected_end": 13 * MS_IN_HOUR,
        }
    ]
    scen_value_error = [
        {
            "start": 24,
            "end": None,
        }
    ]


class TestTimeOfWeek(ConstructTester):

    cls = TimeOfWeek

    max_ms = 7 * MS_IN_DAY

    scen_closed = [
        {
            # Spans from Tue 00:00:00 to Wed 23:59:59 999
            "start": "Tue",
            "end": "Wed",
            "expected_start": 1 * MS_IN_DAY,
            "expected_end": 3 * MS_IN_DAY - 1,
        },
        {
            # Spans from Tue 00:00:00 to Wed 23:59:59 999
            "start": "Tuesday",
            "end": "Wednesday",
            "expected_start": 1 * MS_IN_DAY,
            "expected_end": 3 * MS_IN_DAY - 1,
        },
        {
            # Spans from Tue 00:00:00 to Wed 23:59:59 999
            "start": 2,
            "end": 3,
            "expected_start": 1 * MS_IN_DAY,
            "expected_end": 3 * MS_IN_DAY - 1,
        },
    ]

    scen_open_left = [
        {
            "end": "Tue",
            "expected_end": 2 * MS_IN_DAY - 1 # Tuesday 23:59:59 ...
        }
    ]
    scen_open_right = [
        {
            "start": "Tue",
            "expected_start": 1 * MS_IN_DAY # Tuesday 00:00:00
        }
    ]
    scen_time_point = [
        {
            "start": "Tue",
            "expected_start": 1 * MS_IN_DAY,
            "expected_end": 2 * MS_IN_DAY,
        }
    ]
    scen_value_error = [
        {
            "start": 0,
            "end": None
        }
    ]


class TestTimeOfMonth(ConstructTester):

    cls = TimeOfMonth

    max_ms = 31 * MS_IN_DAY

    scen_closed = [
        {
            "start": "2.",
            "end": "3.",
            "expected_start": 1 * MS_IN_DAY,
            "expected_end": 3 * MS_IN_DAY - 1,
        },
        {
            "start": "2nd",
            "end": "4th",
            "expected_start": 1 * MS_IN_DAY,
            "expected_end": 4 * MS_IN_DAY - 1,
        },
        {
            "start": 2,
            "end": 4,
            "expected_start": 1 * MS_IN_DAY,
            "expected_end": 4 * MS_IN_DAY - 1,
        },
    ]

    scen_open_left = [
        {
            "end": "3.",
            "expected_end": 3 * MS_IN_DAY - 1 
        }
    ]
    scen_open_right = [
        {
            "start": "2.",
            "expected_start": 1 * MS_IN_DAY 
        }
    ]
    scen_time_point = [
        {
            "start": "2.",
            "expected_start": 1 * MS_IN_DAY,
            "expected_end": 2 * MS_IN_DAY,
        }
    ]
    scen_value_error = [
        {
            "start": 0,
            "end": None,
        },
        {
            "start": None,
            "end": 32,
        }
    ]

class TestTimeOfYear(ConstructTester):

    cls = TimeOfYear

    max_ms = 366 * MS_IN_DAY # Leap year has 366 days

    scen_closed = [
        {
            "start": "February",
            "end": "April",
            "expected_start": 31 * MS_IN_DAY,
            "expected_end": (31 + 29 + 31 + 30) * MS_IN_DAY - 1,
        },
        {
            "start": "Feb",
            "end": "Apr",
            "expected_start": 31 * MS_IN_DAY,
            "expected_end": (31 + 29 + 31 + 30) * MS_IN_DAY - 1,
        },
        {
            "start": 2,
            "end": 4,
            "expected_start": 31 * MS_IN_DAY,
            "expected_end": (31 + 29 + 31 + 30) * MS_IN_DAY - 1,
        },
    ]

    scen_open_left = [
        {
            "end": "Apr",
            "expected_end": (31 + 29 + 31 + 30) * MS_IN_DAY - 1 
        },
        {
            "end": "Jan",
            "expected_end": 31 * MS_IN_DAY - 1
        },
    ]
    scen_open_right = [
        {
            "start": "Apr",
            "expected_start": (31 + 29 + 31) * MS_IN_DAY 
        },
        {
            "start": "Dec",
            "expected_start": (366 - 31) * MS_IN_DAY 
        },
    ]
    scen_time_point = [
        {
            "start": "Jan",
            "expected_start": 0,
            "expected_end": 31 * MS_IN_DAY - 1,
        },
        {
            "start": "Feb",
            "expected_start": 31 * MS_IN_DAY,
            "expected_end": (31 + 29) * MS_IN_DAY - 1,
        },
        {
            "start": "Dec",
            "expected_start": (366 - 31) * MS_IN_DAY,
            "expected_end": 366 * MS_IN_DAY - 1,
        },
    ]
    scen_value_error = [
        {
            "start": 0,
            "end": None,
        },
        {
            "start": None,
            "end": 13,
        },
    ]