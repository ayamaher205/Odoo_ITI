from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'patient'

    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    birth_date = fields.Date(string='Date Of Birth')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection(
        [
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+', 'O+'),
            ('O-', 'O-')
        ], string='Blood Type'
    )
    pcr = fields.Boolean(string='PCR', default=False)
    image = fields.Image(string='Image')
    address = fields.Text(string='Address')
    age = fields.Char(string='Age', compute='_compute_age')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            birth_date = record.birth_date
            if isinstance(birth_date, str):
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            elif not isinstance(birth_date, date):
                # Handle cases where birth_date is neither str nor datetime.date
                birth_date = date.today()

            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            record.age = age