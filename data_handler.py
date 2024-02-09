import distutils.util
import json
import os
import logging


IGNORE_DATA = ['const']


class SaveHandler:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.default_save_data_file = 'files/default_save_data.json'
        self.save_data_file = 'save_data.json'

        if not os.path.exists(self.save_data_file):
            self.create_save_file()

        self.check_and_patch_integrity()

    def check_and_patch_integrity(self):
        with open(self.save_data_file, 'r') as fh:
            current_data = json.load(fh)
        with open(self.default_save_data_file, 'r') as default_data_file:
            default_data = json.load(default_data_file)

        for option in default_data:
            if option not in IGNORE_DATA:
                if option not in current_data:
                    self.logger.warning(f"Option '{option}' not found in '{self.save_data_file}', adding.")
                    current_data[option] = default_data[option]
                    self.dump_data_into_save(current_data)

                # inside option level
                for sub_option in default_data[option]:
                    if sub_option not in current_data[option]:
                        self.logger.warning(f"Sub-option '{sub_option}' not found in option '{option}' of '{self.save_data_file}', adding.")
                        current_data[option][sub_option] = default_data[option][sub_option]
                        self.dump_data_into_save(current_data)

    def dump_data_into_save(self, data: dict):
        with open(self.save_data_file, 'r+') as fh:
            fh.truncate(0)
            data.pop('const')
            json.dump(data, fh, indent=4)

    def create_save_file(self):
        with open(self.save_data_file, 'w') as fh:  # creates
            with open(self.default_save_data_file, 'r') as default_data:
                self.logger.info("creating new save data file")
                self.dump_data_into_save(json.load(default_data))

    def get_option(self, option: str):
        with open(self.save_data_file, 'r') as fh:
            data = json.load(fh)
            val = data['options'][option]
            if max_value := self.get_const('max_' + option):
                val = min(max_value, val)
            if min_value := self.get_const('min_' + option):
                val = max(min_value, val)
            return val

    def get_save(self, save_num: int):
        with open(self.save_data_file, 'r') as fh:
            data = json.load(fh)
            return data['save'][save_num]

    def get_const(self, option: str):
        """ Retrieves default data const """
        with open(self.default_save_data_file, 'r') as default_fh:
            const_data = json.load(default_fh)['const']
            if option in const_data:
                return const_data[option]
            return False

    def set_option(self, option: str, value):
        pass

    def set_save(self, save_num):
        pass
