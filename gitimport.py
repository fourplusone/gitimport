import sys
import pygit2
import os.path
from importlib.machinery import ModuleSpec
from importlib.abc import PathEntryFinder, Loader

GIT_REVISION_SEPARATOR = "@"
PACKAGE_SUFFIX = '/__init__.py'
SOURCE_SUFFIX = '.py'

class GitPathNotFoundError(Exception): pass

class GitImportError(ImportError): pass

def split_git_path(path):
    in_repo_path = ''
    while True:

        if len(path) == 0: break

        git_repo, commit_sha = path.split(GIT_REVISION_SEPARATOR, 1)

        if os.path.isdir(git_repo)  and not os.path.isdir(path):
            try:
                commit = pygit2.Repository(git_repo)[commit_sha]
                return git_repo, commit_sha, in_repo_path
            except ValueError:
                pass

        path, rest = os.path.split(path)
        in_repo_path = os.path.join(rest, in_repo_path)

    raise GitPathNotFoundError


class gitimporter(PathEntryFinder):
    def __init__(self, repopath):
        self.repopath = repopath

        try:
            self.repo_basepath, self.commit_sha, self.in_repo_path = split_git_path(repopath)
        except GitPathNotFoundError:
            raise GitImportError("Git path not found")


        try:
            self.repo = pygit2.Repository(self.repo_basepath)
            self.commit = self.repo.get(self.commit_sha)
        except ValueError as e:
            raise GitImportError("Error importing Repository")

    def get_tree_entry(self, key):
        return self.commit.tree[os.path.join(self.in_repo_path, key)]

    def find_spec(self, modulename, target):
        tail_modulename = modulename.rpartition('.')[2]

        try:
            path = tail_modulename + PACKAGE_SUFFIX
            tree_entry = self.get_tree_entry(path)
            if tree_entry.type == 'blob':
                spec = ModuleSpec(modulename,
                                  GitLoader(tree_entry, self.repo),
                                  is_package=True,
                                  origin=path)

                spec.submodule_search_locations = [os.path.join(self.repopath, tail_modulename)]
                return spec
        except KeyError:
            pass

        try:
            path = tail_modulename + SOURCE_SUFFIX
            tree_entry = self.get_tree_entry(path)
            if tree_entry.type == 'blob':
                return ModuleSpec(modulename, GitLoader(tree_entry, self.repo), origin=path)
        except KeyError:
            pass


class GitLoader(Loader):
    def __init__(self, tree_entry, repo):
        self.tree_entry = tree_entry
        self.repo = repo

    def get_code(self):
        return self.repo[self.tree_entry.id].data

    def exec_module(self, module):
        exec(self.get_code(), module.__dict__)


def add_gitimporter_path_hook():
    if gitimporter not in sys.path_hooks:
        sys.path_hooks.append(gitimporter)