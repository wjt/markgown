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

from gi.repository import Gtk, Gio, WebKit2

from rebuilder import Rebuilder


def ff_for_globs(kind, globs):
    ff = Gtk.FileFilter()
    ff.set_name("{} files ({})".format(kind, ", ".join(globs)))
    for glob in globs:
        ff.add_pattern(glob)
    return ff



class ViewerWindow(Gtk.ApplicationWindow):
    def __init__(self, md_filename):
        Gtk.ApplicationWindow.__init__(self)

        self.set_default_size(768, 600)
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.set_titlebar(self.hb)

        open_button = Gtk.Button.new_from_icon_name(
            "document-open-symbolic", Gtk.IconSize.BUTTON)
        open_button.connect('clicked', self.__open_clicked_cb)
        open_button.set_tooltip_text("Open a file")
        self.hb.pack_start(open_button)

        # TODO: neither of these next two icons are quite right
        self.export_button = Gtk.Button.new_from_icon_name(
            "document-send-symbolic", Gtk.IconSize.BUTTON)
        self.export_button.connect('clicked', self.__export_clicked_cb)
        self.export_button.set_sensitive(False)
        self.export_button.set_tooltip_text("Export HTML")
        self.hb.pack_end(self.export_button)

        self.text_plain_app_infos = Gio.AppInfo.get_all_for_type('text/plain')

        self.edit_button = Gtk.Button.new_from_icon_name(
            "send-to-symbolic", Gtk.IconSize.BUTTON)
        self.edit_button.connect('clicked', self.__edit_clicked_cb)
        self.edit_button.set_sensitive(False)
        self.edit_button.set_tooltip_text("Edit file in {}".format(
            self.text_plain_app_infos[0].get_display_name()))
        self.hb.pack_end(self.edit_button)

        self.web_view = WebKit2.WebView()
        self.web_view.connect('notify::title', self.__title_changed_cb)
        sw = Gtk.ScrolledWindow()
        sw.add(self.web_view)
        self.add(sw)

        self.filename = None
        if md_filename is not None:
            self.set_filename(md_filename)

        self.show_all()
        self.__title_changed_cb()

    def set_filename(self, md_filename):
        assert self.filename is None

        self.filename = md_filename
        self.hb.set_subtitle(self.filename)

        self.html_file = tempfile.NamedTemporaryFile(
            prefix=os.path.basename(md_filename),
            suffix='.html')
        self.connect('destroy', ViewerWindow.__destroy_cb)

        self.rebuilder = Rebuilder(self.filename, self.html_file.name,
                                   'mediawiki' if 'mediawiki' in self.filename else 'markdown')
        self.rebuilder.connect('rebuilt', self.__rebuilt_cb)
        self.rebuilder.rebuild()

        self.web_view.load_uri('file://' + self.html_file.name)

        self.export_button.set_sensitive(True)
        self.edit_button.set_sensitive(True)

    def __destroy_cb(self):
        self.html_file.close()

    def __rebuilt_cb(self, rebuilder):
        self.web_view.reload()

    def __title_changed_cb(self, *args):
        title = self.web_view.get_title()

        if not title:
            basename = os.path.basename(self.filename)
            root, _ = os.path.splitext(basename)
            self.hb.set_title(root)
        else:
            self.hb.set_title(title)

    def __open_clicked_cb(self, open_button):
        d = Gtk.FileChooserDialog(
            "Open",
            self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        d.set_local_only(True)
        d.set_select_multiple(True)

        d.add_filter(ff_for_globs("Markdown", [
            "*.md",
            "*.mkd",
            "*.mdwn",
        ]))

        d.add_filter(ff_for_globs("MediaWiki", [
            "*.mediawiki.txt",
        ]))

        ff = Gtk.FileFilter()
        ff.set_name("Text files (let Pandoc guess the format)")
        ff.add_mime_type("text/plain")
        d.add_filter(ff)

        if d.run() == Gtk.ResponseType.OK:
            g_files = d.get_files()
            if self.filename is None and g_files:
                self.set_filename(g_files[0].get_path())
                g_files = g_files[1:]

            for g_file in g_files:
                self.get_application().open(g_file)

        d.destroy()

    def __edit_clicked_cb(self, edit_button):
        self.text_plain_app_infos[0].launch_uris(['file://' + self.filename])

    def __export_clicked_cb(self, export_button):
        d = Gtk.FileChooserDialog(
            "Export as HTML",
            self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        d.set_local_only(True)
        suggested = os.path.splitext(self.filename)[0] + '.html'
        if os.path.exists(suggested):
            d.set_filename(suggested)
        else:
            directory, filename = os.path.split(suggested)
            d.set_current_folder(directory)
            d.set_current_name(filename)

        if d.run() == Gtk.ResponseType.OK:
            self.rebuilder.build(d.get_filename(), self_contained=True)

        d.destroy()


class ViewerApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="uk.me.wjt.markgown.viewer",
                                 flags=Gio.ApplicationFlags.HANDLES_OPEN)

        self.connect("activate", ViewerApp.__activate_cb)
        self.connect("open", ViewerApp.__open_cb)

    def __find_window(self, path):
        for w in self.get_windows():
            if w.filename == path:
                return w

        return None

    def open(self, g_file):
        path = g_file.get_path()
        w = self.__find_window(path)
        if w is None:
            w = self.__find_window(None)
            if w is not None:
                w.set_filename(path)
            else:
                w = ViewerWindow(path)
                self.add_window(w)

        w.present_with_time(Gtk.get_current_event_time())

    def __open_cb(self, g_files, n_g_files, hint):
        for g_file in g_files:
            self.open(g_file)

    def __activate_cb(self):
        self.add_window(ViewerWindow(None))
