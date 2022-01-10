# -*- coding: utf-8 -*-
"""
EX Task: SC : Exercice 1 : partner fax
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime


class SaleOrderFax(models.Model):
    """
    This model gets the 'fax_number' from the 'res.partner' model 
    and display it into 'sale.order' form view
    """
    _inherit = 'sale.order'
    
    fax_number = fields.Char(related='partner_id.fax_number', string="Fax")
