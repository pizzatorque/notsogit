import argparse
from enum import Enum
from pprint import pprint
from typing import Callable

from repository import NotSoGitRepo


class CommandType(Enum):
    ADD = "add"
    CAT_FILE = "cat-file"
    CHECK_IGNORE = "check-ignore"
    CHECKOUT = "checkout"
    COMMIT = "commit"
    HASH_OBJECT = "hash-object"
    INIT = "init"
    LOG = "log"
    LS_FILES = "ls-files"
    LS_TREE = "ls-tree"
    REV_PARSE = "rev-parse"
    RM = "rm"
    SHOW_REF = "show-ref"
    STATUS = "status"
    TAG = "tag"


def add_cmd():
    return


def init_cmd(args: argparse.Namespace) -> NotSoGitRepo:
    repo = NotSoGitRepo.make_new_repo(args.path, True)
    return repo


COMMAND_FN_MAP: dict[CommandType, Callable] = {
    CommandType.ADD: add_cmd,
    CommandType.INIT: init_cmd,
}


parser = argparse.ArgumentParser()

subcommand = parser.add_subparsers(title="command", dest="subcommand", required=True)

init_parser = subcommand.add_parser("init")

init_parser.add_argument("path", type=str, default=".")

args = parser.parse_args()

pprint(COMMAND_FN_MAP[CommandType(args.subcommand)](args).__dict__)
