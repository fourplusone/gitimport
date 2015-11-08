import sys
import gitimport
import unittest
import inspect
import pygit2

class GitImporterTests(unittest.TestCase):
    def setUp(self):
        gitimport.add_gitimporter_path_hook()
        repo = pygit2.Repository('.')
        sys.path.insert(0,'.@{}/import_testmodules'.format(repo.revparse_single('HEAD').id))

    def test_import(self):
        import hello
        self.assertTrue(inspect.ismodule(hello))
        self.assertIsNotNone(hello.say_hello)

    def test_module_import(self):
        import mod
        self.assertTrue(inspect.ismodule(mod))

    def test_submodule_import(self):
        from mod import submod_hello
        self.assertIsNotNone(submod_hello)

    def test_parent_import(self):
        from mod.submod import parent_importer
        self.assertTrue(inspect.ismodule(parent_importer))



if __name__ == '__main__':
    unittest.main()