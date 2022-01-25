# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime


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
    attendees_count = fields.Integer(string="Attendees count", compute="_get_attendees_count", store=True)
    
    @api.depends('attendees')
    def _get_attendees_count(self):
        """
        needed to create an Integer field ('attendees_count') that will be used 
        as the 'measure' for the graph bars. Without this method (and without the 'attendees_count' field) 
        only the other Integer fields would be available in the 'measure' tab/button in the graph view
        """
        for record in self:
            record.attendees_count = len(record.attendees)
                
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
