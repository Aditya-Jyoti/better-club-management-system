import tomllib
from functools import lru_cache


@lru_cache
def get_settings():
    with open("settings.toml", "rb") as toml_file:
        return tomllib.load(toml_file)


@lru_cache
def get_scopes():
    return {
        "read:user": "Read user information",
        "write:user": "Write user information",
        "delete:user": "Delete user information",
    }
