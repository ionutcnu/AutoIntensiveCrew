# -*- coding: utf-8 -*-
"""
Auto Intense Training Mod
Automatically sets WoT Plus intensive crew training to the currently selected vehicle.
"""

import BigWorld
from CurrentVehicle import g_currentVehicle
from helpers import dependency
from skeletons.gui.game_control import IWotPlusController

__author__ = 'Ionut'
__version__ = '1.0.1'


class AutoIntenseTraining(object):
    """Automatically activates intensive crew training for selected vehicle."""

    wotPlusCtrl = dependency.descriptor(IWotPlusController)

    def __init__(self):
        self._enabled = True
        g_currentVehicle.onChanged += self._onVehicleChanged
        BigWorld.logInfo('AutoIntenseTraining', 'Mod initialized v%s' % __version__, None)

    def _onVehicleChanged(self):
        """Called when player selects a different vehicle in garage."""
        if not self._enabled:
            return

        BigWorld.callback(0.5, self._applyIntenseTraining)

    def _applyIntenseTraining(self):
        """Apply intensive training to current vehicle."""
        try:
            if not g_currentVehicle.isPresent():
                return

            if not self.wotPlusCtrl.isEnabled():
                BigWorld.logInfo('AutoIntenseTraining', 'WoT Plus not enabled, skipping', None)
                return

            vehicle = g_currentVehicle.item
            vehicleInvID = vehicle.invID

            # Check if already set for this vehicle
            if self.wotPlusCtrl.hasVehicleCrewIdleXP(vehicleInvID):
                BigWorld.logInfo('AutoIntenseTraining',
                    'Already active for vehicle invID: %d' % vehicleInvID, None)
                return

            # Call the API directly - this bypasses the confirmation dialog
            self.wotPlusCtrl.selectIdleCrewXPVehicle(vehicleInvID)
            BigWorld.logInfo('AutoIntenseTraining',
                'Set intensive training to vehicle invID: %d' % vehicleInvID, None)

        except Exception as e:
            BigWorld.logError('AutoIntenseTraining',
                'Error applying intense training: %s' % str(e), None)

    def fini(self):
        """Cleanup when mod is unloaded."""
        self._enabled = False
        g_currentVehicle.onChanged -= self._onVehicleChanged
        BigWorld.logInfo('AutoIntenseTraining', 'Mod unloaded', None)


g_instance = None


def init():
    """Called by WoT when mod loads."""
    global g_instance
    try:
        g_instance = AutoIntenseTraining()
    except Exception as e:
        BigWorld.logError('AutoIntenseTraining', 'Failed to init: %s' % str(e), None)


def fini():
    """Called by WoT when mod unloads."""
    global g_instance
    if g_instance is not None:
        g_instance.fini()
        g_instance = None
