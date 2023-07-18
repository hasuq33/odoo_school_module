from odoo import fields,api,models

class MyProject(models.Model):
    _inherit = "res.users"

    is_signed_up = fields.Boolean('Signed Up',default=True)