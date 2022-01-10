# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime


class Course(models.Model):
    """
    Course model
    """
    _name = 'course.course'
    _description = 'Course model'
    _rec_name = 'title'  # allows to display the 'title' field into other models 
                         # otherwise odoo takes automatically the field 'name' (not present in this model)

    title = fields.Char(required=True, string="Course title")
    description = fields.Text(string="Description")
    responsible = fields.Many2one("res.users", string="Responsible")
    sessions = fields.One2many("session.session", "course", string="Course")
    
    _sql_constraints = [
        ('course_uniqe', 'unique(title)', 
         'Course title must be unique'),
        ('course_desc_different', 'check(title != description)', 
         'Course description and course title must be different'),
    ]
    
    def copy(self, default = {}):
        """
        Re-implement copy() method + modify the object 'title'
        """
        default['title'] = "copy_of_" + self.title
        return super().copy(default=default)
