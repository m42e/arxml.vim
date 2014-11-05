if exists("b:did_custom_ftplugin")
  finish
endif

let b:did_custom_ftplugin = 1

let g:xml_syntax_folding = 1

exec "command! -buffer XMLLint :%!" . g:xmllint_cmd . " --format -"

let s:fsize = getfsize(expand("<afile>"))
if(s:fsize>0 && s:fsize<10485760)
  setlocal foldmethod=syntax
  normal zR
endif

setlocal omnifunc=xmlcomplete#CompleteTags
