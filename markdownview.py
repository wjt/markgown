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

from gi.repository import Gtk, WebKit, GObject

class MarkdownView(Gtk.ScrolledWindow):
    __gsignals__ = {
        'title-changed': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
                          (GObject.TYPE_STRING,))
    }

    def __init__(self, url):
        Gtk.ScrolledWindow.__init__(self)

        self.url = url
        self.loaded = False

        self.web = WebKit.WebView()
        self.add(self.web)

        self.web.connect('notify::title', self.__notify_title_cb)

    def __notify_title_cb(self, *args):
        self.emit('title-changed', self.web.get_title())

    def refresh(self):
        if self.loaded:
            self.web.reload()
        else:
            self.web.load_uri(self.url)
            self.loaded = True
