import sys
import gitimport
import unittest
import inspect
import pygit2

class GitImporterTests(unittest.TestCase):
    def setUp(self):
        gitimport.add_gitimporter_path_hook()
        self.repo = repo = pygit2.Repository('.')
        self.commit_sha = repo.revparse_single('HEAD').hex
        sys.path.insert(0,'/a/repo/that/does/not/exist@fffff00')
        sys.path.insert(0, gitimport.repository_path(self.repo, in_repo_path='import_testmodules'))

    def test_convenience(self):
        expected_path = sys.path.pop(0)
        sys.path.insert(0, gitimport.repository_path(self.repo, in_repo_path='import_testmodules'))
        self.assertEqual(expected_path, sys.path.pop(0))

        sys.path.insert(0, gitimport.repository_path('.', in_repo_path='import_testmodules'))
        self.assertEqual(expected_path, sys.path.pop(0))

        gitimport.add_repository_to_path('.', in_repo_path='import_testmodules')
        self.assertEqual(expected_path, sys.path.pop(0))
        sys.path.insert(0, expected_path)

    def test_import(self):
        import hello
        self.assertTrue(inspect.ismodule(hello))
        self.assertIsNotNone(hello.say_hello)
        self.assertEqual(hello.__git_commit__, self.commit_sha)

    def test_module_import(self):
        import mod
        self.assertTrue(inspect.ismodule(mod))
        self.assertEqual(mod.__git_commit__, self.commit_sha)


    def test_submodule_import(self):
        from mod import submod_hello
        self.assertIsNotNone(submod_hello)

    def test_parent_import(self):
        from mod.submod import parent_importer
        self.assertTrue(inspect.ismodule(parent_importer))
    
    def test_importerror(self):
        try:
            import does_not_exists
        except ImportError:
            pass

    def test_repository_path(self):
        path = gitimport.repository_path(self.repo)
        self.assertEqual(path, self.repo.path + "@" + self.commit_sha + '/')



if __name__ == '__main__':
    unittest.main()