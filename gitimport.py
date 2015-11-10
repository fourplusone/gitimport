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

        try:
            git_repo, commit_sha = path.split(GIT_REVISION_SEPARATOR, 1)
        except ValueError:
            # In case the path does not contain a GIT_REVISION_SEPARATOR
            break

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
                                  GitLoader(tree_entry, self.repo, self.commit_sha),
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
                return ModuleSpec(modulename, GitLoader(tree_entry, self.repo, self.commit_sha), origin=path)
        except KeyError:
            pass


class GitLoader(Loader):
    def __init__(self, tree_entry, repo, commit_sha=None):
        self.tree_entry = tree_entry
        self.repo = repo
        self.commit_sha = commit_sha

    def get_code(self):
        return self.repo[self.tree_entry.id].data

    def exec_module(self, module):
        if self.commit_sha is not None:
            module.__git_commit__ = self.commit_sha
        exec(self.get_code(), module.__dict__)


def add_gitimporter_path_hook():
    """
    Add gitimport to sys.path_hooks.
    """
    if gitimporter not in sys.path_hooks:
        sys.path_hooks.append(gitimporter)


def repository_path(repo, rev='HEAD', in_repo_path=''):
    """
    Build a path (for further use in sys.path) from a repository reference

    :param repo: a pygit2 repository object or a path to a git repository
    :param rev: the revision which should be used. Acceptable values are all valid git revisions such as 'master',
    'origin/master', 'HEAD', commit SHAs (see man gitrevisions for more information)
    :param in_repo_path: path inside the repository from which the modules should be loaded
    :return:
    """

    if isinstance(repo, str):
        repo = pygit2.Repository(repo)

    path = '{}@{}'.format(repo.path, repo.revparse_single(rev).hex)
    return os.path.join(path, in_repo_path)

def add_repository_to_path(repo, rev='HEAD', in_repo_path=''):
    """
    Adds a repository reference to sys.path. If gitimporter is not initialized yet, it will also be added to
    sys.path_hooks

    :param repo: a pygit2 repository object or a path to a git repository
    :param rev: the revision which should be used. Acceptable values are all valid git revisions such as 'master',
    'origin/master', 'HEAD', commit SHAs (see man gitrevisions for more information)
    :param in_repo_path: path inside the repository from which the modules should be loaded
    :return:
    """
    add_gitimporter_path_hook()
    sys.path.insert(0, repository_path(repo, rev, in_repo_path))
