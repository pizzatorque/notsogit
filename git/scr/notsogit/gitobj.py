from __future__ import annotations

import hashlib
import os
import zlib
from abc import ABC
from enum import Enum, auto
from typing import Optional, Protocol, runtime_checkable

from repository import NotSoGitRepo


class GitType(Enum):
    blob = auto()
    commit = auto()
    tag = auto()
    tree = auto()


@runtime_checkable
class Serializable(Protocol):
    def serialize(self, repo: Optional[NotSoGitRepo]) -> str: ...


@runtime_checkable
class Deserializable(Protocol):
    def deserialize(self, sha: str, repo: NotSoGitRepo) -> GitObject: ...


class AbstractGitObject(ABC):
    git_type: GitType


class GitObject(AbstractGitObject):
    def __init__(self, git_type: GitType, data: bytes):
        "whatever"
        self.git_type: GitType = git_type
        self.data: bytes = data

    def serialize(self, repo: Optional[NotSoGitRepo]) -> str:
        header = (
            f"{self.git_type.value}".encode()
            + b" "
            + f"{len(self.data)}".encode()
            + b"\x00"
            + self.data
        )
        sha = hashlib.sha1(header).hexdigest()
        if repo:
            sha_dir = os.path.join(repo.objects_dir, sha[:2])
            os.makedirs(sha_dir, exist_ok=True)
            with open(os.path.join(sha_dir, sha[2:]), "wb") as f:
                f.write(zlib.compress(header))
        return sha

    @classmethod
    def deserialize(cls, sha: str, repo: NotSoGitRepo) -> GitObject:
        sha_dir = os.path.join(repo.objects_dir, sha[:2])
        with open(os.path.join(sha_dir, sha[2:]), "rb") as f:
            header = zlib.decompress(f.read())
        type_del = header.find(b" ")
        size_del = header.find(b"\x00", type_del)
        git_type = GitType(int(header[:type_del].decode()))
        size = int(header[type_del:size_del].decode("ascii"))
        rest = header[size_del + 1 :]
        if size != len(rest):
            print("data does not match serialization")

        return cls(git_type, rest)


def __check_protocols_serializable(_: type[Serializable]):
    return


def __check_protocols_deserializable(_: type[Deserializable]):
    return


__check_protocols_serializable(GitObject)

__check_protocols_deserializable(GitObject)
