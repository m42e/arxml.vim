import re

from lxml import etree

LIBXML2_MAX_LINE = 65534

def evaluate(xml, xpath, namespaces=dict()):
    try:
        results = _evaluate(xml, xpath, namespaces)
        return results
    except Exception as e:
        if isinstance(e, XmlBaseError):
            raise
        else:
            raise

def _evaluate(xml, xpath, namespaces=dict(), compiled_xpath=None):
    """Evaluate an xpath against some xml. 
    Reports line numbers correctly on xml with over 65534 lines"""

    try:
        tree = etree.fromstring(xml)
    except Exception as e:
        raise

    try:
        if compiled_xpath is None:
            compiled_xpath = etree.XPath(xpath, namespaces=namespaces)

        tree_matches = compiled_xpath(tree)
    except Exception as e:
        raise

    if not(isinstance(tree_matches, list)):
        tree_matches = [tree_matches]

    matches = []
    line_compress_required = False

    for match in tree_matches:
        output_match = _tree_match_to_output_match(match, namespaces)

        if (output_match["line_number"] is None) or \
                output_match["line_number"] <= LIBXML2_MAX_LINE:
            #Only keep matches which are in the line range that libxml2
            #actually reports correctly
            matches.append(output_match)
        else:
            #If there are any higher range matches, 
            #we will have to 'compress lines'
            line_compress_required = True
            break;

    if line_compress_required:
        #Compress the inital line range 1-65534 into a single line,
        #to give us correct line numbers on the next 65534 lines.
        line_compressed_xml = xml.replace("\n", "", LIBXML2_MAX_LINE)

        #Re-evaluate with the new source XML recursively,
        #to handle all higher line ranges
        line_compressed_matches = _evaluate(line_compressed_xml, xpath,
                compiled_xpath=compiled_xpath)

        #Only take matches which we haven't already found, as the higher range
        #evaluations will have incorrect line numbers for matches in lower ranges
        #(the sourceline will be 1 for all lower range matches)
        new_output_matches = line_compressed_matches[len(matches):]

        for output_match in new_output_matches:
            #As we've compressed a bunch of lines down to 1 line, we need to
            #offset the line number of the results to compensate for this
            output_match["line_number"] += LIBXML2_MAX_LINE
            matches.append(output_match)

    return matches

def _tree_match_to_output_match(match, namespaces):
    """Convert an lxml xpath match to a result output dictionary"""
    out = dict()
    out["line_number"] = _output_line_number(match)

    return out

def _output_line_number(match):
    """Return an output source line for a particular match result"""
    sourceline = None

    if isinstance(match, etree._Element):
        sourceline = match.sourceline

    if isinstance(match, etree._ElementStringResult):
        parent = match.getparent()
        if parent is not None:
            sourceline = parent.sourceline

    return sourceline
