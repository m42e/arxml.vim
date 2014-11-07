try:
    #vim module is only available when run from inside vim
    import vim
except ImportError:
    vim = None

from arxml_vim import xpath as x
from arxml_vim import namespace_prefix_guesser as g

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
