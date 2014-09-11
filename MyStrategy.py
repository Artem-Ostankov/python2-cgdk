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

    #static
    top = None

    #local
    partner = None

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


        if self.partner is None:
            for hock in world.hockeyists:
                if hock.player_id == world.get_my_player().id and hock.id != me.id and hock.teammate_index != 2:
                    logging.warning("t:{}".format(hock.teammate_index))
                    self.partner = hock




        if me.id == MyStrategy.top:
            if world.puck.owner_hockeyist_id != me.id:
                self.getPuck(me, world, game, move)
                return

        if self.getToHitPosition(me, world, game, move):

            if MyStrategy.top == me.id:
                if world.puck.owner_hockeyist_id == me.id:
                    if self.lookPartner(me, world, game, move) < pi/180:
                        move.action = ActionType.PASS
            else:
                if world.puck.owner_hockeyist_id == me.id:
                    self.strikeNet(me, world, game, move)
                else:
                    if self.lookPartner(me, world, game, move) < pi/180:
                        if me.get_distance_to_unit(world.puck) < game.stick_length:
                            move.action = ActionType.TAKE_PUCK


    def getPuck(self, me, world, game, move):
        distancePos = me.get_distance_to_unit(world.puck)

        if distancePos < game.stick_length:
            move.action = ActionType.TAKE_PUCK
        else:
            move.turn = me.get_angle_to_unit(world.puck)
            move.speed_up = 1.0

    def getToHitPosition(self, me, world, game, move):
        myAimY = game.rink_top  if me.id == MyStrategy.top else game.rink_bottom
        myAimX = (game.rink_left + game.rink_right) / 2
        distancePos = me.get_distance_to(myAimX,  myAimY)

        if distancePos > me.radius + 60:
            direct = me.get_angle_to(myAimX,  myAimY)
            move.turn = direct
            if direct < pi/ 180:
                move.speed_up = 0.5
            return False
        return True

    def getPartner(self, me, world, game, move):
        for hock in world.hockeyists:
            if hock.player_id == world.get_my_player().id and hock.id != me.id and hock.teammate_index != 2:
                return hock

    def lookPartner(self, me, world, game, move):
        partnerAn = me.get_angle_to_unit(self.getPartner(me, world, game, move))
        move.turn = partnerAn
        return abs(partnerAn)

    def strikeNet(self, me, world, game, move):
        opNetX = (world.get_opponent_player().net_left + world.get_opponent_player().net_right) / 2
        opNetY = (world.get_opponent_player().net_bottom + world.get_opponent_player().net_top) / 2
        opNetY += (0.5 if me.y < opNetY else -0.5) * game.goal_net_height;
        move.turn = me.get_angle_to(opNetX, opNetY)
        move.action= ActionType.SWING
        if abs(me.get_angle_to(opNetX, opNetY)) < pi/180:
            move.action = ActionType.STRIKE
