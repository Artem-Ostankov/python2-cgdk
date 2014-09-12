from __future__ import division
from math import *
from model.ActionType import ActionType
from model.Game import Game
from model.Hockeyist import Hockeyist
from model.Move import Move
from model.World import World
from model.HockeyistState import HockeyistState
from model.HockeyistType import HockeyistType

STRIKE_ANGLE = pi / 180.0

class MyStrategy:
    def move(self, me, world, game, move):
        """
        @type me: Hockeyist
        @type world: World
        @type game: Game
        @type move: Move
        """
        if(me.state == HockeyistState.SWINGING):
            move.action = ActionType.STRIKE
            return

        if world.puck.owner_player_id == me.player_id:
            if world.puck.owner_hockeyist_id == me.id:
                opPlayer = world.get_opponent_player()
                netX = 0.5 * (opPlayer.net_back + opPlayer.net_front)
                netY = 0.5 * (opPlayer.net_bottom + opPlayer.net_top)

                netY += (0.5 if me.y < netY else -0.5) * game.goal_net_height

                angleToNet = me.get_angle_to(netX, netY)
                move.turn = angleToNet

                if (abs(angleToNet) < STRIKE_ANGLE):
                    move.action = ActionType.SWING
            else:
                nearestOp = self.getNearestOpponent(me.x, me.y, world)
                if nearestOp is not None:
                    if me.get_distance_to_unit(nearestOp) > game.stick_length:
                        move.speed_up = 1.0
                    elif abs(me.get_angle_to_unit(nearestOp)) < 0.5 * game.stick_sector:
                        move.action = ActionType.STRIKE

                    move.turn = me.get_angle_to_unit(nearestOp)

        else:
            move.speed_up = 1.0
            move.turn = me.get_angle_to(world.puck.x, world.puck.y)
            move.action = ActionType.TAKE_PUCK


    def getNearestOpponent(self, x, y, world):
        """
        @type x: float
        @type y: float
        @type world: World
        """

        nearestOp = None
        nearestOpRange = 0

        for hock in world.hockeyists:
            if hock.teammate or hock.type == HockeyistType.GOALIE or \
                        hock.state == HockeyistState.KNOCKED_DOWN or hock.state == HockeyistState.RESTING:
                continue

            opRange = hypot(x- hock.x, y - hock.y)

            if nearestOp is None or opRange < nearestOpRange:
                nearestOp = hock
                nearestOpRange = opRange

        return nearestOp

