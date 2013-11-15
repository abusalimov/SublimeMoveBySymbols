Sublime Move By Symbols
=======================

Sublime Text plugin for navigating by symbols of current file up and down.

This is how it works with default settings out of the box.

![Animation](http://habrastorage.org/storage3/113/4e7/25a/1134e725aa2d63666d909637889cb295.gif)


Usage
---
Two keybindings are available by default:

                | Windows / Linux | OSX
--------------- | --------------- | --- 
Previous Symbol | <kbd>alt</kbd> + <kbd>up</kbd>   | <kbd>⌃ control</kbd> + <kbd>up</kbd>
Next Symbol     | <kbd>alt</kbd> + <kbd>down</kbd> | <kbd>⌃ control</kbd> + <kbd>down</kbd>

Also a mouse wheel can be used insead of <kbd>up</kbd>/<kbd>down</kbd> keys, with the same modifiers.


Customization
---
The main command is **`move_by_symbols`**, it takes two boolean arguments:

 - <strong>`forward`</strong>: `bool`, mandatory<br/>
   Move direction
 - <strong>`extend`</strong>: `bool`, default is `false`<br/>
   Controls whether to retain current selection or not

Apart from these two arguments, few more options are considered:

 - <strong>`symbol_selector`</strong>: `string`, default is `null`, example value: `"entity.name"`<br/>
   If not specified (default), a symbol index is used (shown by <kbd>ctrl</kbd> + <kbd>R</kbd> outline).
   Some syntax bundles (like Python) override symbol selector to get more neat outline
   by adding extra indentation or list of arguments.
   However, it is much more convenient to navigate by selecting symbol names (identifiers) only,
   without a surrounding text.
   Designed to be customized on a per-syntax basis using `MoveBySymbols.symbol_selector` setting.

 - <strong>`force_single_selection`</strong>: `bool`, default is `false`<br/>
   Setting this option to `true` discards all selections except the first or last one
   depending on the direction used.

 - <strong>`highlight`</strong>: `bool`, default is `true`<br/>
   Highlight symbols while navigating.

 - <strong>`highlight_scope`</strong>: `string`, default is `null`, example value: `"string"`<br/>
   If not specified (default), use a foreground color of the symbol itself.
   If you want all symbols to be painted with the same color, set this option
   to the name of the desired scope, for example "string", or "comment".

 - <strong>`highlight_style`</strong>: one of `"outline"` or `"fill"`, default is `null`<br/>
   Controls how symbols are highlighted.

 - <strong>`highlight_timeout`</strong>: `int`, default is 1500<br/>
   Time in milliseconds before highlighting automatically disappears.


Installation
---
TDB

