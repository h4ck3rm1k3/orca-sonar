#!/usr/bin/python

"""Test of icon output."""

from macaroon.playback import *
import utils

sequence = MacroSequence()

sequence.append(KeyComboAction("<Control>f"))
sequence.append(TypeAction("Images"))
sequence.append(KeyComboAction("Escape"))
sequence.append(KeyComboAction("Up"))
sequence.append(KeyComboAction("<Shift>Right"))
sequence.append(KeyComboAction("Down"))
sequence.append(KeyComboAction("Return"))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "bin icon",
    ["BRAILLE LINE:  'gtk-demo application GtkIconView demo frame bin icon'",
     "     VISIBLE:  'bin icon', cursor=1",
     "SPEECH OUTPUT: 'bin icon'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(utils.AssertPresentationAction(
    "bin icon Where Am I",
    ["BRAILLE LINE:  'gtk-demo application GtkIconView demo frame bin icon'",
     "     VISIBLE:  'bin icon', cursor=1",
     "SPEECH OUTPUT: 'Icon panel'",
     "SPEECH OUTPUT: 'bin'",
     "SPEECH OUTPUT: '1 of 20 items selected on 1 of 20'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Right"))
sequence.append(utils.AssertPresentationAction(
    "boot icon",
    ["BRAILLE LINE:  'gtk-demo application GtkIconView demo frame boot icon'",
     "     VISIBLE:  'boot icon', cursor=1",
     "SPEECH OUTPUT: 'boot icon'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("<Shift>Left"))
sequence.append(utils.AssertPresentationAction(
    "icon selection",
    ["BRAILLE LINE:  'gtk-demo application GtkIconView demo frame bin icon'",
     "     VISIBLE:  'bin icon', cursor=1",
     "SPEECH OUTPUT: 'bin icon'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(utils.AssertPresentationAction(
    "icon selection Where Am I",
    ["BRAILLE LINE:  'gtk-demo application GtkIconView demo frame bin icon'",
     "     VISIBLE:  'bin icon', cursor=1",
     "SPEECH OUTPUT: 'Icon panel'",
     "SPEECH OUTPUT: 'bin'",
     "SPEECH OUTPUT: '2 of 20 items selected on 1 of 20'"]))

sequence.append(KeyComboAction("<Alt>F4"))

sequence.append(utils.AssertionSummaryAction())
sequence.start()
