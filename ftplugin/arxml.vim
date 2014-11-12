
if exists("b:did_ftplugin")
   finish
endif
" Don't set 'b:did_ftplugin = 1' because that is xml.vim's responsability.

" Just load the stuff for xml
runtime! ftplugin/xml.vim


if has("folding")
   function! ArxmlFoldText()
      if &fdm=='diff'
         return foldtext()
      endif

      let foldtext = matchstr( getline( v:foldstart ), '\s*<[-A-Z]\+' )
      if (foldtext =~ "\s*<AR-PACKAGES")
         let pkgs = ''
         let pkgs_append = ""
         if (min([v:foldstart + 10000, v:foldend] ) < v:foldend )
            let pkgs_append = ", ...?"
         endif
         for line in split(join(getline( v:foldstart + 1, min([v:foldstart + 10000, v:foldend] ))),"\(\/AR-PACKAGE>\s*\|$\)")
            let m = matchstr(line,  '<AR-PACKAGE.\{-}>\s*<SHORT-NAME>\zs[-_A-Za-z0-9]\+\ze<\/SHORT-NAME>')
            if(m != "")
               if(pkgs == '')
                  let pkgs .= " PKGS: "
               else
                  let pkgs .= ', '
               endif
               let pkgs .= m
            endif
         endfor
         if (pkgs != '')
            let foldtext .= pkgs.pkgs_append
         endif
      else
         let shortname = matchstr( join( getline( v:foldstart + 1, v:foldstart + 5 ) ), '^\s*<SHORT-NAME>\zs[-_A-Za-z0-9]\+\ze<\/SHORT-NAME>' )
         if( shortname != "" )
            let foldtext .= ' "' . shortname . '"'
         else
            let reference = matchstr( join( getline(v:foldstart + 1, min([v:foldend, v:foldstart + 2]) ) ), '^\s*<.\{-}-REF .\{-}>.*\/\zs[-_A-Za-z0-9]\+\ze<', 0,1)

            if( reference != "" )
               let foldtext .=  ' REF:"' . reference . '"'
            endif
         endif
      endif 
      let foldtext .= '>'

      let foldtext .= ' (' . ( v:foldend-v:foldstart ) . ' lines) '
      let linelength = winwidth(0) - &foldcolumn
      if( &number || &relativenumber )
         let linelength -= &numberwidth
      endif
      let foldtext = strpart( foldtext, 0, linelength )

      return foldtext
   endfunction

   setlocal foldtext=ArxmlFoldText()
endif
