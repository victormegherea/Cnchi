#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bootloader.py
#  
#  Copyright 2013 Antergos
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Antergos Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Raúl Granados (pollitux) <raulgranados.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#   Marc Miralles (arcnexus) <arcnexus.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>

from gi.repository import Gtk, GObject

import subprocess
import os
import logging

class BootLoader():
    def __init__(self, settings):
        self.ui_dir = settings.get('UI_DIR')
        self.ui = Gtk.Builder()

        self.ui.add_from_file(os.path.join(self.ui_dir, "bootloader.ui"))
        self.ui.connect_signals(self)
        
        self.btns = {}
        self.btns["GRUB2"] = self.ui.get_object("GRUB2")
        self.btns["UEFI_x86_64"] = self.ui.get_object("UEFI_x86_64")
        self.btns["UEFI_i386"] = self.ui.get_object("UEFI_i386")
        
        # set bios as default
        self.btns["GRUB2"].set_active(True)

        self.dialog = self.ui.get_object("bootloader")
        self.title = self.ui.get_object("title")
        self.translate_ui()

    def translate_ui(self):
        txt = _("What is your boot system type?")
        txt = '<span weight="bold" size="large">%s</span>' % txt
        self.title.set_markup(txt)

        label = self.ui.get_object("GRUB2_label")
        txt = _("BIOS (Common)")
        txt = '<span weight="bold">%s</span>' % txt
        label.set_markup(txt)

        label = self.ui.get_object("UEFI_x86_64_label")
        txt = _("x86_64 UEFI")
        label.set_markup(txt)

        label = self.ui.get_object("UEFI_i386_label")
        txt = _("i386 UEFI")
        label.set_markup(txt)
        
    def get_type(self):
        for k in self.btns:
            if self.btns[k].get_active():
                return k
        return ""

    def run(self):
        bootloader_type = ""
        response = self.dialog.run()
        
        if response == Gtk.ResponseType.OK:
            bootloader_type = self.get_type()
        else:
            print("Cancel or close")

        self.dialog.hide()
        
        return bootloader_type

    def ask(self):
        # Ask bootloader type (don't know if it must be done here or after)
            bootloader_type = bl.run()
            
            if len(bootloader_type) > 0:
                self.settings.set('install_bootloader', True)
                self.settings.set('bootloader_type', bootloader_type)
                logging.info(_("Cnchi will install a %s bootloader") % bootloader_type)
            else:
                self.settings.set('install_bootloader', False)
