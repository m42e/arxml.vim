"Prevent script from being loaded multiple times
if exists("g:skip_arxml")
	finish
endif

if (! exists("g:skip_arxml_python"))
	"Check python is installed
	if !has("python")
		echo 'arxml.vim requires vim to be compiled with python support, and '
					\ . 'python to be installed for several features. To stop this message from '
					\ . 'appearing, either install python, uninstall this plugin '
					\ . 'or add the line "let g:skip_arxml_python = 1" to your vimrc.'
		finish
	endif
	"Check python lxml library is installed
	let s:no_lxml = 0

	" Load the vim adaptor python script
	let s:curfile = expand("<sfile>")
	let s:curfiledir = fnamemodify(s:curfile, ":h")
	let s:pyfile = fnameescape(s:curfiledir . "/../python/main.py")
	let s:xpath_search_history = []

	py import sys
	execute "py sys.argv = ['" . s:pyfile . "']"
	execute "pyfile " . s:pyfile

py <<EOF
import vim
try:
	import lxml
except ImportError:
	vim.command('let s:no_lxml = 1')
EOF

	if s:no_lxml
		echo 'arxml.vim requires the lxml python library (http://lxml.de) to be '
					\ . 'installed. To stop this message from appearing, either '
					\ . 'install lxml, uninstall this plugin or add the line '
					\ . '"let g:skip_arxml_python = 1" to your vimrc.'
		finish
	endif
	"Load the vim adaptor python script
	let s:curfile = expand("<sfile>")
	let s:curfiledir = fnamemodify(s:curfile, ":h")

	let s:pyfile = fnameescape(s:curfiledir . "/../python/main.py")
	let s:followlast = 0

	function! FollowShortName()
		if ( "" == matchstr(getline("."), "-T\\?REF[ >]"))
			if ( s:followlast == 0)
				echo "no reference in line hit again to follow last yanked ShortName"
				let s:followlast = 1
				return
			endif
		else
			let s:followlast = 0
			silent normal! "syit
		endif
      call FollowYankedShortName()
	endf

	function! FollowYankedShortName()
		if !exists("b:ns_prefixes")
			call XPathGuessPrefixes()
		endif
		let l:active_window = winnr()
		let l:active_buffer = winbufnr(l:active_window)
		let shortnamepath = @s
      let elements = split(shortnamepath, "/")
      let xpath = ''
      for elem in elements
         let xpath = xpath . "//default:SHORT-NAME[text()=\"".elem."\"]/.."
      endfor
      " To build a robuster XPATH we do not accept any ancestor that do not
      " have a name thats part of the shortname
      let xp2 = ''
      for elem in elements[0:-2]
         if xp2 != ''
            let xp2 = xp2 . ' or '
         endif
         let xp2 = xp2 . "text()=\"".elem."\""
      endfor
      let xpath = xpath.'/self::node()[not(ancestor::*/default:SHORT-NAME[not('.xp2.')])]'

		let l:ns_prefixes = getbufvar(l:active_buffer, "ns_prefixes")
		let xpath = escape(xpath, "'\\")
	   call setqflist([])
		execute "py vim_adaptor.evaluate_xpath(" .
					\ l:active_buffer . ", " .
					\ "'" . l:xpath . "', " .
					\ "'" . l:shortnamepath . "', " .
					\ string(l:ns_prefixes) . ")"
	endf

	function! XPathGuessPrefixes()
		let l:active_window = winnr()
		let l:active_buffer = winbufnr(l:active_window)

		try
			execute "py vim_adaptor.guess_prefixes(" . l:active_buffer . ")"
			call XPathSetBufferPrefixes(l:ns_prefixes)
		catch
		endtry
	endf

	function! FindShortNameReferences()
		let l:active_window = winnr()
		let l:active_buffer = winbufnr(l:active_window)
      let b:references = []
      execute "g/".substitute(GetShortNamePathForLine(), "\\/", "\\\\/", "g")."/call add(b:references, {\"bufnr\": ".l:active_buffer.", \"lnum\": line(\".\"), \"text\": getline(\".\")})"
      if len(b:references) > 1
         call setqflist(b:references)
         execute "cw"
      else
         execute "ccl"
      endif
	endf

	function! GetShortNamePathForLine()
		if !exists("b:ns_prefixes")
			call XPathGuessPrefixes()
		endif
		let l:active_window = winnr()
		let l:active_buffer = winbufnr(l:active_window)

		let l:ns_prefixes = getbufvar(l:active_buffer, "ns_prefixes")
		execute "py vim_adaptor.get_shortnamepath(" .
					\ l:active_buffer . ", " .
					\ "'" . line(".") . "', " .
					\ string(l:ns_prefixes) . ")"
		return l:current_snpath
	endf
	
	function! GetXPathForLine()
		if !exists("b:ns_prefixes")
			call XPathGuessPrefixes()
		endif
		let l:active_window = winnr()
		let l:active_buffer = winbufnr(l:active_window)

		let l:ns_prefixes = getbufvar(l:active_buffer, "ns_prefixes")
		execute "py vim_adaptor.get_xpath(" .
					\ l:active_buffer . ", " .
					\ "'" . line(".") . "', " .
					\ string(l:ns_prefixes) . ")"
	endf

	function! XPathSetBufferPrefixes(ns_prefixes)
		if !exists("g:ns_prefixes")
			let b:ns_prefixes = a:ns_prefixes
		else
			let b:ns_prefixes = copy(g:ns_prefixes)
			for prefix in keys(a:ns_prefixes)
				"Global prefixes always 'win'
				if !has_key(b:ns_prefixes, prefix)
					let b:ns_prefixes[prefix] = a:ns_prefixes[prefix]
				else
					let b:ns_prefixes[prefix . "_buf"] = a:ns_prefixes[prefix]
				endif
			endfor
		endif
	endf
endif

" Script to detect file types
augroup filetypedetect
	au! BufRead,BufNewFile *.arxml    set filetype=arxml
augroup END

if ! exists("g:xmllint_cmd")
	let g:xmllint_cmd = 'xmllint'
endif
