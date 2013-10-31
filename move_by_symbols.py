"""
Jump up and down between symbols of current file.
"""

__author__ = 'Eldar Abusalimov'

import sublime_plugin


class MoveBySymbolsCommand(sublime_plugin.TextCommand):

    def run(self, edit, **kwargs):
        try:
            forward = bool(kwargs['forward'])
        except KeyError:
            return  # do nothing in case of missing required argument

        settings = self.view.settings()

        # By default one can move multiple selections (why not, after all?).
        # Setting 'single_selection' to true discards all selections
        # except the first/last (depending on the direction used).
        try:
            single_selection = kwargs['single_selection']
        except KeyError:
            single_selection = settings.get('single_selection', False)

        # Some syntax bundles (like Python) override default symbol selector
        # to get more neat looking symbol outline.
        # For example, for this file the first two symbols from outline are
        # 'class MoveBySymbolsCommand(sublime_plugin.TextCommand):' and
        # '    def run(...):'.
        # However, it is much more convenient to navigate by selecting
        # identifiers only, like 'MoveBySymbolsCommand' and 'run', without a
        # surrounding text.
        try:
            symbol_selector = kwargs['symbol_selector']
        except KeyError:
            symbol_selector = settings.get('symbol_selector', 'entity.name')

        self.do_move(forward, single_selection, symbol_selector)

    def do_move(self, forward, single_selection, symbol_selector):
        sel = self.view.sel()

        if single_selection:
            self.fixup_empty_selection(forward)
            sel_list = [sel[-forward]]
        else:
            sel_list = list(sel)

        if symbol_selector:
            sym_list = self.view.find_by_selector(symbol_selector)
        else:  # fallback: use symbols from ouline
            sym_list = [region for region, string in self.view.symbols()]

        sel_it = uni_iter(sel_list, forward)
        sym_it = uni_iter(sym_list, forward)

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

