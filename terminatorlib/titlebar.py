#!/usr/bin/python
# Terminator by Chris Jones <cmsj@tenshu.net>
# GPL v2 only
"""titlebar.py - classes necessary to provide a terminal title bar"""

import gtk
import gobject

from version import APP_NAME
from newterminator import Terminator
from editablelabel import EditableLabel

# pylint: disable-msg=R0904
# pylint: disable-msg=W0613
class Titlebar(gtk.EventBox):
    """Class implementing the Titlebar widget"""

    terminator = None
    oldtitle = None
    termtext = None
    sizetext = None
    label = None
    hbox = None
    ebox = None
    grouphbox = None
    groupicon = None
    grouplabel = None

    __gsignals__ = {
            'clicked': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
            'edit-done': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
    }

    def __init__(self):
        """Class initialiser"""
        gtk.EventBox.__init__(self)
        self.__gobject_init__()

        self.terminator = Terminator()

        self.label = EditableLabel()
        self.label.connect('edit-done', self.on_edit_done)
        self.ebox = gtk.EventBox()
        self.grouphbox = gtk.HBox()
        self.grouplabel = gtk.Label()
        self.groupicon = gtk.Image()

        groupsend_type = self.terminator.groupsend_type
        if self.terminator.groupsend == groupsend_type['all']:
            icon_name = 'all'
        elif self.terminator.groupsend == groupsend_type['group']:
            icon_name = 'group'
        elif self.terminator.groupsend == groupsend_type['off']:
            icon_name = 'off'
        self.set_from_icon_name('_active_broadcast_%s' % icon_name, 
                gtk.ICON_SIZE_MENU)

        self.grouphbox.pack_start(self.groupicon, False, True, 2)
        self.grouphbox.pack_start(self.grouplabel, False, True, 2)
        self.ebox.add(self.grouphbox)
        self.ebox.show_all()

        self.hbox = gtk.HBox()
        self.hbox.pack_start(self.ebox, False, True, 0)
        self.hbox.pack_start(gtk.VSeparator(), False, True, 0)
        self.hbox.pack_start(self.label, True, True)

        self.add(self.hbox)
        self.show_all()

        self.connect('button-press-event', self.on_clicked)

    def connect_icon(self, func):
        """Connect the supplied function to clicking on the group icon"""
        self.ebox.connect('button-release-event', func)

    def update(self):
        """Update our contents"""
        self.label.set_text("%s %s" % (self.termtext, self.sizetext))

    def set_from_icon_name(self, name, size = gtk.ICON_SIZE_MENU):
        """Set an icon for the group label"""
        if not name:
            self.groupicon.hide()
            return
        
        self.groupicon.set_from_icon_name(APP_NAME + name, size)
        self.groupicon.show()

    def update_terminal_size(self, width, height):
        """Update the displayed terminal size"""
        self.sizetext = "%sx%s" % (width, height)
        self.update()

    def set_terminal_title(self, widget, title):
        """Update the terminal title"""
        self.termtext = title
        self.update()

    def set_group_label(self, name):
        """Set the name of the group"""
        if name:
            self.grouplabel.set_text(name)
            self.grouplabel.show()
        else:
            self.grouplabel.hide()

    def on_clicked(self, widget, event):
        """Handle a click on the label"""
        self.emit('clicked')

    def on_edit_done(self, widget):
        """Re-emit an edit-done signal from an EditableLabel"""
        self.emit('edit-done')

gobject.type_register(Titlebar)
