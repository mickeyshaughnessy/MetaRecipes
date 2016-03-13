set encoding=utf-8


let pyindent_nested_paren="&sw*2"
let pyindent_open_paren="&sw*2"

set ruler
set bs=2
autocmd FileType yaml,html set ts=2 softtabstop=2 shiftwidth=2 expandtab
autocmd FileType python,markdown,javascript,node set ts=4 softtabstop=4 shiftwidth=4 expandtab
autocmd FileType rust,rs set sw=4 ts=4 sts=4 tw=99 expandtab smarttab
autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
