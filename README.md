Sublime Move By Symbols
=======================

Sublime Text plugin for navigating by symbols of current file up and down.

This is how it works with default settings out of the box.

![Animation](http://habrastorage.org/storage3/113/4e7/25a/1134e725aa2d63666d909637889cb295.gif)


Installation
---
### Package Control
With [Package Control](https://sublime.wbond.net/installation) installed:
 - Open Command Palette (<kbd>ctrl</kbd> + <kbd>shift</kbd> + <kbd>P</kbd> or <kbd>⌘ super</kbd> + <kbd>⇧ shift</kbd> + <kbd>P</kbd>)
 - Select *Package Control: Install Package* (`pkginst`)
 - Search for ***Move By Symbols*** (`mbsym`) package and install it

### Manual
Locate Sublime Text `Packages` directory (*Preferences -> Browse Packages...*)
and clone this repository there:

    git clone https://github.com/abusalimov/SublimeMoveBySymbols.git "Move By Symbols"

Usage
---
Two keybindings are provided by default:

                | OSX | Linux / Windows
--------------- | --- | ---------------
Previous Symbol | <kbd>⌃ control</kbd> + <kbd>up</kbd>   | <kbd>alt</kbd> + <kbd>up</kbd>
Next Symbol     | <kbd>⌃ control</kbd> + <kbd>down</kbd> | <kbd>alt</kbd> + <kbd>down</kbd>


Also a mouse wheel can be used insead of <kbd>up</kbd>/<kbd>down</kbd> keys, with the same modifiers.


Customization
---
The main command is **`move_by_symbols`**, it takes two boolean arguments:

 - <strong>`forward`</strong>: `bool`, mandatory<br/>Move direction
 - <strong>`extend`</strong>: `bool`, default is `false`<br/>Controls whether to retain current selection or not

### Settings files
All available options are listed [below](#available-settings).
You can also refer to *Preferences -> Package Settings -> Move By Symbols -> Settings – Default* to get the list of all settings with their description and fallback defaults.

Options are read in the following order (last match always wins):
 - Package settings
 - Sublime settings
 - Command arguments

#### Package settings
These settings have the least priority and can be used to modify options globally.
For example, to disable showing a symbol in the status bar, open `Packages/User/Move By Symbols.sublime-settings` file
(*Preferences -> Package Settings -> Move By Symbols -> Settings – User*), and add:
```json
{
    "show_in_status_bar": false
}
```

#### Sublime settings
Sublime settings chain is handled as described in the [documentation](http://www.sublimetext.com/docs/3/settings.html):

 - `Packages/User/Preferences.sublime-settings`
 - Project Settings
 - `Packages/User/<syntax>.sublime-settings`

To avoid global namespace pollution all related settings are specified with `MoveBySymbols.` prefix.
   
For example, to modify navigation through Diff files so that only names of changed files are included
(without selecting diff sections) and to make file names more conspicuous while navigating,
create `Packages/User/Diff.sublime-settings` file (or open it while editing a diff file
with *Preferences -> Settings – More -> Syntax Specific – User*) and add these lines:
```json
{
    "MoveBySymbols.symbol_selector": "meta.toc-list.file-name.diff",
    "MoveBySymbols.highlight_style": "fill",
    "MoveBySymbols.highlight_scope": "string"
}
```

#### Command arguments
Arguments passed to the `move_by_symbols` command override everything above.

For example, to add a shortcut (with, say, <kbd>ctrl</kbd> modifier) for navigating between classes only,
add the following to `Packages/User/Default (<platform>).sublime-keymap`:
```json
[
    { "keys": ["ctrl+alt+up"],   "command": "move_by_symbols",
            "args": {"forward": false, "symbol_selector": "entity.name.type"}},
    { "keys": ["ctrl+alt+down"], "command": "move_by_symbols",
            "args": {"forward": true,  "symbol_selector": "entity.name.type"}}
]
```

### Available settings
The following options contol the package behavior:

 - <strong>`symbol_selector`</strong>: `string`, default is `null`, example value: `"entity.name"`<br/>If not specified (default), a symbol index is used (shown by <kbd>ctrl</kbd> + <kbd>R</kbd> outline).
   Some syntax bundles (like Python) override symbol selector to get more neat outline by adding extra indentation or list of arguments.
   However, it is much more convenient to navigate by selecting symbol names (identifiers) only, without a surrounding text.
   Designed to be customized on a per-syntax basis using `MoveBySymbols.symbol_selector` setting.

 - <strong>`force_single_selection`</strong>: `bool`, default is `false`<br/>Setting this option to `true` discards all selections except the first or last one depending on the direction used.

 - <strong>`show_in_status_bar`</strong>: `bool`, default is `true`<br/>If a single symbol is selected, show its name in the status bar.

 - <strong>`highlight`</strong>: `bool`, default is `true`<br/>Highlight symbols while navigating.

 - <strong>`highlight_scope`</strong>: `string`, default is `null`, example value: `"string"`<br/>If not specified (default), use a foreground color of the symbol itself.
   If you want all symbols to be painted with the same color, set this option to the name of the desired scope, for example "string", or "comment".

 - <strong>`highlight_style`</strong>: one of `"outline"` or `"fill"`, default is `null`<br/>Controls how symbols are highlighted.

 - <strong>`highlight_timeout`</strong>: `int`, default is 1500<br/>Time in milliseconds before highlighting automatically disappears.

