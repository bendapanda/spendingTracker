"""Module to run the tests for the user_interface module

    Author: Ben Shirley
    Date: 29 Oct 2023

    
"""
import pytest
import sys
sys.path.insert(0, '../source')
import user_interface
import pandas as pd

class TestGetUserFile:
    """
    class that runs the tests for getting a valid user file
    """
    valid_file = "../data/transactions.csv"
    invalid_extension = "../data/transactions.csw"
    non_existant_file = "../data/not_real.csv"
    def test_valid_file(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: self.valid_file)
        data, status = user_interface.get_user_file()
        assert type(data) == pd.DataFrame
    def test_invalid_extension(self, monkeypatch, capsys):
        inputs = iter([self.invalid_extension, self.valid_file])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        user_interface.get_user_file()
        outputs = capsys.readouterr()
        assert outputs.out == "We don't seem to support that type of file. Please try again\n"
    def test_non_existant_file(self, monkeypatch, capsys):
        inputs = iter([self.non_existant_file, self.valid_file])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        user_interface.get_user_file()
        outputs = capsys.readouterr()
        assert outputs.out == "We couldn't find that file, try again\n"