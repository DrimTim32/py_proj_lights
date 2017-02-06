from core.configuration.config import Config
from core.algorithms.Optimizer import Optimizer


def read_configuration(config_path):
    """Reads configuration from file"""
    return Config.from_config_file(config_path)


opt = Optimizer(Config.from_config_file("../config.json"))
report, best_times = opt.optimise()
