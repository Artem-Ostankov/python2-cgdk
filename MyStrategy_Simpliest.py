from math import *
from model.ActionType import ActionType

STRIKE_ANGLE = pi / 180.0

class MyStrategy:
    def move(self, me, world, game, move):
        if world.puck.owner_hockeyist_id == me.id:
            opPlayer = world.get_opponent_player()
            netX = 0.5 * (opPlayer.net_back + opPlayer.net_front)
            netY = 0.5 * (opPlayer.net_left + opPlayer.net_right)
            angleToNet = me.get_angle_to(netX, netY)

            move.turn = angleToNet

            if (abs(angleToNet) < STRIKE_ANGLE):
                move.action = ActionType.STRIKE
        else:
            move.speed_up = 1.0
            move.turn = me.get_angle_to(world.puck.x, world.puck.y)
            move.action = ActionType.TAKE_PUCK

