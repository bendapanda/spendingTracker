import pytest
import sys
import datetime

sys.path.insert(0, '../source')
import ui_helper

class TestGetValidDateTime:
    def test_valid_date(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: "05-01-2021")
        output = ui_helper.get_valid_datetime('test one')
        assert output == datetime.datetime(day=5, month=1, year=2021)
        