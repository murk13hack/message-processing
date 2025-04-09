import yaml
from typing import Dict, Any
from functools import cache

@cache
def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    required_fields = ["db_config", "prompt_file", "rebbitMQ_host", "rebbitMQ_queue_name"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required config field: {field}")
    
    return config

CONFIG = load_config()