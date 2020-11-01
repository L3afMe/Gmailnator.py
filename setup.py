# ##############################################################################
#                                                                              #
#  Clover - setup.py                                                           #
#  Copyright (C) 2020 L3af                                                     #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify it     #
#  under the terms of the GNU General Public License as published by the       #
#  Free Software Foundation, either version 3 of the License, or (at your      #
#  option) any later version.                                                  #
#                                                                              #
#  This program is distributed in the hope that it will be useful, but         #
#  WITHOUT ANY WARRANTY; without even the implied warranty of                  #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See  the GNU General   #
#  Public License for more details.                                            #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program. If not, see <https://www.gnu.org/licenses/>.       #
#                                                                              #
# ##############################################################################
from setuptools import setup

setup(
        name = 'gmailnator.py',
        version = '1.0.1',
        description = 'Python wrapper to access Gmailnator programmatically',
        long_description = open('README').read(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/L3afMe/Gmailnator.py',
        author = 'L3afMe',
        author_email = 'L3afMeAlon3@gmail.com',
        license = 'GNU GPLv3 or later',
        packages = ['gmailnator'],
        include_package_data = True,
        install_requires = []
)
