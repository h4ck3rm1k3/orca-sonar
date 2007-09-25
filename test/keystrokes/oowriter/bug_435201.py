#!/usr/bin/python

"""Test to verify bug #435201 is still fixed.
   Orca is too chatty when navigating by paragraph in OOo Writer.
"""

from macaroon.playback import *

sequence = MacroSequence()

######################################################################
# 1. Start oowriter. There is a bug_435201.params file that will
# automatically load spanish.odt
#
sequence.append(WaitForWindowActivate("spanish - OpenOffice.org Writer",None))

######################################################################
# 2. Type Control-Home to position the text caret to the left of the
#    first character on the first line.
#
# BRAILLE LINE:  'soffice Application spanish - OpenOffice.org Writer Frame spanish - OpenOffice.org Writer RootPane ScrollPane Document view NOBODY expects the Spanish Inquisition! Our chief weapon is surprise. Surprise and  $l'
# VISIBLE:  'NOBODY expects the Spanish Inqui', cursor=1
# SPEECH OUTPUT: 'NOBODY expects the Spanish Inquisition! Our chief weapon is surprise. Surprise and '
#
sequence.append(KeyComboAction("<Control>Home"))
sequence.append(WaitForFocus("", acc_role=pyatspi.ROLE_PARAGRAPH))

######################################################################
# 3. Type Control-down to move to the next paragraph.
#
# BRAILLE LINE:  'soffice Application spanish - OpenOffice.org Writer Frame spanish - OpenOffice.org Writer RootPane ScrollPane Document view NOBODY expects the Spanish Inquisition! Amongst our weaponry are such diverse  $l'
# VISIBLE:  ' NOBODY expects the Spanish Inqui', cursor=1
# SPEECH OUTPUT: 'NOBODY expects the Spanish Inquisition! Amongst our weaponry are such diverse '
#
sequence.append(KeyComboAction("<Control>Down"))
sequence.append(WaitForFocus("", acc_role=pyatspi.ROLE_PARAGRAPH))

######################################################################
# 4. Type Control-down to move to the next paragraph.
#
# BRAILLE LINE:  'soffice Application spanish - OpenOffice.org Writer Frame spanish - OpenOffice.org Writer RootPane ScrollPane Document view NOBODY expects the Spanish Inquisition! Amongst our weaponry are such diverse  $l'
# VISIBLE:  ' NOBODY expects the Spanish Inqu', cursor=1
# SPEECH OUTPUT: 'blank'
#
sequence.append(KeyComboAction("<Control>Down"))
sequence.append(WaitForFocus("", acc_role=pyatspi.ROLE_PARAGRAPH))

######################################################################
# 5. Type Control-down to move to the next paragraph.
#
# BRAILLE LINE:  'soffice Application spanish - OpenOffice.org Writer Frame spanish - OpenOffice.org Writer RootPane ScrollPane Document view Now old lady, you have one last chance. Confess the heinous sin of heresy, reject  $l'
# VISIBLE:  'Now old lady, you have one last ', cursor=1
# SPEECH OUTPUT: 'Now old lady, you have one last chance. Confess the heinous sin of heresy, reject '
#
sequence.append(KeyComboAction("<Control>Down"))
sequence.append(WaitForFocus("", acc_role=pyatspi.ROLE_PARAGRAPH))

######################################################################
# 6. Type Control-down to move to the next paragraph.
#
# BRAILLE LINE:  'soffice Application spanish - OpenOffice.org Writer Frame spanish - OpenOffice.org Writer RootPane ScrollPane Document view Now old lady, you have one last chance. Confess the heinous sin of heresy, reject  $l'
# VISIBLE:  ' Now old lady, you have one last', cursor=1
# SPEECH OUTPUT: 'blank'
#
sequence.append(KeyComboAction("<Control>Down"))
sequence.append(WaitForFocus("", acc_role=pyatspi.ROLE_PARAGRAPH))

######################################################################
# 7. Type Control-down to move to the next paragraph.
#
# BRAILLE LINE:  'soffice Application spanish - OpenOffice.org Writer Frame spanish - OpenOffice.org Writer RootPane ScrollPane Document view Hm! She is made of harder stuff! Cardinal Fang! Fetch the COMFY CHAIR! $l'
# VISIBLE:  'Hm! She is made of harder stuff!', cursor=1
# SPEECH OUTPUT: 'Hm! She is made of harder stuff! Cardinal Fang! Fetch the COMFY CHAIR!'
#
sequence.append(KeyComboAction("<Control>Down"))
sequence.append(WaitForFocus("", acc_role=pyatspi.ROLE_PARAGRAPH))

######################################################################
# 8. Enter Alt-f, Alt-c to close the Writer application.
#
sequence.append(KeyComboAction("<Alt>f"))
sequence.append(WaitForFocus("New", acc_role=pyatspi.ROLE_MENU))

sequence.append(KeyComboAction("<Alt>c"))
sequence.append(WaitAction("object:property-change:accessible-name",
                           None,
                           None,
                           pyatspi.ROLE_ROOT_PANE,
                           30000))

######################################################################
# 9. Enter Alt-f, right arrow and Return, (File->New->Text Document),
#    to get the application back to the state it was in when the
#    test started.
#
sequence.append(KeyComboAction("<Alt>f"))
sequence.append(WaitForFocus("New", acc_role=pyatspi.ROLE_MENU))

sequence.append(KeyComboAction("Right"))
sequence.append(WaitForFocus("Text Document", acc_role=pyatspi.ROLE_MENU_ITEM))

sequence.append(KeyComboAction("Return"))
sequence.append(WaitAction("object:property-change:accessible-name",
                           None,
                           None,
                           pyatspi.ROLE_ROOT_PANE,
                           30000))
sequence.append(WaitForFocus("", acc_role=pyatspi.ROLE_PARAGRAPH))

######################################################################
# 10. Wait for things to get back to normal.
#
sequence.append(PauseAction(3000))

sequence.start()
