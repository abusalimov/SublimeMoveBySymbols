"""
Jump up and down between symbols of current file.
"""

__author__ = 'Eldar Abusalimov'

import sublime, sublime_plugin

import collections

class MoveBySymbolsCommand(sublime_plugin.TextCommand):

    highlighted = None  # { "scope": [regions...] }

    def run(self, edit, **kwargs):
        try:
            forward = bool(kwargs['forward'])
        except KeyError:
            return  # do nothing in case of missing required argument

        extend = bool(kwargs.get('extend', False))

        # By default one can move multiple selections (why not, after all?).
        # Setting 'force_single_selection' argument to true discards all
        # selections except the first/last (depending on the direction used).
        force_single_selection = kwargs.get('force_single_selection', False)

        # Some syntax bundles (like Python) override default symbol selector
        # to get more neat looking symbol outline.
        # For example, for this file the first two symbols from the outline are
        # 'class MoveBySymbolsCommand(sublime_plugin.TextCommand):' and
        # '    def run(...):'.
        # However, it is much more convenient to navigate by selecting
        # names (identifiers) only, like 'MoveBySymbolsCommand' and 'run',
        # without a surrounding text.
        symbol_selector = self.get_option(kwargs, 'symbol_selector',
                                          'move_by_symbols_selector')

        # Highlighting options: style, scope, timeout
        highlight = self.get_option(kwargs, 'highlight')
        highlight = True
        if highlight is True:
            highlight = "outline"
        if highlight not in ("outline", "fill"):
            highlight = None

        highlight_scope = self.get_option(kwargs, 'highlight_scope')
        if not isinstance(highlight_scope, str):
            highlight_scope = None

        highlight_timeout = self.get_option(kwargs, 'highlight_timeout')
        if not isinstance(highlight_timeout, int):
            highlight_timeout = 1500   # default value

        symbols = self.find_symbols(symbol_selector)

        if highlight or 1:
            self.highlight_symbols(symbols, highlight,
                                   highlight_scope, highlight_timeout)

        self.do_move(symbols, forward, extend, force_single_selection)

    def get_option(self, kwargs, arg_name, setting_name=None):
        try:
            return kwargs[arg_name]
        except KeyError:
            if setting_name is None:
                setting_name = 'move_by_symbols_' + arg_name
            return self.view.settings().get(setting_name)

    def find_symbols(self, symbol_selector=None):
        if symbol_selector:
            return self.view.find_by_selector(symbol_selector)
        else:  # fallback: use symbols from the outline
            return [region for region, string in self.view.symbols()]

    def highlight_symbols(self, symbols, style, scope, timeout):
        self.clear_highlighting()

        draw_flags = 0
        if style != "fill":     draw_flags |= sublime.DRAW_NO_FILL
        if style != "outline":  draw_flags |= sublime.DRAW_NO_OUTLINE

        self.highlighted = regions_dict = collections.defaultdict(list)

        if scope:
            regions_dict[scope] = symbols
        else:
            for symbol in symbols:
                symbol_scope = self.view.scope_name(symbol.begin())
                regions_dict[symbol_scope].append(symbol)

        for region_scope, regions in regions_dict.items():
            self.view.add_regions('move_by_symbols : ' + region_scope,
                                  regions, region_scope, flags=draw_flags)

        sublime.set_timeout(lambda: self.clear_highlighting(regions_dict),
                            timeout)

    def clear_highlighting(self, regions_dict=None):
        if regions_dict is not self.highlighted or self.highlighted is None:
            return  # highlighting changed or nothing highlighted at all

        for region_scope in self.highlighted:
            self.view.erase_regions('move_by_symbols : ' + region_scope)

        del self.highlighted

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

