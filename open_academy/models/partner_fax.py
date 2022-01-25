# -*- coding: utf-8 -*-
"""
EX Task: SC : Exercice 1 : partner fax
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class PartnerFax(models.Model):
    """
    This model is used to add the field 'fax_number' into the partner form view
    """
    _inherit = 'res.partner'
    
    fax_number = fields.Char(string="Fax")
    