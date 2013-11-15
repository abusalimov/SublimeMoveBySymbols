"""
Highlights symbols during navigation.
"""

import sublime, sublime_plugin

import collections

ST3 = (int(sublime.version()) >= 3000)


class Highlighting(object):

    def __init__(self, view, symbols, scope=None):
        super(Highlighting, self).__init__()
        self.view = view
        self.sel = list(view.sel())
        self.regions = collections.defaultdict(list)

        if scope:
            self.regions[scope] = symbols
        else:
            for symbol in symbols:
                symbol_scope = self.view.scope_name(symbol.begin())
                self.regions[symbol_scope].append(symbol)

    def highlight(self, style="outline"):
        for region_scope, regions in self.regions.items():
            self.view.add_regions('move_by_symbols : ' + region_scope,
                                  regions, region_scope, "",
                                  prepare_draw_flags(style))

    def clear(self, regions=None):
        for region_scope in self.regions:
            self.view.erase_regions('move_by_symbols : ' + region_scope)


if ST3:
    def prepare_draw_flags(style):
        draw_flags = 0
        if style != "fill":     draw_flags |= sublime.DRAW_NO_FILL
        if style != "outline":  draw_flags |= sublime.DRAW_NO_OUTLINE
        return draw_flags
else:
    def prepare_draw_flags(style):
        draw_flags = 0
        if style == "outline":  draw_flags |= sublime.DRAW_OUTLINED
        return draw_flags


view_highlightings = {}

def add_highlighting(view, symbols, scope=None, style="outline", timeout=None):
    erase_highlighting(view)

    highlighting = Highlighting(view, symbols, scope)
    if timeout is not None:
        sublime.set_timeout(lambda: erase_highlighting(view, highlighting),
                            timeout)
        view_highlightings[view.id()] = highlighting

    highlighting.highlight(style)

def erase_highlighting(view, only_highlighting=None):
    highlighting = view_highlightings.get(view.id())

    if (only_highlighting is not None and
        only_highlighting is not highlighting):
        return  # highlighting changed
    if highlighting is None:
        return  # nothing highlighted

    highlighting.clear()
    del view_highlightings[view.id()]


class SymbolHighlightingEvents(sublime_plugin.EventListener):

    def on_modified(self, view):
        erase_highlighting(view)

    def on_selection_modified(self, view):
        highlighting = view_highlightings.get(view.id())
        if highlighting is not None and highlighting.sel != list(view.sel()):
            erase_highlighting(view)

    def on_deactivated(self, view):
        erase_highlighting(view)

    def on_close(self, view):
        erase_highlighting(view)

