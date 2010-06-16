# Orca
#
# Copyright 2010 Informal Informatica LTDA.
# Author: Jose Vilmar <vilmar@informal.com.br>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""Custom script for Eclipse."""
__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2010 Informal Informatica LTDA."
__license__   = "LGPL"

import orca.default as default
import pyatspi
from script_utilities import Utilities

########################################################################
#                                                                      #
# The Eclipse script class.                                            #
#                                                                      #
########################################################################
class Script(default.Script):

    def __init__(self, app):
        """Creates a new script for the given application."""
        default.Script.__init__(self, app)
        self.movementKeys = ["Up", "Down", "Left", "Right", "Page_Up",
                   "Page_Down", "Home", "End"]

    def _presentTextAtNewCaretPosition(self, event, otherObj=None):
        """Updates braille, magnification, and outputs speech for the
        event.source or the otherObj. Overridden here so that we can
        give more feedback to user
        """

        if self.utilities.isDuplicateEvent(event):
            return

        # Let the default script's normal behavior do its thing
        #
        default.Script._presentTextAtNewCaretPosition(self, event, otherObj)

        # check if the obj was spoken in the default script
        lastKey, mods = self.utilities.lastKeyAndModifiers()
        if lastKey in self.movementKeys:
            # already spoken in default script
            return

        obj = otherObj or event.source
        if obj.getState().contains(pyatspi.STATE_SINGLE_LINE):
            return

        self.sayLine(obj)
        self._saveLastTextPosition(obj)

    def onFocus(self, event):
        """Called whenever an object gets focus.  Overridden here so that
        so that we can avoid speaking text when caret moves after new text
        receives focus and is spoken.

        Arguments:
        - event: the Event
        """

        # Let the default script's normal behavior do its thing
        #
        default.Script.onFocus(self, event)

        self._saveLastTextPosition(event.source)

    def getUtilities(self):
        """Returns the utilities for this script."""

        return Utilities(self)

    def onTextInserted(self, event):
        """Called whenever text is inserted into an object. Overridden here
        so that we can avoid speaking text when caret moves after new text
        is inserted.

        Arguments:
        - event: the Event
        """

        # Let the default script's normal behavior do its thing
        #
        default.Script.onTextInserted(self, event)
        self._saveLastTextPosition(event.source)

    def onTextDeleted(self, event):
        """Called whenever text is deleted from an object.  Overridden here
        so that we can avoid speaking text when caret moves after new text
        is deleted.

        Arguments:
        - event: the Event
        """

        # Let the default script's normal behavior do its thing
        #
        default.Script.onTextDeleted(self, event)
        self._saveLastTextPosition(event.source)

    def _saveLastTextPosition(self, obj):
        if self.utilities.isTextArea(obj):
            self._saveLastCursorPosition(obj, obj.queryText().caretOffset)


