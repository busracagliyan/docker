import gi
gi.require_version("Gtk", "3.0")
from Docker import *
from gi.repository import Gtk, Gdk, Gio
import locale
import os
from locale import gettext as _
import locale


# Translation Constants:
APPNAME = "docker-gui"
TRANSLATIONS_PATH = "/usr/share/locale"
SYSTEM_LANGUAGE = os.environ.get("LANG")

# Translation functions:
locale.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
locale.textdomain(APPNAME)
locale.setlocale(locale.LC_ALL, SYSTEM_LANGUAGE)


class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(APPNAME)
        self.builder.add_from_file(os.path.dirname(
            os.path.abspath(__file__)) + "/MainWindow.glade")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.window.set_application()
        self.window.connect("destroy", self.onDestroy)

        self.define_components()

        self.docker = docker()

        self.plus_btn.connect("clicked", self.plus_button)
        self.images_btn.connect("clicked", self.show_images)
        self.container_btn.connect("clicked", self.show_container)
        self.volume_btn.connect("clicked", self.show_volume)
        self.show_container(self.container_btn)
        self.window.show_all()

    def define_components(self):
        # stacks
        self.main_stack = self.builder.get_object("main_stack")

        # windows
        self.images_window = self.builder.get_object("images_window")
        self.containers_window = self.builder.get_object("containers_window")

        # lists
        self.images_list = self.builder.get_object("images_list")
        self.container_list = self.builder.get_object("container_list")

        # texts
        self.img_name_txt = self.builder.get_object("images_name_text")
        self.img_option_txt = self.builder.get_object("images_option_text")
        self.cnt_name_txt = self.builder.get_object("container_name_text")
        self.cnt_option_txt = self.builder.get_object("container_option_text")

        # buttons
        self.images_btn = self.builder.get_object("images_button")
        self.container_btn = self.builder.get_object("container_button")
        self.volume_btn = self.builder.get_object("volume_button")
        self.plus_btn = self.builder.get_object("plus_button")
        self.menu_btn = self.builder.get_object("menu_button")
        self.add_image_btn = self.builder.get_object("images_add_button")
        self.add_container_btn = self.builder.get_object(
            "container_add_button")

        self.popovermenu = self.builder.get_object("gtkpopovermenu")

    def onDestroy(self, widget):
        Gtk.main_quit()

    def update_stack_button(self,widget):
        self.images_btn.set_sensitive(True)
        self.container_btn.set_sensitive(True)
        self.volume_btn.set_sensitive(True)
        widget.set_sensitive(False)

    def show_images(self, widget):
        self.main_stack.set_visible_child_name("images_page")
        self.update_stack_button(widget)

    def show_container(self, widget):
        self.main_stack.set_visible_child_name("containers_page")
        self.update_stack_button(widget)

    def show_volume(self, widget):
        self.main_stack.set_visible_child_name("volumes_page")
        self.update_stack_button(widget)

    def plus_button(self, widget):
        if "images_page" == self.main_stack.get_visible_child_name():
            self.images_window.set_application()
            self.images_window.show()
        elif "containers_page" == self.main_stack.get_visible_child_name():
            self.containers_window.set_application()
            self.containers_window.show()
        else:
            pass


if __name__ == "__main__":
    app = MainWindow()
    Gtk.main()
