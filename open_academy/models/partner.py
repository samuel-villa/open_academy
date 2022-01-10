# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime


class Partner(models.Model):
    """
    This model is used to add the fields 'instructor' and 'teacher' into the partner
    and create a relation between 'session' and 'partner'
    """
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string="Instructor")
    teacher = fields.Selection([
        ('t1', 'Teacher / Level 1'), 
        ('t2', 'Teacher / Level 2')
    ], string="Teacher")
    session_partner = fields.Many2many("session.session", string="Relation between Session and Partner")
