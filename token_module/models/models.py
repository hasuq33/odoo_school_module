from odoo import fields,api,models

class MyModel(models.Model):
    _inherit = "account.move"

    def action_generate_invoice_pdf(self):  
        return {
            'type': 'ir.actions.act_url',
            'target':'self',
            'url': self.get_portal_url() + '&report_type=pdf&download=true',
        }
    