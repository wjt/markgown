#!/usr/bin/python
# vim: set fileencoding=utf-8 :
#
# © 2012 Will Thompson <will@willthompson.co.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GLib, Gtk, Gio, GObject

from markdownview import MarkdownView
from pips import Pips
from sourceview import MarkdownSourceView, MarkdownBuffer
from rebuilder import Rebuilder

import os.path
import sys

class MarkgownWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        self.filename = os.path.realpath(sys.argv[1])
        self.loaded = False

        base, _ = os.path.splitext(self.filename)
        # FIXME: make this a dotfile? delete it on quit?
        self.html_file = "%s.html" % base

        self.set_default_size(1000, 600)
        paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        self.add(paned)

        sw = Gtk.ScrolledWindow()

        self.b = MarkdownBuffer(self.filename)
        view = MarkdownSourceView(self.b)
        sw.add(view)

        overlay = Gtk.Overlay()
        overlay.add(sw)

        self.spinner = Pips()
        self.spinner.set_halign(Gtk.Align.END)
        self.spinner.set_valign(Gtk.Align.END)
        overlay.add_overlay(self.spinner)

        paned.add1(overlay)

        self.markdownview = MarkdownView(url=('file://' + self.html_file))
        self.markdownview.connect('title_changed', self.title_changed_cb)
        paned.add2(self.markdownview)

        paned.set_position(600)

        self.show_all()

        self.rebuilder = Rebuilder(self.filename, self.html_file)
        self.rebuilder.connect('rebuilt', lambda *args: self.markdownview.refresh())
        self.rebuilder.rebuild()

        self.b.connect('modified-changed', lambda args: self.check_modified())
        self.check_modified()

        self.connect('delete-event', self.__check_save)

    def __check_save(self, *args):
        if self.b.get_modified():
            self.save()

        return False

    def save(self):
        self.b.save()
        return False

    def check_modified(self):
        if self.b.get_modified():
            GLib.timeout_add_seconds(5, self.save)
            self.spinner.count_down_from(5)
            self.spinner.show()
        else:
            self.spinner.hide()

    def title_changed_cb(self, view, title):
        if title is None:
            title = self.filename
        else:
            title = '%s (%s)' % (title, self.filename)

        self.set_title(title)

if __name__ == '__main__':
    window = MarkgownWindow()
    window.connect('destroy', Gtk.main_quit)
    Gtk.main()
