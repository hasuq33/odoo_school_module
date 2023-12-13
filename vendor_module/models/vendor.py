from odoo import api,fields,models

class Contact(models.Model):
    _inherit = 'res.partner'

    is_vendor = fields.Boolean(string='Is_Vendor')
