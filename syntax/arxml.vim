if exists("b:current_syntax")
  finish
endif

doau Syntax xml

let b:current_syntax = "arxml"
