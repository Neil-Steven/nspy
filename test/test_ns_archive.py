import unittest

from ns_archive import *


class NsArchiveTestCase(unittest.TestCase):

    def test_compress(self):
        compress()

    def test_make_zip(self):
        make_zip()

    def test_make_7z(self):
        make_7z()

    def test_make_tar(self):
        make_tar()

    def test_make_gz(self):
        make_gz()

    def test_decompress(self):
        decompress()

    def test_un_zip(self):
        un_zip()

    def test_un_rar(self):
        un_rar()

    def test_un_7z(self):
        un_7z()

    def test_un_tar(self):
        un_tar()

    def test_un_gz(self):
        un_gz()
