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
