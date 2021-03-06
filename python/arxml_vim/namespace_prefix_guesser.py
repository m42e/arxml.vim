from lxml import etree

class PrefixGuessingError(Exception):
    def __init__(self, e):
        self.inner = e
        self.msg = "An error occurred while guessing namespace prefixes: "\
           + "{0} - {1}".format(e.__class__.__name__, e.msg)

def guess_prefixes(xml):
    try:
        a =  _guess_prefixes(xml)
        return a
    except Exception as e:
        wrapped = PrefixGuessingError(e)
        raise wrapped

def _guess_prefixes(xml):
    """Attempt to create a rough prefix -> url mapping based on an input XML.
    The tree is traversed depth first, and the first node to define the
    prefix 'claims' it with URL assosciated with that prefix in that node.
    The first prefixless namespace found is given the prefix 'default'. """

    prefixes = {}

    utf8_parser = etree.XMLParser(encoding='utf-8')
    s = xml.encode('utf-8')
    tree =  etree.fromstring(s, parser=utf8_parser)


    for el in tree.iter():
        node_prefixes = el.nsmap
        if node_prefixes is not None:
            for prefix in node_prefixes.keys():
                url = node_prefixes[prefix]

                if prefix is None:
                    prefix = "default"

                if not prefix in prefixes:
                    prefixes[prefix] = url

    return prefixes
