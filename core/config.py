import json
import logging
import os
import traceback

from discord.ext.commands.bot import AutoShardedBot

from core.functions import jsonKeys2int


class Configuration():
    "Class for maintaining configuration information and files"

    def __init__(self, filename: str, bot: AutoShardedBot):
        self.CONFIG = os.path.expanduser(f"./config/{filename}.json")
        self.config: dict[str, dict] = {}
        self.bot = bot

    def load(self):
        try:
            logging.info(
                f"Loading: {self.CONFIG}")
            self.config = json.load(
                open(self.CONFIG, encoding="utf-8"), object_hook=jsonKeys2int)
            type(self.config.keys())
        except FileNotFoundError:
            logging.warning(
                f"Config is unavailable or protected. Loading fallback...")
            self.config = self.bot.fallback
            logging.info(f"Fallback loaded")
            try:
                logging.info(
                    f"Creating new config file: {self.CONFIG}")
                self.save()
            except:
                logging.info(traceback.format_exc())
                logging.error(
                    f"Error writing config file, please check if you have permission to write in this location: {self.CONFIG}")
                return
        logging.info(f"Config loaded")

    def save(self):
        try:
            with open(self.CONFIG, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4,
                          sort_keys=True, ensure_ascii=False)
            logging.debug("Config saved")
        except:
            logging.info(traceback.format_exc())
            logging.warning(f"Unable to save data to {self.CONFIG}")

    def json_str(self):
        return json.dumps(self.config)

    def __repr__(self):
        return self.config

    def __getitem__(self, name: str):
        logging.debug(f"Grabbing {name} from config")
        try:
            return self.config[name]
        except:
            logging.debug(
                f"{name} not found in config, trying to get from fallback")
            self.config[name] = self.bot.fallback[name]
            self.save()
            return self.bot.fallback[name]

    def __setitem__(self, key: str, val):
        logging.debug(f"Setting {key} to {val}")
        self.config[key] = val

    def __delitem__(self, key: str):
        logging.debug(f"Deleting {key} from config")
        self.config.pop(key)
