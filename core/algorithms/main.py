from core.configuration.config import Config
from core.algorithms.optimiser import Optimiser


def read_configuration(config_path):
    """Reads configuration from file"""
    return Config.from_config_file(config_path)


opt = Optimiser(Config.from_config_file("../config.json"))
report, best_times = opt.optimise()
