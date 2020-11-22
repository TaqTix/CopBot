import unittest
import test #import testing python file

class Testx(unittest.TestCase):

    def testx(self):
        x = test.APPVERSION
        y = test.EXPVERSION
        self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()DSS