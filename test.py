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
        sys.path.insert(0,'/a/repo/that/does/not/exist@fffff00')
        
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
    
    def test_importerror(self):
        try:
            import does_not_exists
        except ImportError:
            pass



if __name__ == '__main__':
    unittest.main()