from Docker import *
from gi.repository import Gtk, Gdk, Gio
import locale
import os
from locale import gettext as _
import locale
import gi
gi.require_version("Gtk", "3.0")

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
        self.window.show_all()

    def define_components(self):
        # stacks
        self.main_stack = self.builder.get_object("main_stack")

        # windows
        self.images_window = self.builder.get_object("images_window")
        self.containerappwindow = self.builder.get_object("containerappwindow")

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

    def show_images(self, widget):
        self.main_stack.set_visible_child_name("images_page")

    def show_container(self, widget):
        self.main_stack.set_visible_child_name("container_page")

    def show_volume(self, widget):
        # self.main_stack.set_visible_child_name("container_page")
        pass

    def plus_button(self, widget):
        if "images_page" == self.main_stack.get_visible_child_name():
            self.images_window.set_application()
            self.images_window.show()
        elif "container_page" == self.main_stack.get_visible_child_name():
            self.imagesappwindow.set_application()
            self.imagesappwindow.show()
        else:
            pass


if __name__ == "__main__":
    app = MainWindow()
    Gtk.main()
