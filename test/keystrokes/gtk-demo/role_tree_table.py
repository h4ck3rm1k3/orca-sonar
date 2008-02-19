#!/usr/bin/python

"""Test of tree table output using the gtk-demo Tree Store demo
   under the Tree View area.
"""

from macaroon.playback import *
import utils

sequence = MacroSequence()

########################################################################
# We wait for the demo to come up and for focus to be on the tree table
#
sequence.append(WaitForWindowActivate("GTK+ Code Demos"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TREE_TABLE))

########################################################################
# Once gtk-demo is running, invoke the Tree Store demo
#
sequence.append(KeyComboAction("<Control>f"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TEXT))
sequence.append(TypeAction("Tree View", 1000))
sequence.append(KeyComboAction("Return", 500))
sequence.append(KeyComboAction("<Shift>Right"))
sequence.append(WaitAction("object:state-changed:expanded",
                           None,
                           None,
                           pyatspi.ROLE_TABLE_CELL,
                           5000))

sequence.append(KeyComboAction("<Control>f"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TEXT))
sequence.append(TypeAction("Tree Store", 1000))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Return", 500))
#sequence.append(WaitForWindowActivate("Card planning sheet",None))
sequence.append(WaitForFocus("Holiday",
                             acc_role=pyatspi.ROLE_TABLE_COLUMN_HEADER))
sequence.append(utils.AssertPresentationAction(
    "Tree table initial focus",
    ["BRAILLE LINE:  'gtk-demo Application Window Tree Store $l'",
     "     VISIBLE:  'Tree Store $l', cursor=11",
     "BRAILLE LINE:  'gtk-demo Application Window  $l'",
     "     VISIBLE:  'gtk-demo Application Window  $l', cursor=29",
     "BRAILLE LINE:  'gtk-demo Application Window  $l'",
     "     VISIBLE:  'gtk-demo Application Window  $l', cursor=29",
     "BRAILLE LINE:  'gtk-demo Application GTK+ Code Demos Frame TabList Widget (double click for demo) Page ScrollPane TreeTable Widget (double click for demo) ColumnHeader Tree Store TREE LEVEL 2'",
     "     VISIBLE:  'Tree Store TREE LEVEL 2', cursor=1",
     "BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame'",
     "     VISIBLE:  'Card planning sheet Frame', cursor=1",
     "BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader'",
     "     VISIBLE:  'Holiday ColumnHeader', cursor=1",
     "SPEECH OUTPUT: 'Widget (double click for demo) page'",
     "SPEECH OUTPUT: 'Widget (double click for demo) column header'",
     "SPEECH OUTPUT: 'Tree Store'",
     "SPEECH OUTPUT: 'tree level 2'",
     "SPEECH OUTPUT: ''",
     "SPEECH OUTPUT: 'Card planning sheet frame'",
     "SPEECH OUTPUT: ''",
     "SPEECH OUTPUT: 'Holiday column header'"]))

########################################################################
# Down arrow twice to select the "January" cell.
#
sequence.append(KeyComboAction("Down", 500))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TREE_TABLE))
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down", 500))
sequence.append(WaitAction("object:state-changed:selected",
                           None,
                           None,
                           pyatspi.ROLE_TABLE_CELL,
                           5000))
sequence.append(utils.AssertPresentationAction(
    "January cell focus",
    ["BUG? - nothing spoken and line not brailled"]))

########################################################################
# Do a basic "Where Am I" via KP_Enter.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(PauseAction(3000))
sequence.append(utils.AssertPresentationAction(
    "January cell basic Where Am I",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader January expanded < > Alex < > Havoc < > Tim < > Owen < > Dave TREE LEVEL 1'",
     "     VISIBLE:  'January expanded < > Alex < > Ha', cursor=1",
     "SPEECH OUTPUT: 'tree table'",
     "SPEECH OUTPUT: 'Holiday'",
     "SPEECH OUTPUT: 'cell'",
     "SPEECH OUTPUT: 'January'",
     "SPEECH OUTPUT: 'row 1 of 53'",
     "SPEECH OUTPUT: 'expanded'",
     "SPEECH OUTPUT: 'tree level 1'"]))

########################################################################
# Do a detailed "Where Am I" via KP_Enter.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(PauseAction(3000))
sequence.append(utils.AssertPresentationAction(
    "January cell detailed Where Am I",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader January expanded < > Alex < > Havoc < > Tim < > Owen < > Dave TREE LEVEL 1'",
     "     VISIBLE:  'January expanded < > Alex < > Ha', cursor=1",
     "BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader January expanded < > Alex < > Havoc < > Tim < > Owen < > Dave TREE LEVEL 1'",
     "     VISIBLE:  'January expanded < > Alex < > Ha', cursor=1",
     "SPEECH OUTPUT: 'tree table'",
     "SPEECH OUTPUT: 'Holiday'",
     "SPEECH OUTPUT: 'cell'",
     "SPEECH OUTPUT: 'January'",
     "SPEECH OUTPUT: 'row 1 of 53'",
     "SPEECH OUTPUT: 'expanded'",
     "SPEECH OUTPUT: 'tree level 1'",
     "SPEECH OUTPUT: 'tree table'",
     "SPEECH OUTPUT: 'Holiday'",
     "SPEECH OUTPUT: 'cell'",
     "SPEECH OUTPUT: 'January'",
     "SPEECH OUTPUT: 'row 1 of 53'",
     "SPEECH OUTPUT: 'January'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'expanded'",
     "SPEECH OUTPUT: 'tree level 1'"]))

########################################################################
# Collapse the cell.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("<Shift>Left", 500))
sequence.append(WaitAction("object:state-changed:expanded",
                           None,
                           None,
                           pyatspi.ROLE_TABLE_CELL,
                           5000))
sequence.append(utils.AssertPresentationAction(
    "January cell collapsed",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader January collapsed < > Alex < > Havoc < > Tim < > Owen < > Dave TREE LEVEL 1'",
     "     VISIBLE:  'January collapsed < > Alex < > H', cursor=1",
     "SPEECH OUTPUT: 'collapsed'"]))

########################################################################
# Do a basic "Where Am I" via KP_Enter.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(PauseAction(3000))
sequence.append(utils.AssertPresentationAction(
    "January cell collapsed basic Where Am I",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader January collapsed < > Alex < > Havoc < > Tim < > Owen < > Dave TREE LEVEL 1'",
     "     VISIBLE:  'January collapsed < > Alex < > H', cursor=1",
     "SPEECH OUTPUT: 'tree table'",
     "SPEECH OUTPUT: 'Holiday'",
     "SPEECH OUTPUT: 'cell'",
     "SPEECH OUTPUT: 'January'",
     "SPEECH OUTPUT: 'row 1 of 50'",
     "SPEECH OUTPUT: 'collapsed'",
     "SPEECH OUTPUT: 'tree level 1'"]))

########################################################################
# Do a detailed "Where Am I" via KP_Enter.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(PauseAction(3000))
sequence.append(utils.AssertPresentationAction(
    "January cell collapsed detailed Where Am I",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader January collapsed < > Alex < > Havoc < > Tim < > Owen < > Dave TREE LEVEL 1'",
     "     VISIBLE:  'January collapsed < > Alex < > H', cursor=1",
     "BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader January collapsed < > Alex < > Havoc < > Tim < > Owen < > Dave TREE LEVEL 1'",
     "     VISIBLE:  'January collapsed < > Alex < > H', cursor=1",
     "SPEECH OUTPUT: 'tree table'",
     "SPEECH OUTPUT: 'Holiday'",
     "SPEECH OUTPUT: 'cell'",
     "SPEECH OUTPUT: 'January'",
     "SPEECH OUTPUT: 'row 1 of 50'",
     "SPEECH OUTPUT: 'collapsed'",
     "SPEECH OUTPUT: 'tree level 1'",
     "SPEECH OUTPUT: 'tree table'",
     "SPEECH OUTPUT: 'Holiday'",
     "SPEECH OUTPUT: 'cell'",
     "SPEECH OUTPUT: 'January'",
     "SPEECH OUTPUT: 'row 1 of 50'",
     "SPEECH OUTPUT: 'January'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'check box not checked'",
     "SPEECH OUTPUT: 'collapsed'",
     "SPEECH OUTPUT: 'tree level 1'"]))

########################################################################
# Expand the cell again.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("<Shift>Right"))
sequence.append(WaitAction("object:state-changed:expanded",
                           None,
                           None,
                           pyatspi.ROLE_TABLE_CELL,
                           5000))
sequence.append(utils.AssertPresentationAction(
    "January cell expanded",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader January expanded < > Alex < > Havoc < > Tim < > Owen < > Dave TREE LEVEL 1'",
     "     VISIBLE:  'January expanded < > Alex < > Ha', cursor=1",
     "SPEECH OUTPUT: 'expanded 3 items'"]))

########################################################################
# Arrow down a row.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down", 500))
sequence.append(WaitAction("object:state-changed:selected",
                           None,
                           None,
                           pyatspi.ROLE_TABLE_CELL,
                           5000))
sequence.append(utils.AssertPresentationAction(
    "New Year's Day cell",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Holiday ColumnHeader New Years Day <x> Alex <x> Havoc <x> Tim <x> Owen < > Dave TREE LEVEL 2'",
     "     VISIBLE:  'New Years Day <x> Alex <x> Havoc', cursor=1",
     "SPEECH OUTPUT: ''",
     "SPEECH OUTPUT: 'New Years Day Alex check box checked  Havoc check box checked  Tim check box checked  Owen check box checked  Dave check box not checked '",
     "SPEECH OUTPUT: 'tree level 2'"]))

########################################################################
# Arrow right to a column.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("<Control>Right", 500))
sequence.append(WaitAction("object:active-descendant-changed",
                           None,
                           None,
                           pyatspi.ROLE_TABLE,
                           5000))
sequence.append(utils.AssertPresentationAction(
    "Alex checkbox cell",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Alex ColumnHeader New Years Day <x> Alex <x> Havoc <x> Tim <x> Owen < > Dave'",
     "     VISIBLE:  '<x> Alex <x> Havoc <x> Tim <x> O', cursor=1",
     "SPEECH OUTPUT: ''",
     "SPEECH OUTPUT: 'Alex column header'",
     "SPEECH OUTPUT: 'New Years Day Alex check box checked  Havoc check box checked  Tim check box checked  Owen check box checked  Dave check box not checked '"]))

#
# [[[BUG?: Somewhere around here, the demo flakes out.]]]
#

########################################################################
# Do a basic "Where Am I" via KP_Enter.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(PauseAction(3000))
sequence.append(utils.AssertPresentationAction(
    "Alex checkbox cell basic Where Am I",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Alex ColumnHeader <x> Alex'",
     "     VISIBLE:  '<x> Alex', cursor=1",
     "SPEECH OUTPUT: 'tree table'",
     "SPEECH OUTPUT: 'Alex'",
     "SPEECH OUTPUT: 'cell'",
     "SPEECH OUTPUT: 'check box checked'",
     "SPEECH OUTPUT: 'row 2 of 53'"]))

########################################################################
# Do a detailed "Where Am I" via KP_Enter.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(PauseAction(3000))
sequence.append(utils.AssertPresentationAction(
    "Alex checkbox cell detailed Where Am I",
    ["BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Alex ColumnHeader <x> Alex'",
     "     VISIBLE:  '<x> Alex', cursor=1",
     "BRAILLE LINE:  'gtk-demo Application Card planning sheet Frame ScrollPane TreeTable Alex ColumnHeader <x> Alex'",
     "     VISIBLE:  '<x> Alex', cursor=1",
     "SPEECH OUTPUT: 'tree table'",
     "SPEECH OUTPUT: 'Alex'",
     "SPEECH OUTPUT: 'cell'",
     "SPEECH OUTPUT: 'check box checked'",
     "SPEECH OUTPUT: 'row 2 of 53'",
     "SPEECH OUTPUT: 'tree table'",
     "SPEECH OUTPUT: 'Alex'",
     "SPEECH OUTPUT: 'cell'",
     "SPEECH OUTPUT: 'check box checked'",
     "SPEECH OUTPUT: 'row 2 of 53'",
     "SPEECH OUTPUT: 'New Years Day'",
     "SPEECH OUTPUT: 'check box checked'",
     "SPEECH OUTPUT: 'check box checked'",
     "SPEECH OUTPUT: 'check box checked'",
     "SPEECH OUTPUT: 'check box checked'",
     "SPEECH OUTPUT: 'check box not checked'"]))

########################################################################
# Change the state of the checkbox.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction(" "))
sequence.append(WaitAction("object:state-changed:checked",
                           None,
                           None,
                           pyatspi.ROLE_TABLE_CELL,
                           5000))
sequence.append(utils.AssertPresentationAction(
    "Alex checkbox cell unchecked",
    ["BUG? - nothing presented"]))

########################################################################
# Change the state of the checkbox.
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction(" "))
sequence.append(WaitAction("object:state-changed:checked",
                           None,
                           None,
                           pyatspi.ROLE_TABLE_CELL,
                           5000))
sequence.append(utils.AssertPresentationAction(
    "Alex checkbox cell checked",
    ["BUG? - nothing presented"]))

########################################################################
# Close the Card planning sheet demo
#
sequence.append(KeyComboAction("<Alt>F4", 1000))

########################################################################
# Go back to the main gtk-demo window and reselect the
# "Application main window" menu.  Let the harness kill the app.
#
#sequence.append(WaitForWindowActivate("GTK+ Code Demos",None))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TREE_TABLE))
sequence.append(KeyComboAction("<Control>f"))

sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TEXT))
sequence.append(TypeAction("Tree View", 1000))
sequence.append(KeyComboAction("Return", 500))
sequence.append(KeyComboAction("<Shift>Left"))
sequence.append(WaitAction("object:state-changed:expanded",
                           None,
                           None,
                           pyatspi.ROLE_TABLE_CELL,
                           5000))

sequence.append(KeyComboAction("Home"))

sequence.append(WaitAction("object:active-descendant-changed",
                           None,
                           None,
                           pyatspi.ROLE_TREE_TABLE,
                           5000))

# Just a little extra wait to let some events get through.
#
sequence.append(PauseAction(3000))

sequence.append(utils.AssertionSummaryAction())

sequence.start()
