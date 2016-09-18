#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# controller.py
#
# Copyright © 2013-2016 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" UI Controller """

import importlib

from _base_object import (
    BaseObject,
    Singleton,
    sys
)


class CnchiController(BaseObject, metaclass=Singleton):
    """
    UI Controller

    Class Attributes:
        See also `BaseObject.__doc__`

    """

    modules = []

    def __init__(self, name='main_controller', *args, **kwargs):

        super().__init__(name=name, *args, **kwargs)

        self._initialize_controller()
        self._initialize_pages()

    def _initialize_pages(self):
        first_page = self.controller.pages[0]
        self._pages = {p: {'locked': True} for p in self.controller.pages}
        self._pages[first_page]['locked'] = False

    def _initialize_controller(self):
        ui_module_name = self.settings.ui.module
        ui_module_settings = getattr(self.settings.ui, ui_module_name)
        controller_path = '.{}.{}'.format(ui_module_name, ui_module_settings.controller_path)
        controller_name = '{}Controller'.format(ui_module_name.capitalize())

        controller_module = importlib.import_module(controller_path, 'ui')
        controller = getattr(controller_module, controller_name)

        self.controller = controller()

    def do_restart(self):
        pass

    def exit_app(self):
        sys.exit(0)