"""
Jump up and down between symbols of current file.
"""

__author__ = 'Eldar Abusalimov'

import sublime_plugin

class MoveBySymbolsCommand(sublime_plugin.TextCommand):

    def run(self, edit, forward=None, single_selection=False,
            symbol_selector='entity.name'):
        if forward is None:
            return  # to bypass TypeError on missing argument

        sel = self.view.sel()

        if single_selection:
            self.fixup_empty_selection(forward)
            sel_list = [sel[-forward]]
        else:
            sel_list = list(sel)

        sel_it = uni_iter(sel_list, forward)
        sym_it = uni_iter(self.view.symbols(), forward)

        sel.clear()

        # O(max(Nsel, Nsym)), not their product (as one might have thought)
        for sel_region in sel_it:
            cursor = sel_region.a

            for sym_region, sym_string in sym_it:
                if point_past_region_boundary(cursor, sym_region, not forward):
                    continue  # inner

                self.specify_region_by_selector(sym_region, symbol_selector)

                if point_past_region_boundary(cursor, sym_region, forward):
                    break  # inner
            else:
                break  # outer

            sel.add(sym_region)

        self.fixup_empty_selection(not forward)  # fallback cursor at bof/eof
        self.view.show(sel[-forward])

    def specify_region_by_selector(self, region, selector):
        step = 1 if (region.a < region.b) else -1
        a, b = (region.a, region.b)[::step]

        score_selector = self.view.score_selector

        for a in range(a, b, 1):
            if score_selector(a, selector):
                break

        for b in range(b, a, -1):
            if score_selector(b-1, selector):
                break

        region.a, region.b = (a, b)[::step]

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

