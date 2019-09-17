import json
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from collections import OrderedDict


def read_json(filename):
    db = {}

    with open(filename) as f:
        db = json.loads(f.read())

    return db


class PartFinder:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.partdb = read_json(dir_path + "/database/part_database.json")

    def process_partname(self, partname: str) -> dict:
        # Get results from fuzzy matching, limit to sensible number of viewing
        res = process.extract(partname, self.partdb .keys(), limit=5)
        # Sort tuple by value (largest to smallest)
        res.sort(key=lambda x: x[1], reverse=True)
        # Create and orderered dict and insert the values based on match value
        dict_parts = OrderedDict()
        for i in res:
            dict_parts[i[0]] = i[1]
        return dict_parts

    def find(self, board_name: str) -> dict:
        """
        Find a board and return recommended settings
        :param board_name: str
        :return: dict
        """
        return self.partdb[board_name]

if __name__ == "__main__":
    pf = PartFinder()
    print(f"{pf.partdb['Arduino Zero']}")
    res = pf.process_partname("Zero")
    print(res)
