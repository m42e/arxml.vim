try:
    #vim module is only available when run from inside vim
    import vim
except ImportError:
    vim = None

import pprint
from arxml_vim import xpath as x
from arxml_vim import namespace_prefix_guesser as g
from lxml import etree

VARIABLE_SCOPE = "s:"

def get_buffer_string(bufnr):
    offset = -1

    #0-indexed buffers object became 1-indexed in vim74
    try:
        vim.buffers[0]
    except ValueError:
        offset = 0

    buffer = vim.buffers[bufnr + offset]
    return "\n".join(buffer)

def evaluate_xpath(bufnr, xpath, ns_prefixes={}):
    xml = get_buffer_string(bufnr)

    try:
        results = x.evaluate(xml, xpath, ns_prefixes)
        if len(results) > 1:
            vim.command("echo \"ShortName not unique\"")
        elif len(results) < 1:
            vim.command("echo \"ShortName path not found in file\"")
        else:
            if results[0]["line_number"] is not None:
                vim.command("normal! {0}gg".format(results[0]["line_number"]))
    except Exception as e:
        vim.command("echo \"XPath error{0}\"".format(e.msg))
        print (e.message)

def guess_prefixes(bufnr):
    try:
        xml = get_buffer_string(bufnr)
        prefixes = g.guess_prefixes(xml)

        outstr = "let l:ns_prefixes = {"
        for prefix in prefixes:
            outstr += '"{0}": "{1}",'.format(prefix, prefixes[prefix])

        outstr += "}"

        vim.command(outstr)
    except Exception as e:
        vim.command('throw "{0}"'.format(e.msg))

def get_shortnamepath(bufnr, linenr, ns_prefixes={}):
    xml = get_buffer_string(bufnr)
    try:
        tree = etree.fromstring(xml)
    except Exception as e:
        raise
    shortnamepath = ""
    for element in tree.iter():
        if (element.sourceline == int(linenr)):
            while(not element is None):
                shortnameelement = element.xpath("default:SHORT-NAME", namespaces=ns_prefixes)
                if(len(shortnameelement) > 0):
                    shortname = '/'+shortnameelement[0].text
                else:
                    shortname = ''
                shortnamepath = "{0}{1}".format(shortname, shortnamepath)
                element = element.getparent()
            break
    command = 'let l:current_snpath = \"{0}\"'.format(shortnamepath)
    print command
    vim.command(command)

def get_xpath(bufnr, linenr, ns_prefixes={}):
    xml = get_buffer_string(bufnr)
    try:
        tree = etree.fromstring(xml)
    except Exception as e:
        raise
    xpath = ""
    for element in tree.iter():
        if (element.sourceline == int(linenr)):
            while(not element is None):
                shortnameelement = element.xpath("default:SHORT-NAME", namespaces=ns_prefixes)
                if(len(shortnameelement) > 0):
                    shortname = "/SHORT-NAME[text()='{0}'/..".format(shortnameelement[0].text)
                else:
                    shortname = ''
                xpath = "{0}{1}/{2}".format(element.tag, shortname, xpath)
                element = element.getparent()
            break
    command = 'let l:current_path = \"{0}\"'.format(xpath)
    vim.command(command)
