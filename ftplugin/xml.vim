if exists("b:did_custom_ftplugin")
  finish
endif

let b:did_custom_ftplugin = 1

let g:xml_syntax_folding = 1

setlocal equalprg=g:xmllint_cmd . "xmllint --format --recover -"
setlocal foldmethod=syntax

setlocal omnifunc=xmlcomplete#CompleteTags
