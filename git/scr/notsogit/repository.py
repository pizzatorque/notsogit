import configparser
import os

NOT_SO_GIT_DIR = ".notsogit"


def _create_dir(path: str, force: bool = False):
    try:
        os.makedirs(name=path, exist_ok=force)
    except OSError as e:
        print(e)
        return False
    return True


def _make_file_if_not(path: str, force=False):
    if not os.path.exists(path) or force:
        with open(path, "w") as f:
            f.write("")
    else:
        raise OSError(f"File {path} already exists")


def find_repo_root(path: str):
    abs_path = os.path.abspath(path)
    if ".notsogit" in os.listdir(abs_path):
        return abs_path
    upper_abs_path = "/".join(abs_path.split("/")[:-1])
    if os.path.exists(upper_abs_path):
        return find_repo_root(upper_abs_path)
    raise OSError("Cannot find Not So Git Root")


class NotSoGitRepo:
    def __init__(self, path: str, force: bool = False):
        abs_path = os.path.abspath(path)
        self.git_dir = os.path.join(abs_path, NOT_SO_GIT_DIR)
        self.config_parser = configparser.ConfigParser()
        self.config_location = os.path.join(self.git_dir, "config")
        self.__init_config()
        self.config = self.__load_config(self.config_location)
        self.objects_dir = os.path.join(self.git_dir, "objects")
        self.refs_dir = os.path.join(self.git_dir, "refs")
        self.head_path = os.path.join(self.git_dir, "HEAD")

    def __init_config(self):
        with open(self.config_location) as _:
            contents = _.read()
            if len(contents) > 0:
                return

        with open(self.config_location, "w") as f:
            self.config_parser.add_section("core")
            self.config_parser.set("core", "repositoryformatversion", "0")
            self.config_parser.set("core", "filemode", "false")
            self.config_parser.set("core", "bare", "false")
            self.config_parser.write(f)

    def __load_config(self, path: str) -> str:
        if not os.path.exists(path):
            raise OSError("Path to notsogit config does not exist")
        with open(self.config_location) as _:
            contents = _.read()
            return contents

    @classmethod
    def make_new_repo(cls, path: str, force: bool = False):
        abs_path = os.path.abspath(path)
        git_dir = os.path.join(abs_path, NOT_SO_GIT_DIR)
        _create_dir(git_dir, force)
        for dir in ["objects", "refs"]:
            _create_dir(os.path.join(git_dir, dir))
        for _file in ["HEAD", "config"]:
            _make_file_if_not(os.path.join(git_dir, _file), force)
        return cls(abs_path, force)
