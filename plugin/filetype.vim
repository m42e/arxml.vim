" Script to detect file types
augroup filetypedetect
  au! BufRead,BufNewFile *.arxml    set filetype=arxml
augroup END

if ! exists("g:xmllint_cmd")
   let g:xmllint_cmd = 'xmllint'
endif
