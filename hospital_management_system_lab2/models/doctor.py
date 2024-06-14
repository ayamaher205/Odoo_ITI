from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctors'
    _description = 'doctors'
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Image(string='Upload Image')
    departments_ids = fields.Many2many(comodel_name='hms.department', string='Departments')
    patient_ids = fields.Many2many("hms.patient", string="Patients")