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
    field_div = None

    #local
    partner = None
    cur_loop = 0
    looks_on_aim = False

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

        MyStrategy.field_div = (world.get_my_player().net_front - world.get_opponent_player().net_front - 100) / 10
        MyStrategy.div_mult = -1 if world.get_my_player().net_front > world.get_opponent_player().net_front else 1
        MyStrategy.field_div *= MyStrategy.div_mult



        if self.partner is None:
            for hock in world.hockeyists:
                if hock.player_id == world.get_my_player().id and hock.id != me.id and hock.teammate_index != 2:
                    logging.warning("t:{}".format(hock.teammate_index))
                    self.partner = hock




        if me.id == MyStrategy.top:
            if world.puck.owner_hockeyist_id != me.id:
                self.getPuck(me, world, game, move)
                return

            myAimY = game.goal_net_top
            myAimX = (world.get_my_player().net_front + (50* MyStrategy.div_mult)) + (MyStrategy.field_div * self.cur_loop)
            # logging.warning("x:{}".format(myAimX))
            if self.getToHitPosition(me, world, game, move, myAimX, myAimY):
                self.strikeNet(me, world, game, move)


    def getPuck(self, me, world, game, move):
        distancePos = me.get_distance_to_unit(world.puck)

        if distancePos < game.stick_length:
            move.action = ActionType.TAKE_PUCK
        else:
            move.turn = me.get_angle_to_unit(world.puck)
            move.speed_up = 1.0

    def getToHitPosition(self, me, world, game, move, myAimX, myAimY):

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

    def lookNet(self, me, world, game, move):
        opNetX = (world.get_opponent_player().net_left + world.get_opponent_player().net_right) / 2
        opNetY = (world.get_opponent_player().net_bottom + world.get_opponent_player().net_top) / 2
        opNetY += (0.5 if me.y < opNetY else -0.5) * game.goal_net_height;
        move.turn = me.get_angle_to(opNetX, opNetY)
        if abs(me.get_angle_to(opNetX, opNetY)) < pi/180:
            move.action= ActionType.SWING
            self.looks_on_aim = True

    def strikeNet(self, me, world, game, move):
        opNetX = (world.get_opponent_player().net_left + world.get_opponent_player().net_right) / 2
        opNetY = (world.get_opponent_player().net_bottom + world.get_opponent_player().net_top) / 2
        opNetY += (0.5 if me.y < opNetY else -0.5) * game.goal_net_height;
        move.turn = me.get_angle_to(opNetX, opNetY)

        logging.warning("{} : {}".format(self.looks_on_aim, me.last_action_tick ))
        if abs(me.get_angle_to(opNetX, opNetY)) < pi/180:

            if self.looks_on_aim and me.last_action_tick > 20:
                # move.action = ActionType.STRIKE
                # self.looks_on_aim = False
                self.cur_loop += 1
            else:
                move.action= ActionType.SWING
                self.looks_on_aim = True

            
            
