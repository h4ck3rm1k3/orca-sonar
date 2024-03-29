# Orca
#
# Copyright (C) 2010-2011 The Orca Team
# Copyright (C) 2011-2012 Igalia, S.L.
#
# Author: Joanmarie Diggs <jdiggs@igalia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (C) 2010-2011 The Orca Team" \
                "Copyright (C) 2011-2012 Igalia, S.L."
__license__   = "LGPL"

import pyatspi
import pyatspi.utils as utils

import orca.scripts.default as default
import orca.cmdnames as cmdnames
import orca.debug as debug
import orca.guilabels as guilabels
import orca.input_event as input_event
import orca.messages as messages
import orca.orca as orca
import orca.settings as settings
import orca.settings_manager as settings_manager
import orca.speechserver as speechserver
import orca.orca_state as orca_state
import orca.speech as speech

from . import script_settings
from .structural_navigation import StructuralNavigation
from .braille_generator import BrailleGenerator
from .speech_generator import SpeechGenerator
from .script_utilities import Utilities

_settingsManager = settings_manager.getManager()

########################################################################
#                                                                      #
# The WebKitGtk script class.                                          #
#                                                                      #
########################################################################

class Script(default.Script):

    CARET_NAVIGATION_KEYS = ['Left', 'Right', 'Up', 'Down', 'Home', 'End']

    def __init__(self, app, isBrowser=True):
        """Creates a new script for WebKitGtk applications.

        Arguments:
        - app: the application to create a script for.
        """

        default.Script.__init__(self, app)
        self._loadingDocumentContent = False
        self._isBrowser = isBrowser
        self._lastCaretContext = None, -1

        self.sayAllOnLoadCheckButton = None

    def setupInputEventHandlers(self):
        """Defines InputEventHandler fields for this script that can be
        called by the key and braille bindings."""

        default.Script.setupInputEventHandlers(self)
        self.inputEventHandlers.update(
            self.structuralNavigation.inputEventHandlers)

        self.inputEventHandlers["sayAllHandler"] = \
            input_event.InputEventHandler(
                Script.sayAll,
                cmdnames.SAY_ALL)

        self.inputEventHandlers["panBrailleLeftHandler"] = \
            input_event.InputEventHandler(
                Script.panBrailleLeft,
                cmdnames.PAN_BRAILLE_LEFT,
                False) # Do not enable learn mode for this action

        self.inputEventHandlers["panBrailleRightHandler"] = \
            input_event.InputEventHandler(
                Script.panBrailleRight,
                cmdnames.PAN_BRAILLE_RIGHT,
                False) # Do not enable learn mode for this action

    def getToolkitKeyBindings(self):
        """Returns the toolkit-specific keybindings for this script."""

        return self.structuralNavigation.keyBindings

    def getAppPreferencesGUI(self):
        """Return a GtkGrid containing the application unique configuration
        GUI items for the current application."""

        from gi.repository import Gtk

        grid = Gtk.Grid()
        grid.set_border_width(12)

        label = guilabels.READ_PAGE_UPON_LOAD
        self.sayAllOnLoadCheckButton = \
            Gtk.CheckButton.new_with_mnemonic(label)
        self.sayAllOnLoadCheckButton.set_active(script_settings.sayAllOnLoad)
        grid.attach(self.sayAllOnLoadCheckButton, 0, 0, 1, 1)

        grid.show_all()

        return grid

    def setAppPreferences(self, prefs):
        """Write out the application specific preferences lines and set the
        new values.

        Arguments:
        - prefs: file handle for application preferences.
        """

        prefs.writelines("\n")
        prefix = "orca.scripts.toolkits.WebKitGtk.script_settings"
        prefs.writelines("import %s\n\n" % prefix)

        value = self.sayAllOnLoadCheckButton.get_active()
        prefs.writelines("%s.sayAllOnLoad = %s\n" % (prefix, value))
        script_settings.sayAllOnLoad = value

    def getBrailleGenerator(self):
        """Returns the braille generator for this script."""

        return BrailleGenerator(self)

    def getSpeechGenerator(self):
        """Returns the speech generator for this script."""

        return SpeechGenerator(self)

    def getStructuralNavigation(self):
        """Returns the 'structural navigation' class for this script."""

        types = self.getEnabledStructuralNavigationTypes()
        return StructuralNavigation(self, types, True)

    def getEnabledStructuralNavigationTypes(self):
        """Returns a list of the structural navigation object types
        enabled in this script."""

        enabledTypes = [StructuralNavigation.ANCHOR,
                        StructuralNavigation.BLOCKQUOTE,
                        StructuralNavigation.BUTTON,
                        StructuralNavigation.CHECK_BOX,
                        StructuralNavigation.CHUNK,
                        StructuralNavigation.COMBO_BOX,
                        StructuralNavigation.ENTRY,
                        StructuralNavigation.FORM_FIELD,
                        StructuralNavigation.HEADING,
                        StructuralNavigation.LANDMARK,
                        StructuralNavigation.LINK,
                        StructuralNavigation.LIST,
                        StructuralNavigation.LIST_ITEM,
                        StructuralNavigation.LIVE_REGION,
                        StructuralNavigation.PARAGRAPH,
                        StructuralNavigation.RADIO_BUTTON,
                        StructuralNavigation.SEPARATOR,
                        StructuralNavigation.TABLE,
                        StructuralNavigation.TABLE_CELL,
                        StructuralNavigation.UNVISITED_LINK,
                        StructuralNavigation.VISITED_LINK]

        return enabledTypes

    def getUtilities(self):
        """Returns the utilites for this script."""

        return Utilities(self)

    def onCaretMoved(self, event):
        """Called whenever the caret moves.

        Arguments:
        - event: the Event
        """

        self._lastCaretContext = event.source, event.detail1

        lastKey, mods = self.utilities.lastKeyAndModifiers()
        if lastKey in ['Tab', 'ISO_Left_Tab']:
            return

        if lastKey == 'Down' \
           and orca_state.locusOfFocus == event.source.parent \
           and event.source.getIndexInParent() == 0 \
           and orca_state.locusOfFocus.getRole() == pyatspi.ROLE_LINK:
            self.updateBraille(event.source)
            return

        orca.setLocusOfFocus(event, event.source, False)

        default.Script.onCaretMoved(self, event)

    def onDocumentReload(self, event):
        """Callback for document:reload accessibility events."""

        docRoles = [pyatspi.ROLE_DOCUMENT_FRAME, pyatspi.ROLE_DOCUMENT_WEB]
        if event.source.getRole() in docRoles:
            self._loadingDocumentContent = True

    def onDocumentLoadComplete(self, event):
        """Callback for document:load-complete accessibility events."""

        docRoles = [pyatspi.ROLE_DOCUMENT_FRAME, pyatspi.ROLE_DOCUMENT_WEB]
        if not event.source.getRole() in docRoles:
            return

        self._loadingDocumentContent = False
        if not self._isBrowser:
            return

        # TODO: We need to see what happens in Epiphany on pages where focus
        # is grabbed rather than set the caret at the start. But for simple
        # content in both Yelp and Epiphany this is alright for now.
        obj, offset = self.setCaretAtStart(event.source)
        orca.setLocusOfFocus(event, obj, False)

        self.updateBraille(obj)
        if script_settings.sayAllOnLoad \
           and _settingsManager.getSetting('enableSpeech'):
            self.sayAll(None)

    def onDocumentLoadStopped(self, event):
        """Callback for document:load-stopped accessibility events."""

        docRoles = [pyatspi.ROLE_DOCUMENT_FRAME, pyatspi.ROLE_DOCUMENT_WEB]
        if event.source.getRole() in docRoles:
            self._loadingDocumentContent = False

    def onFocusedChanged(self, event):
        """Callback for object:state-changed:focused accessibility events."""

        obj = event.source
        role = obj.getRole()
        self._lastCaretContext = obj, -1

        if role == pyatspi.ROLE_LIST_ITEM and obj.childCount:
            return

        widgetRoles = [pyatspi.ROLE_MENU,
                       pyatspi.ROLE_MENU_ITEM,
                       pyatspi.ROLE_LIST_ITEM,
                       pyatspi.ROLE_RADIO_BUTTON]
        if role in widgetRoles:
            default.Script.onFocusedChanged(self, event)
            return

        textRoles = [pyatspi.ROLE_HEADING,
                     pyatspi.ROLE_PANEL,
                     pyatspi.ROLE_PARAGRAPH,
                     pyatspi.ROLE_SECTION,
                     pyatspi.ROLE_TABLE_CELL]
        if role in textRoles:
            return

        if not (role == pyatspi.ROLE_LINK and obj.childCount):
            lastKey, mods = self.utilities.lastKeyAndModifiers()
            if lastKey in self.CARET_NAVIGATION_KEYS:
                return

        default.Script.onFocusedChanged(self, event)

    def onBusyChanged(self, event):
        """Callback for object:state-changed:busy accessibility events."""

        obj = event.source
        try:
            role = obj.getRole()
            name = obj.name
        except:
            return

        docRoles = [pyatspi.ROLE_DOCUMENT_FRAME, pyatspi.ROLE_DOCUMENT_WEB]
        if role not in docRoles or not self._isBrowser:
            return

        if event.detail1:
            self.presentMessage(messages.PAGE_LOADING_START)
        elif name:
            self.presentMessage(messages.PAGE_LOADING_END_NAMED % name)
        else:
            self.presentMessage(messages.PAGE_LOADING_END)

    def sayCharacter(self, obj):
        """Speak the character at the caret.

        Arguments:
        - obj: an Accessible object that implements the AccessibleText interface
        """

        if obj.getRole() == pyatspi.ROLE_ENTRY:
            default.Script.sayCharacter(self, obj)
            return

        boundary = pyatspi.TEXT_BOUNDARY_CHAR
        objects = self.utilities.getObjectsFromEOCs(obj, boundary=boundary)
        for (obj, start, end, string) in objects:
            if string:
                speech.speakCharacter(string)
            else:
                speech.speak(self.speechGenerator.generateSpeech(obj))

    def sayWord(self, obj):
        """Speaks the word at the caret.

        Arguments:
        - obj: an Accessible object that implements the AccessibleText interface
        """

        if obj.getRole() == pyatspi.ROLE_ENTRY:
            default.Script.sayWord(self, obj)
            return

        boundary = pyatspi.TEXT_BOUNDARY_WORD_START
        objects = self.utilities.getObjectsFromEOCs(obj, boundary=boundary)
        for (obj, start, end, string) in objects:
            self.sayPhrase(obj, start, end)

    def sayLine(self, obj):
        """Speaks the line at the caret.

        Arguments:
        - obj: an Accessible object that implements the AccessibleText interface
        """

        if obj.getRole() == pyatspi.ROLE_ENTRY:
            default.Script.sayLine(self, obj)
            return

        boundary = pyatspi.TEXT_BOUNDARY_LINE_START
        objects = self.utilities.getObjectsFromEOCs(obj, boundary=boundary)
        for (obj, start, end, string) in objects:
            self.sayPhrase(obj, start, end)

            # TODO: Move these next items into the speech generator.
            if obj.getRole() == pyatspi.ROLE_PANEL \
               and obj.getIndexInParent() == 0:
                obj = obj.parent

            rolesToSpeak = [pyatspi.ROLE_HEADING, pyatspi.ROLE_LINK]
            if obj.getRole() in rolesToSpeak:
                speech.speak(self.speechGenerator.getRoleName(obj))

    def sayPhrase(self, obj, startOffset, endOffset):
        """Speaks the text of an Accessible object between the given offsets.

        Arguments:
        - obj: an Accessible object that implements the AccessibleText interface
        - startOffset: the start text offset.
        - endOffset: the end text offset.
        """

        if obj.getRole() == pyatspi.ROLE_ENTRY:
            default.Script.sayPhrase(self, obj, startOffset, endOffset)
            return

        phrase = self.utilities.substring(obj, startOffset, endOffset)
        if len(phrase) and phrase != "\n":
            if phrase.isupper():
                voice = self.voices[settings.UPPERCASE_VOICE]
            else:
                voice = self.voices[settings.DEFAULT_VOICE]

            phrase = self.utilities.adjustForRepeats(phrase)
            links = [x for x in obj if x.getRole() == pyatspi.ROLE_LINK]
            if links:
                phrase = self.utilities.adjustForLinks(obj, phrase, startOffset)
            speech.speak(phrase, voice)
        else:
            # Speak blank line if appropriate.
            #
            self.sayCharacter(obj)

    def skipObjectEvent(self, event):
        """Gives us, and scripts, the ability to decide an event isn't
        worth taking the time to process under the current circumstances.

        Arguments:
        - event: the Event

        Returns True if we shouldn't bother processing this object event.
        """

        if event.type.startswith('object:state-changed:focused') \
           and event.detail1:
            if event.source.getRole() == pyatspi.ROLE_LINK:
                return False

        return default.Script.skipObjectEvent(self, event)

    def useStructuralNavigationModel(self):
        """Returns True if we should do our own structural navigation.
        This should return False if we're in a form field, or not in
        document content.
        """

        doNotHandleRoles = [pyatspi.ROLE_ENTRY,
                            pyatspi.ROLE_TEXT,
                            pyatspi.ROLE_PASSWORD_TEXT,
                            pyatspi.ROLE_LIST,
                            pyatspi.ROLE_LIST_ITEM,
                            pyatspi.ROLE_MENU_ITEM]

        if not self.structuralNavigation.enabled:
            return False

        if not self.utilities.isWebKitGtk(orca_state.locusOfFocus):
            return False

        states = orca_state.locusOfFocus.getState()
        if states.contains(pyatspi.STATE_EDITABLE):
            return False

        role = orca_state.locusOfFocus.getRole()
        if role in doNotHandleRoles:
            if role == pyatspi.ROLE_LIST_ITEM:
                return not states.contains(pyatspi.STATE_SELECTABLE)

            if states.contains(pyatspi.STATE_FOCUSED):
                return False

        return True

    def setCaretAtStart(self, obj):
        """Attempts to set the caret at the specified offset in obj. Because
        this is not always possible, this method will attempt to locate the
        first place inside of obj in which the caret can be positioned.

        Arguments:
        - obj: the accessible object in which the caret should be placed.

        Returns the object and offset in which we were able to set the caret.
        Otherwise, None if we could not find a text object, and -1 if we were
        not able to set the caret.
        """

        def implementsText(obj):
            if obj.getRole() == pyatspi.ROLE_LIST:
                return False
            return 'Text' in utils.listInterfaces(obj)

        child = obj
        if not implementsText(obj):
            child = utils.findDescendant(obj, implementsText)
            if not child:
                return None, -1

        index = -1
        text = child.queryText()
        for i in range(text.characterCount):
            if text.setCaretOffset(i):
                index = i
                break

        return child, index

    def panBrailleLeft(self, inputEvent=None, panAmount=0):
        """In document content, we want to use the panning keys to browse the
        entire document.
        """

        if self.flatReviewContext \
           or not self.isBrailleBeginningShowing() \
           or not self.utilities.isWebKitGtk(orca_state.locusOfFocus):
            return default.Script.panBrailleLeft(self, inputEvent, panAmount)

        obj = self.utilities.findPreviousObject(orca_state.locusOfFocus)
        orca.setLocusOfFocus(None, obj, notifyScript=False)
        self.updateBraille(obj)

        # Hack: When panning to the left in a document, we want to start at
        # the right/bottom of each new object. For now, we'll pan there.
        # When time permits, we'll give our braille code some smarts.
        while self.panBrailleInDirection(panToLeft=False):
            pass
        self.refreshBraille(False)

        return True

    def panBrailleRight(self, inputEvent=None, panAmount=0):
        """In document content, we want to use the panning keys to browse the
        entire document.
        """

        if self.flatReviewContext \
           or not self.isBrailleEndShowing() \
           or not self.utilities.isWebKitGtk(orca_state.locusOfFocus):
            return default.Script.panBrailleRight(self, inputEvent, panAmount)

        obj = self.utilities.findNextObject(orca_state.locusOfFocus)
        orca.setLocusOfFocus(None, obj, notifyScript=False)
        self.updateBraille(obj)

        # Hack: When panning to the right in a document, we want to start at
        # the left/top of each new object. For now, we'll pan there. When time
        # permits, we'll give our braille code some smarts.
        while self.panBrailleInDirection(panToLeft=True):
            pass
        self.refreshBraille(False)

        return True

    def sayAll(self, inputEvent):
        """Speaks the contents of the document beginning with the present
        location.  Overridden in this script because the sayAll could have
        been started on an object without text (such as an image).
        """

        if not self.utilities.isWebKitGtk(orca_state.locusOfFocus):
            return default.Script.sayAll(self, inputEvent)

        speech.sayAll(self.textLines(orca_state.locusOfFocus),
                      self.__sayAllProgressCallback)

        return True

    def getTextSegments(self, obj, boundary, offset=0):
        segments = []
        text = obj.queryText()
        length = text.characterCount
        string, start, end = text.getTextAtOffset(offset, boundary)
        while string and offset < length:
            string = self.utilities.adjustForRepeats(string)
            voice = self.speechGenerator.getVoiceForString(obj, string)
            string = self.utilities.adjustForLinks(obj, string, start)
            # Incrementing the offset should cause us to eventually reach
            # the end of the text as indicated by a 0-length string and
            # start and end offsets of 0. Sometimes WebKitGtk returns the
            # final text segment instead.
            if segments and [string, start, end, voice] == segments[-1]:
                break

            segments.append([string, start, end, voice])
            offset = end + 1
            string, start, end = text.getTextAtOffset(offset, boundary)
        return segments

    def textLines(self, obj):
        """Creates a generator that can be used to iterate over each line
        of a text object, starting at the caret offset.

        Arguments:
        - obj: an Accessible that has a text specialization

        Returns an iterator that produces elements of the form:
        [SayAllContext, acss], where SayAllContext has the text to be
        spoken and acss is an ACSS instance for speaking the text.
        """

        if not obj:
            return

        if obj.getRole() == pyatspi.ROLE_LINK:
            obj = obj.parent

        docRoles = [pyatspi.ROLE_DOCUMENT_FRAME, pyatspi.ROLE_DOCUMENT_WEB]
        document = utils.findAncestor(obj, lambda x: x.getRole() in docRoles)
        if not document or document.getState().contains(pyatspi.STATE_BUSY):
            return

        allTextObjs = utils.findAllDescendants(
            document, lambda x: x and 'Text' in utils.listInterfaces(x))
        allTextObjs = allTextObjs[allTextObjs.index(obj):len(allTextObjs)]
        textObjs = [x for x in allTextObjs if x.parent not in allTextObjs]
        if not textObjs:
            return

        boundary = pyatspi.TEXT_BOUNDARY_LINE_START
        sayAllStyle = _settingsManager.getSetting('sayAllStyle')
        if sayAllStyle == settings.SAYALL_STYLE_SENTENCE:
            boundary = pyatspi.TEXT_BOUNDARY_SENTENCE_START

        offset = textObjs[0].queryText().caretOffset
        for textObj in textObjs:
            textSegments = self.getTextSegments(textObj, boundary, offset)
            roleInfo = self.speechGenerator.getRoleName(textObj)
            if roleInfo:
                roleName, voice = roleInfo
                textSegments.append([roleName, 0, -1, voice])

            for (string, start, end, voice) in textSegments:
                yield [speechserver.SayAllContext(textObj, string, start, end),
                       voice]

            offset = 0

    def __sayAllProgressCallback(self, context, progressType):
        if progressType == speechserver.SayAllContext.PROGRESS:
            return

        obj = context.obj
        orca.setLocusOfFocus(None, obj, notifyScript=False)

        offset = context.currentOffset
        text = obj.queryText()

        if progressType == speechserver.SayAllContext.INTERRUPTED:
            text.setCaretOffset(offset)
            return

        # SayAllContext.COMPLETED doesn't necessarily mean done with SayAll;
        # just done with the current object. If we're still in SayAll, we do
        # not want to set the caret (and hence set focus) in a link we just
        # passed by.
        try:
            hypertext = obj.queryHypertext()
        except NotImplementedError:
            pass
        else:
            linkCount = hypertext.getNLinks()
            links = [hypertext.getLink(x) for x in range(linkCount)]
            if [l for l in links if l.startIndex <= offset <= l.endIndex]:
                return

        text.setCaretOffset(offset)

    def getTextLineAtCaret(self, obj, offset=None):
        """Gets the line of text where the caret is.

        Argument:
        - obj: an Accessible object that implements the AccessibleText
          interface
        - offset: an optional caret offset to use. (Not used here at the
          moment, but needed in the Gecko script)

        Returns the [string, caretOffset, startOffset] for the line of text
        where the caret is.
        """

        textLine = default.Script.getTextLineAtCaret(self, obj, offset)
        string = textLine[0]
        if string and string.find(self.EMBEDDED_OBJECT_CHARACTER) == -1 \
           and obj.getState().contains(pyatspi.STATE_FOCUSED):
            return textLine

        textLine[0] = self.utilities.displayedText(obj)
        try:
            text = obj.queryText()
        except:
            pass
        else:
            textLine[1] = min(textLine[1], text.characterCount)

        return textLine

    def updateBraille(self, obj, extraRegion=None):
        """Updates the braille display to show the given object.

        Arguments:
        - obj: the Accessible
        - extra: extra Region to add to the end
        """

        if not _settingsManager.getSetting('enableBraille') \
           and not _settingsManager.getSetting('enableBrailleMonitor'):
            debug.println(debug.LEVEL_INFO, "BRAILLE: update disabled")
            return

        if not obj:
            return

        if not self.utilities.isWebKitGtk(obj) \
           or (not self.utilities.isInlineContainer(obj) \
               and not self.utilities.isTextListItem(obj)):
            default.Script.updateBraille(self, obj, extraRegion)
            return

        brailleLine = self.getNewBrailleLine(clearBraille=True, addLine=True)
        for child in obj:
            if not self.utilities.onSameLine(child, obj[0]):
                break
            [regions, fRegion] = self.brailleGenerator.generateBraille(child)
            self.addBrailleRegionsToLine(regions, brailleLine)

        if not brailleLine.regions:
            [regions, fRegion] = self.brailleGenerator.generateBraille(
                obj, role=pyatspi.ROLE_PARAGRAPH)
            self.addBrailleRegionsToLine(regions, brailleLine)
            self.setBrailleFocus(fRegion)

        if extraRegion:
            self.addBrailleRegionToLine(extraRegion, brailleLine)

        self.refreshBraille()
