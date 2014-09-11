from __future__ import division
from math import *
from model.ActionType import ActionType
from model.Hockeyist import Hockeyist
from model.World import World
import model.Game
import model.Move
import model.HockeyistState
import model.Player
import logging


class MyStrategy:

    top = None

    def move(self, me, world, game, move):
        """
        @type me:Hockeyist
        @type world:World
        @type game:Game
        @type move:Move
        """

        # for h in world.hockeyists:

        if MyStrategy.top is None:
            MyStrategy.top = me.id

        myNetX = (world.get_my_player().net_left + world.get_my_player().net_right) / 2
        myNetY = (world.get_my_player().net_bottom + world.get_my_player().net_top) / 2

        myNetAimY = world.get_my_player().net_top if me.id == MyStrategy.top else world.get_my_player().net_bottom
        distancePos = me.get_distance_to(world.get_my_player().net_front,  myNetAimY)

        if distancePos > me.radius + 5:
            direct = None
            if me.id == MyStrategy.top:
                direct = me.get_angle_to(world.get_my_player().net_front,  myNetAimY)
            else :
                direct = me.get_angle_to(world.get_my_player().net_front,  myNetAimY)
            move.turn = -direct

            if direct < pi/ 180:
                move.speed_up = -1.0
        else :
            move.turn = me.get_angle_to_unit(world.puck)

        distancePuck = me.get_distance_to_unit(world.puck)

        logging.warn(me.radius)
        logging.warn(distancePos)

        if distancePuck < game.stick_length:
            move.action = ActionType.TAKE_PUCK
