# Fuel4TheLight
# Copyright (C) 2017  Oscar Triano @cat_dotoscat

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from enum import IntFlag
S = 8. #Size unit

#virtual screen
VWIDTH = 240
VHEIGHT = 160

SPEED = 64.0
JUMP = 128.0

class Type(IntFlag):
    PLAYER = 1
    POWERUP = 2

PLATFORM_PER_SEC = 2.
ENGINE_SPEED = 8.
GRAVITY = VWIDTH
