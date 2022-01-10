# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime


class SetAttendees(models.TransientModel):
    """
    This model allow users to create attendees for a particular session, or for a list of sessions at once.
    Only partners not registered to selected sessions will be displayed
    """
    _name = 'wizard.openacademy.setattendees'        
    
    session_ids = fields.Many2many("session.session", string="Sessions")
    attendees_ids = fields.Many2many("res.partner", string="Attendees")
    
    def set_attendees(self):
        """
        Function triggered by the 'Set Attendees' button. 
        It allows to add extra attendees to the selected sessions
        """
        self.session_ids.attendees += self.attendees_ids
    
    @api.onchange('session_ids')
    def _onchange_session_attendees(self):
        """
        Allows to display 'attendees' not yet registered to the selected sessions
        """
        return {'domain':{'attendees_ids':[('id','not in',self.session_ids.attendees.ids)]}}