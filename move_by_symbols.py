"""
Jump up and down between symbols of current file.
"""

__author__ = 'Eldar Abusalimov'


import sublime, sublime_plugin

ST3 = (int(sublime.version()) >= 3000)
if ST3:
    from .symbols_highlighting import add_highlighting
else:
    from symbols_highlighting import add_highlighting

symbolCache = {}

# remove symbol cache on edit or on close
class MoveBySymbolsEventListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        if view.id() in symbolCache:
            del symbolCache[view.id()]

    def on_close(self, view):
        if view.id() in symbolCache:
            del symbolCache[view.id()]      

class MoveBySymbolsCommand(sublime_plugin.TextCommand):

    def run(self, edit, **kwargs):
        try:
            forward = bool(kwargs['forward'])
        except KeyError:
            return  # do nothing in case of missing required argument

        extend = bool(kwargs.get('extend', False))

        # Some syntax bundles (like Python) override default symbol selector
        # to get more neat looking symbol outline.
        # For example, for this file the first two symbols from the outline are
        # 'class MoveBySymbolsCommand(sublime_plugin.TextCommand):' and
        # '    def run(...):'.
        # However, it is much more convenient to navigate by selecting
        # names (identifiers) only, like 'MoveBySymbolsCommand' and 'run',
        # without a surrounding text.
        symbol_selector = self.get_option(kwargs, 'symbol_selector')

        # By default one can move multiple selections (why not, after all?).
        # Setting 'force_single_selection' argument to true discards all
        # selections except the first/last (depending on the direction used).
        force_single_selection = bool(
                self.get_option(kwargs, 'force_single_selection'))

        # cache symbols to improve performance in large files
        viewId = self.view.id()
        if viewId not in symbolCache:
            symbolCache[viewId] = self.find_symbols(symbol_selector)

        symbols = symbolCache[viewId]

        self.do_move(symbols, forward, extend, force_single_selection)

        if bool(self.get_option(kwargs, 'show_in_status_bar')):
            sel = self.view.sel()
            if len(sel) == 1:
                symbol_string = self.view.substr(sel[0])
                sublime.status_message(symbol_string)

        if bool(self.get_option(kwargs, 'highlight')):
            hl_scope = self.get_option(kwargs, 'highlight_scope')
            if not isinstance(hl_scope, str):
                hl_scope = None

            hl_style = self.get_option(kwargs, 'highlight_style')
            if hl_style not in ("outline", "fill"):
                hl_style = "outline"

            hl_timeout = self.get_option(kwargs, 'highlight_timeout')
            if not isinstance(hl_timeout, int):
                hl_timeout = 1500   # default value

            add_highlighting(self.view, symbols,
                             hl_scope, hl_style, hl_timeout)

    def get_option(self, kwargs, name, default=None):
        try:
            return kwargs[name]
        except KeyError:
            view_settings = self.view.settings()
            view_key = 'MoveBySymbols.' + name
            if view_settings.has(view_key):
                return view_settings.get(view_key)
            else:
                return plugin_settings.get(name)

    def find_symbols(self, symbol_selector=None):
        if symbol_selector:
            return self.view.find_by_selector(symbol_selector)
        else:  # fallback: use symbols from the outline
            return [region for region, string in self.view.symbols()]

    def do_move(self, symbols, forward, extend=False,
                force_single_selection=False):
        sel = self.view.sel()

        if force_single_selection:
            self.fixup_empty_selection(forward)
            selection = [sel[-forward]]
        else:
            selection = list(sel)

        sel_it = uni_iter(selection, forward)
        sym_it = uni_iter(symbols, forward)

        if not extend:
            sel.clear()

        # O(max(Nsel, Nsym)), not their product (as one might have thought)
        for sel_region in sel_it:
            cursor = sel_region.a

            for sym_region in sym_it:
                if point_past_region_boundary(cursor, sym_region, forward):
                    break  # inner
            else:
                break  # outer

            sel.add(sym_region)

        self.fixup_empty_selection(not forward)  # fallback cursor at bof/eof
        self.view.show(sel[-forward])

    def fixup_empty_selection(self, begin):
        sel = self.view.sel()
        if len(sel) == 0:
            sel.add(0 if begin else self.view.size())


def uni_iter(iterable, forward=True):
    if forward:
        return iter(iterable)
    else:
        return reversed(iterable)

def point_past_region_boundary(point, region, begin):
    if begin:
        return (point < region.begin())
    else:
        return (point > region.end())


def plugin_loaded():
    global plugin_settings
    plugin_settings = sublime.load_settings('Move By Symbols.sublime-settings')

if not ST3:
    plugin_loaded()
