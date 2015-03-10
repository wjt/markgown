#!/usr/bin/python
# vim: set fileencoding=utf-8 :
#
# © 2012–2015 Will Thompson <will@willthompson.co.uk>
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

import os.path
import sys
import tempfile

from gi.repository import Gtk, Gio, WebKit

from rebuilder import Rebuilder

class ViewerWindow(Gtk.ApplicationWindow):
    def __init__(self, md_filename):
        Gtk.ApplicationWindow.__init__(self)

        self.set_default_size(768, 600)
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.set_titlebar(self.hb)

        self.filename = md_filename
        html_file = tempfile.NamedTemporaryFile(prefix=os.path.basename(md_filename), suffix='.html')
        # TODO: close (and hence delete) on destroy

        self.web_view = WebKit.WebView()
        self.web_view.load_uri('file://' + html_file.name)
        self.web_view.connect('notify::title', self.__title_changed_cb)
        sw = Gtk.ScrolledWindow()
        sw.add(self.web_view)
        self.add(sw)

        self.rebuilder = Rebuilder(self.filename, html_file.name)
        self.rebuilder.connect('rebuilt', self.__rebuilt_cb)
        self.rebuilder.rebuild()

        self.show_all()

    def __rebuilt_cb(self, rebuilder):
        self.web_view.reload()

    def __title_changed_cb(self, *args):
        title = self.web_view.get_title()

        if title is None:
            self.hb.set_title(self.filename)
            self.hb.set_subtitle(None)
        else:
            self.hb.set_title(title)
            self.hb.set_subtitle(self.filename)


class ViewerApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id="uk.me.wjt.markgownviewer",
                                 flags=Gio.ApplicationFlags.HANDLES_OPEN)

        self.connect("open", ViewerApp.__open_cb)

    def __open_cb(self, g_files, n_g_files, hint):
        for g_file in g_files:
            w = ViewerWindow(g_file.get_path())
            self.add_window(w)

if __name__ == '__main__':
    app = ViewerApp()
    app.run(sys.argv)
