from odoo import api,fields,models

class TestModelWizard(models.TransientModel):
    _name = 'test.model.wizard'
    _description = 'Test Model Wizard'

    teachar_name = fields.Char(string="Teachar Name")
    course_cat_ids = fields.Many2many(
    'crm.tag', "school_item_tag_wizard",string='Add Items')
    
    @api.model
    def create(self,vals):
        active_school_id = self.env.context.get('active_id')
        school = self.env['school.student'].browse(active_school_id)
        if 'teachar_name' in vals:
            school.teachar_name = vals['teachar_name']
        if 'course_cat_ids' in vals:
            school.course_cat_ids =vals['course_cat_ids']
        return super(TestModelWizard,self).create(vals)