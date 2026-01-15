# -*- coding: utf-8 -*-
"""
Auto Intense Training Mod
Automatically sets WoT Plus intensive crew training to the currently selected vehicle.
"""

import BigWorld
from debug_utils import LOG_DEBUG, LOG_ERROR
from CurrentVehicle import g_currentVehicle
from helpers import dependency
from skeletons.gui.game_control import IWotPlusController

__author__ = 'Ionut'
__version__ = '1.0.8'


def _log(msg):
    LOG_DEBUG('[AutoIntenseTraining] %s' % msg)
    print '[AutoIntenseTraining] %s' % msg


class AutoIntenseTraining(object):
    """Automatically activates intensive crew training for selected vehicle."""

    wotPlusCtrl = dependency.descriptor(IWotPlusController)

    def __init__(self):
        self._enabled = True
        g_currentVehicle.onChanged += self._onVehicleChanged
        _log('init v%s' % __version__)

    def _onVehicleChanged(self):
        """Called when player selects a different vehicle in garage."""
        if not self._enabled:
            return

        _log('vehicle change detected; scheduling apply in 0.5s')
        BigWorld.callback(0.5, self._applyIntenseTraining)

    def _applyIntenseTraining(self):
        """Apply intensive training to current vehicle via direct API (no dialog)."""
        try:
            if not g_currentVehicle.isPresent():
                _log('no vehicle present, skipping')
                return

            if not self.wotPlusCtrl.isEnabled():
                _log('WoT Plus not enabled, skipping')
                return

            vehicle = g_currentVehicle.item
            vehicleInvID = vehicle.invID

            # Skip if already set for this vehicle
            if self.wotPlusCtrl.hasVehicleCrewIdleXP(vehicleInvID):
                _log('already active invID=%d' % vehicleInvID)
                return

            # Direct API call bypasses UI confirmation dialog
            self.wotPlusCtrl.selectIdleCrewXPVehicle(vehicleInvID)
            _log('set invID=%d' % vehicleInvID)

        except Exception as e:
            LOG_ERROR('[AutoIntenseTraining] error: %s' % str(e))
            print '[AutoIntenseTraining] error: %s' % str(e)

    def fini(self):
        """Cleanup when mod is unloaded."""
        self._enabled = False
        g_currentVehicle.onChanged -= self._onVehicleChanged
        _log('unloaded')


g_instance = None


def init():
    """Called by WoT when mod loads."""
    global g_instance
    if g_instance is not None:
        return
    try:
        g_instance = AutoIntenseTraining()
    except Exception as e:
        LOG_ERROR('[AutoIntenseTraining] failed to init: %s' % str(e))
        print '[AutoIntenseTraining] failed to init: %s' % str(e)


def fini():
    """Called by WoT when mod unloads."""
    global g_instance
    if g_instance is not None:
        g_instance.fini()
        g_instance = None


# Ensure initialization even if loader does not invoke init()
try:
    init()
except Exception as e:
    LOG_ERROR('[AutoIntenseTraining] autostart init failed: %s' % str(e))
    print '[AutoIntenseTraining] autostart init failed: %s' % str(e)
