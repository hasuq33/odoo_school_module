from odoo import fields,api,models

class AdmissionRegister(models.Model):
    _name = "admission.student"

    name = fields.Char(string="First Name")
    lname = fields.Char(string="Last Name")
    address = fields.Text(string="Address")
    phone = fields.Char(string="Phone No.")
    email = fields.Char(string="Email")  
    user_image = fields.Binary("User's Image")
    subject_ids = fields.One2many('admission.student.line','admission_id',string="Subject Line")


class AdmissionSubject(models.Model):
    _name = "admission.student.line"

    admission_id = fields.Many2one('admission.student',string="Applicant Name")    
    subject = fields.Char(string="Subject")
    sub_priority = fields.Selection([('Optional', 'Optional'), ('Mandatory', 'Mandatory')],string='Select Priority')