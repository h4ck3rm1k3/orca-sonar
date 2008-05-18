# Orca
#
# Copyright 2004-2008 Sun Microsystems Inc.
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

""" Custom script for Thunderbird 3.
"""

__id__        = "$Id: $"
__version__   = "$Revision: $"
__date__      = "$Date: $"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import pyatspi

import orca.orca as orca
import orca.debug as debug
import orca.default as default
import orca.speech as speech
import orca.scripts.toolkits.Gecko as Gecko

from orca.orca_i18n import _

from speech_generator import SpeechGenerator

########################################################################
#                                                                      #
# The Thunderbird script class.                                        #
#                                                                      #
########################################################################

class Script(Gecko.Script):
    """The script for Thunderbird."""

    _containingPanelName = ""

    def __init__(self, app):
        """ Creates a new script for the given application.

        Arguments:
        - app: the application to create a script for.
        """

        # Set the debug level for all the methods in this script.
        self.debugLevel = debug.LEVEL_FINEST

        Gecko.Script.__init__(self, app)

    def getSpeechGenerator(self):
        """Returns the speech generator for this script.
        """
        return SpeechGenerator(self)

    def _debug(self, msg):
        """ Convenience method for printing debug messages
        """
        debug.println(self.debugLevel, "Thunderbird.py: "+msg)

    def onFocus(self, event):
        """ Called whenever an object gets focus.

        Arguments:
        - event: the Event

        """
        obj = event.source
        parent = obj.parent
        top = self.getTopLevel(obj)
        consume = False

        # Don't speak chrome URLs.
        #
        if obj.name.startswith("chrome://"):
            return

        # This is a better fix for bug #405541. Thunderbird gives
        # focus to the cell in the column that is being sorted
        # (e.g., Date). Braille should show the row from the begining.
        # This fix calls orca.setLocusOfFocus to give focus to the
        # cell at the beginning of the row. It consume the event
        # so Gecko.py doesn't reset the focus.
        #
        if obj.getRole() == pyatspi.ROLE_TABLE_CELL:
            table = parent.queryTable()
            row = table.getRowAtIndex(obj.getIndexInParent())
            acc = table.getAccessibleAt(row, 0)
            orca.setLocusOfFocus(event, acc)
            consume = True

        # Handle dialogs.
        #
        if top and top.getRole() == pyatspi.ROLE_DIALOG:
            self._speakEnclosingPanel(obj)

        if not consume:
            Gecko.Script.onFocus(self, event)

    def onStateChanged(self, event):
        """Called whenever an object's state changes.

        Arguments:
        - event: the Event
        """

        # For now, we'll bypass the Gecko script's desire to let
        # someone know when a page has started/completed loading.  The
        # reason for this is that getting message content from someone
        # is counted as loading a page.
        #
        default.Script.onStateChanged(self, event)

    def onTextInserted(self, event):
        """Called whenever text is inserted into an object.

        Arguments:
        - event: the Event
        """
        obj = event.source
        parent = obj.parent

        if parent.getRole() == pyatspi.ROLE_AUTOCOMPLETE:
            # Thunderbird does not present all the text in an
            # autocompletion text entry. This is a workaround.
            #
            speech.stop()

            utterances = []
            [text, caretOffset, startOffset] = self.getTextLineAtCaret(obj)
            utterances.append(text)
            self._debug("onTextInserted: utterances='%s'" % utterances)

            speech.speakUtterances(utterances)
        else:
            Gecko.Script.onTextInserted(self, event)

    def onVisibleDataChanged(self, event):
        """Called when the visible data of an object changes."""

        # [[[TODO: JD - In Gecko.py, we need onVisibleDataChanged() to
        # to detect when the user switches between the tabs holding
        # different URLs in Firefox.  Thunderbird issues very similar-
        # looking events as the user types a subject in the message
        # composition window. For now, rather than trying to distinguish
        # them  in Gecko.py, we'll simply prevent Gecko.py from seeing when
        # Thunderbird issues such an event.]]]
        #
        return

    def _speakEnclosingPanel(self, obj):
        """Speak the enclosing panel for the object, if it is
        named. Going two containers up the hierarchy appears to be far
        enough to find a named panel, if there is one.  Don't speak
        panels whose name begins with 'chrome://'"""

        self._debug("_speakEnclosingPanel")

        parent = obj.parent
        if not parent:
            return

        if parent.name != "" \
            and (not parent.name.startswith("chrome://")) \
            and (parent.getRole() == pyatspi.ROLE_PANEL):

            # Speak the parent panel name, but only once.
            #
            if parent.name != self._containingPanelName:
                self._containingPanelName = parent.name
                utterances = []
                # Translators: this is the name of a panel in Thunderbird.
                #
                text = _("%s panel") % parent.name
                utterances.append(text)
                speech.speakUtterances(utterances)
        else:
            grandparent = parent.parent
            if grandparent \
                and (grandparent.name != "") \
                and (not grandparent.name.startswith("chrome://")) \
                and (grandparent.getRole() == pyatspi.ROLE_PANEL):

                # Speak the grandparent panel name, but only once.
                #
                if grandparent.name != self._containingPanelName:
                    self._containingPanelName = grandparent.name
                    utterances = []
                    # Translators: this is the name of a panel in Thunderbird.
                    #
                    text = _("%s panel") % grandparent.name
                    utterances.append(text)
                    speech.speakUtterances(utterances)

    def isLineBreakChar(self, obj, offset):
        """Returns True of the character at the given offset within
        obj is a newline.
        """

        char = self.getCharacterAtOffset(obj, offset)
        return char == "\n"