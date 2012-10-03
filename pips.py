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

from gi.repository import GLib, Gtk

class Pips(Gtk.Label):
    def __init__(self):
        Gtk.Label.__init__(self, None)
        self.__n = 0
        self.__timer = None

    def count_down_from(self, n):
        self.__n = n
        self.__update_label()

        if self.__timer is None:
            self.__timer = GLib.timeout_add_seconds(1, self.__count_down)

    def __update_label(self):
        if self.__n == 0:
            self.set_text('hide me')
            if self.__timer is not None:
                GLib.source_remove(self.__timer)
        else:
            self.set_text('•' * self.__n)

    def __count_down(self):
        self.__n = self.__n - 1
        self.__update_label()
        if self.__n > 0:
            return True
        else:
            self.__timer = None
            return False
