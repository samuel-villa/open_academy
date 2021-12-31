# -*- coding: utf-8 -*-
"""
Open Academy exercise based on Odoo documentation:
https://www.odoo.com/documentation/15.0/developer/howtos/backend.html?highlight=context#
"""
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
        
    
class Session(models.Model):
    """
    Session model
    """
    _name = 'session.session'
    _description = 'Session model'

    name = fields.Char(required=True, string="Session name")
    start_date = fields.Date(required=True, default=fields.Date.context_today, string="Start date")
    duration = fields.Integer(string="Duration (days)")
    end_date = fields.Date(compute='_calculate_end_date', string="End date")
    number_of_seats = fields.Integer(string="Number of Seats")
    number_of_seats_pc = fields.Char(compute='_calculate_percentage', string="Number of Seats (%)")
    active = fields.Boolean(default=True, string="Active")  # reserved field
    instructor = fields.Many2one("res.partner", string="Instructor")
    course = fields.Many2one("course.course", required=True, string="Course")
    attendees = fields.Many2many("res.partner", string="Attendees")
                
    @api.depends('start_date', 'duration')
    def _calculate_end_date(self):
        """
        calculate the end date by adding 'duration' (days) to the start date
        """
        for record in self:
            record.end_date = record.start_date + datetime.timedelta(days=record.duration)
                
    @api.depends('number_of_seats', 'attendees')
    def _calculate_percentage(self):
        """
        calculate percentage of taken seats by the attendees of a session
        """
        for record in self:
            total_attendees = len(record.attendees)
            if total_attendees == 0:
                record.number_of_seats_pc = 0
            else:
                # if using progressbar in the view, the function should return an Int (not a string)
                record.number_of_seats_pc = int(total_attendees / record.number_of_seats * 100)
                
    @api.onchange('number_of_seats', 'attendees')
    def _onchange_warning(self):
        """
        return a warning message whether the fields mentioned in the 'onchange' decorator are modified
        """
        if self.number_of_seats < 0 or self.number_of_seats < len(self.attendees): 
            return {
                'warning': {
                    'title': "Error",
                    'message': "'Number Of Seats' must be a positive number and \
                     the number of 'Attendees' must be less or equal to 'Number Of Seats'.",
                }
            }
    
    @api.constrains('instructor', 'attendees')
    def _check_instructor_attendees(self):
        """
        constraint that prevent adding an instructor as an attendee of his/her own session
        """
        for record in self:
            if record.instructor in record.attendees:
                raise ValidationError("The instructor cannot attend his/her own session.")
                
    def manage_attendees(self):
        """
        window action based on the 'SetAttendees' class that allow to launch a wizard form 
        within the Session model
        """
        return self.env['ir.actions.act_window']._for_xml_id('open_academy.set_attendees_wizard')


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
    
    
class SetAttendees(models.TransientModel):
    """
    This model allow users to create attendees for a particular session, or for a list of sessions at once.
    """
    _name = 'wizard.openacademy.setattendees'        
    
    session_id = fields.Many2one("session.session", string="Session")
    attendees_ids = fields.Many2many("res.partner", string="Attendees")
    
    def set_attendees(self):
        """
        this function MUST be present because it's used to trigger the button function in the view
        """
        return True
    
    @api.onchange('session_id')
    def _onchange_session_attendees(self):
        """
        allows to add 'attendees' to the selected 'session' based on attendees already present
        """
        return {'domain':{'attendees_ids':[('id','not in',self.session_id.attendees.ids)]}}
    
    
# ===============================================================================================
#         EX Task: SC : Exercice 1 : partner fax
# ===============================================================================================
class PartnerFax(models.Model):
    """
    This model is used to add the field 'fax_number' into the partner form view
    """
    _inherit = 'res.partner'
    
    fax_number = fields.Char(string="Fax")


class SaleOrderFax(models.Model):
    """
    This model gets the 'fax_number' from the 'res.partner' model 
    and display it into 'sale.order' form view
    """
    _inherit = 'sale.order'
    
    fax_number = fields.Char(related='partner_id.fax_number', string="Fax")
