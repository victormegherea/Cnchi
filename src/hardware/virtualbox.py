#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  virtualbox.py
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

"""  driver installation """

from hardware import Hardware

DEVICES = [('0x80ee', '0xcafe')]

CLASS_NAME = "Virtualbox"

class Virtualbox(Hardware):
    def __init__(self):
        pass
        
    def get_packages(self):
        return ["virtualbox-guest-utils"]
    
    def chroot(self, cmd):
        __super__().chroot(self, cmd)
    
    def post_install(self, dest_dir):
        path = "%s/etc/modules-load.d/virtualbox-guest.conf" % dest_dir
        with open(path, 'w') as modules:
            modules.write("vboxguest\n")
            modules.write("vboxsf\n")
            modules.write("vboxvideo\n")
        self.chroot(["systemctl", "disable", "openntpd"], dest_dir)
        self.chroot(["systemctl", "enable", "vboxservice"], dest_dir)

    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        if device in DEVICES:
            return True
        return False
