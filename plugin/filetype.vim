" Script to detect file types
augroup filetypedetect
  au! BufRead,BufNewFile *.arxml    set filetype=arxml
augroup END

