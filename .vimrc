set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
Plugin 'tpope/vim-fugitive'
" plugin from http://vim-scripts.org/vim/scripts.html
"Plugin 'L9'
" Git plugin not hosted on GitHub
"Plugin 'git://git.wincent.com/command-t.git'
"Plugin 'Lokaltog/vim-powerline'
Plugin 'bling/vim-airline'
Plugin 'elzr/vim-json'
"Plugin 'bling/vim-airline'
" git repos on your local machine (i.e. when working on your own plugin)
" Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.
"Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Avoid a name conflict with L9
"Plugin 'user/L9', {'name': 'newL9'}

" All of your Plugins must be added before the following line
call vundle#end()            " required
"filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

""" Puts a vertical bar at 80 characters
"if (exists('+colorcolumn'))                                                     
"set colorcolumn=80                                                          
"highlight ColorColumn ctermbg=9                                             
"endif

syntax on
"set mouse=a
" Indent Python in the Google way.

"setlocal indentexpr=GetGooglePythonIndent(v:lnum)

"let s:maxoff = 50 " maximum number of lines to look backwards.

"function GetGooglePythonIndent(lnum)
"
"  " Indent inside parens.
"  " Align with the open paren unless it is at the end of the line.
"  " E.g.
"  "   open_paren_not_at_EOL(100,
"  "                         (200,
"  "                          300),
"  "                         400)
"  "   open_paren_at_EOL(
"  "       100, 200, 300, 400)
"  call cursor(a:lnum, 1)
"  let [par_line, par_col] = searchpairpos('(\|{\|\[', '', ')\|}\|\]', 'bW',
"        \ "line('.') < " . (a:lnum - s:maxoff) . " ? dummy :"
"        \ . " synIDattr(synID(line('.'), col('.'), 1), 'name')"
"        \ . " =~ '\\(Comment\\|String\\)$'")
"  if par_line > 0
"    call cursor(par_line, 1)
"    if par_col != col("$") - 1
"      return par_col
"    endif
"  endif
"
"  " Delegate the rest to the original function.
"  return GetPythonIndent(a:lnum)
"
"endfunction
let g:Powerline_symbols = 'fancy'
"let g:airline_powerline_fonts = 1
set laststatus=2
set encoding=utf-8


let pyindent_nested_paren="&sw*2"
let pyindent_open_paren="&sw*2"

set ruler
set bs=2
autocmd FileType yaml set ts=2 softtabstop=2 shiftwidth=2 expandtab
autocmd FileType python,markdown,javascript,node set ts=4 softtabstop=4 shiftwidth=4 expandtab
autocmd FileType rust,rs set sw=4 ts=4 sts=4 tw=99 expandtab smarttab

