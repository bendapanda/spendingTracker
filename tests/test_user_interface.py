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
    def test_valid_file(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: self.valid_file)
        data, status = user_interface.get_user_file()
        assert type(data) == pd.DataFrame
