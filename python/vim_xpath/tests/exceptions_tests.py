import unittest
from lxml import etree

from vim_xpath.exceptions import *

class ExceptionsTests(unittest.TestCase):

    def setUp(self):
        self.tree = etree.fromstring("<Root><Tag/></Root>")

    def test_undefined_namespace_in_xpath_error_is_converted(self):
        error = None
        try:
            xp = etree.XPath("//a:Tag")
            xp(self.tree)
        except Exception as e:
            error = e

        converted = from_lxml_xpath_exception(error)
        self.assertIsInstance(converted, XPathNamespaceUndefinedError)

    def test_xpath_syntax_error_is_converted(self):
        error = None
        try:
            etree.XPath("//A/Bad/XPa()th")
        except Exception as e:
            error = e

        converted = from_lxml_xpath_exception(error)
        self.assertIsInstance(converted, XPathSyntaxError)

    def test_malformed_xml_error_is_converted(self):
        error = None
        try:
            etree.fromstring("<asdhdkj")
        except Exception as e:
            error = e

        converted = from_lxml_parse_exception(error)
        self.assertIsInstance(converted, BufferXmlError)

    def test_other_errors_are_converted(self):
        error = None
        try:
            etree.XPath("//AnXWhat?")
        except Exception as e:
            error = e

        converted = from_lxml_xpath_exception(error)
        self.assertIsInstance(converted, XPathError)
