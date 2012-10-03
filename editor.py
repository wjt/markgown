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

from gi.repository import Gtk, GtkSource, Pango

class MarkdownSourceView(GtkSource.View):
    def __init__(self, b):
        GtkSource.View.__init__(self)

        self.set_wrap_mode(Gtk.WrapMode.WORD)

        desc = Pango.FontDescription()
        desc.set_family('monospace')
        self.modify_font(desc)

        self.set_buffer(b)

class MarkdownBuffer(GtkSource.Buffer):
    def __init__(self, initial_data):
        GtkSource.Buffer.__init__(self)

        self.set_language(
            GtkSource.LanguageManager.get_default().get_language('markdown'))
        self.set_text(initial_data.strip())
        self.set_modified(False)
