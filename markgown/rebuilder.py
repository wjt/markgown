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

import os.path
import subprocess

from gi.repository import Gio, GObject

class Rebuilder(GObject.Object):
    __gsignals__ = {
        'rebuilt': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
                          ())
    }

    def __init__(self, path, html_path):
        GObject.Object.__init__(self)

        self.path = path
        self.html_path = html_path

        self.file = Gio.File.new_for_path(path)
        self.monitor = self.file.monitor(
            flags=Gio.FileMonitorFlags.NONE, cancellable=None)
        self.monitor.connect('changed', self.__changed_cb)

    def __changed_cb(self, monitor, file, other_file, event_type):
        if event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            self.rebuild()

    def build(self, destination, self_contained=False):
        css_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'markdown.css'))

        pandoc = subprocess.Popen(["pandoc", "-s", "--smart", "--toc",
                                   "--css=%s" % css_path] +
                                  (["--self-contained"] if self_contained else []) + 
                                  [self.path, "-o", destination])
        pandoc.wait()

    def rebuild(self):
        self.build(self.html_path)
        self.emit('rebuilt')

