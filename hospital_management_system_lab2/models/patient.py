from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import ValidationError
import re
class Patient(models.Model):
    _name = 'patients_lab2'
    _description = 'Patient'
    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Email must be unique! and this email is already exists')
    ]

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=1)
    birth_date = fields.Date(string='Date Of Birth')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR', default=False)
    image = fields.Image(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age')
    state = fields.Selection([
        ('Undetermined', 'undetermined'),
        ('Good', 'good'),
        ('Fair', 'fair'),
        ('Serious', 'serious')
    ])
    department_id = fields.Many2one(comodel_name='hms.department', string='Department')
    department_capacity = fields.Integer(related='department_id.capacity', string='Department Capacity')
    doctor_ids = fields.Many2many("hms.doctors", string="Doctors")
    log_history_ids = fields.One2many("hms.patient.log.history", "patient_id", string="Log History")
    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                birth_date = record.birth_date
                if isinstance(birth_date, str):
                    birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
                elif not isinstance(birth_date, date):
                    birth_date = date.today()

                today = date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0

    @api.onchange('age')
    def age_change(self):
        for rec in self:
            if rec.age and rec.age < 30:
                rec.pcr = True
                return {
                    'warning': {
                        'title': "Age Change Warning",
                        'message': 'PCR has been checked.'
                    }
                }

    @api.constrains('email')
    def _check_email(self):
        email_pattern = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )
        for rec in self:
            if rec.email and not email_pattern.match(rec.email):
                raise ValidationError("The email is not valid.")
    @api.constrains("pcr", "cr_ratio")
    def _check_cr_mandatory(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError(
                    "CR Ratio is required if PCR Test is checked."
                )

    @api.model
    def create(self, vals):
        res = super(Patient, self).create(vals)
        if "state" in vals:
            self.env["hms.patient.log.history"].create(
                {
                    "patient_id": res.id,
                    "description": f"State changed to {vals['state']}",
                }
            )
        return res

    def write(self, vals):
        res = super(Patient, self).write(vals)
        if "state" in vals:
            for record in self:
                self.env["hms.patient.log.history"].create(
                    {
                        "patient_id": record.id,
                        "description": f"State changed to {vals['state']}",
                    }
                )
        return res

class PatientLogHistory(models.Model):
    _name = "hms.patient.log.history"
    _description = "Patient Log History"

    date = fields.Datetime(string="Date", default=fields.Datetime.now, required=True)
    description = fields.Text(string="Description", required=True)
    patient_id = fields.Many2one("patients_lab2", string="Patient", required=True)
