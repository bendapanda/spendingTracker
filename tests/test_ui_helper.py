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
    
    def test_invalid_day(self, monkeypatch, capsys):
        inputs = iter(["60-01-2023", "03-01-2023"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        ui_helper.get_valid_datetime('test two')
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "please enter date in dd-mm-yyyy\nInvalid Format, please try again.\nplease enter date in dd-mm-yyyy\n"

    def test_invalid_day_month_combo(self, monkeypatch, capsys):
        inputs = iter(["31-02-2023", "03-01-2023"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        ui_helper.get_valid_datetime('test three')
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "please enter date in dd-mm-yyyy\nInvalid Format, please try again.\nplease enter date in dd-mm-yyyy\n"

    def test_invalid_month(self, monkeypatch, capsys):
        inputs = iter(["30-20-2023", "03-01-2023"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        ui_helper.get_valid_datetime('test four')
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "please enter date in dd-mm-yyyy\nInvalid Format, please try again.\nplease enter date in dd-mm-yyyy\n"
    
    def test_invalid_format(self, monkeypatch, capsys):
        inputs = iter(["30-20-2023", "03-01-2023"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        ui_helper.get_valid_datetime('test five')
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "please enter date in dd-mm-yyyy\nInvalid Format, please try again.\nplease enter date in dd-mm-yyyy\n"

    def test_no_date(self, monkeypatch):
       monkeypatch.setattr('builtins.input', lambda _:'-')
       output = ui_helper.get_valid_datetime('test six') 
       assert output == None