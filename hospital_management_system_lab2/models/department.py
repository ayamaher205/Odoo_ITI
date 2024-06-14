from odoo import models, fields

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Departments'

    name = fields.Char(string='Name')
    capacity = fields.Integer(string='Capacity')
    is_open = fields.Boolean(string='Is Open')
    patient_ids = fields.One2many(comodel_name='patients_lab2', inverse_name='department_id', string='Patients')
