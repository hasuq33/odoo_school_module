from odoo import api, fields, models
import datetime


class SpecialAbstarctReport(models.AbstractModel):
    _name = "report.school_module.fv_special_report"

    @api.model
    def _get_report_values(self,docids,data=None):
        records = self.env['school.student'].search([])
        return {
            'doc_ids': docids,
            'doc_model': 'school.student',
            'docs': records,
        }

# This Model Is about Student's Details
class SchoolModel(models.Model):
    _name = "school.student"
    _description = "School Student"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Student Name",tracking=True)
    #Add Customer in my form view
    company_id = fields.Many2one('res.company', store=True, copy=False,default=lambda self: self.env.company)
    rel_partner_id = fields.Many2one('res.partner', string="Customer",store=True) 
    # Add User in my form view
    rel_user_id = fields.Many2one('res.users', string="User Name",default=lambda self: self.env.user.id,readonly=True,store=True)
    rollno = fields.Integer(string="Roll No.")
    gender = fields.Selection([("Male", "Male"), ("Female", "Female")], string="Gender")
    date_of_birth = fields.Date(string="Date of Birth",tracking=True)
    progress_report = fields.Text(string="Progress Report", help="Write Student Progress in School")
    age = fields.Integer(string="Age", null=True)
    marksheet = fields.Binary()
    course_cat_ids = fields.Many2many("crm.tag", "school_item_tag", string="Add Items")
    phone = fields.Char(string="Phone",tracking=True)
    email = fields.Char(string="Email",tracking=True)
    state = fields.Selection(selection=[('draft','Draft'),
                                        ('done','Done'),
                                        ('cancel','Cancel')],
                                        string="Status",required=True,readonly=True,copy=False,tracking=True,default='draft')
    teachar_name = fields.Char(string="Teachar Name",tracking=True)
    sales_school_ids = fields.Many2many('sale.order', 'school_sale_tag',string='Sales Order')
    sales_orders_count = fields.Integer(compute='compute_count', string="Sale Orders", store=True)
    #sales_order_ids field will show only Confirm sale order for selection 
    # sale_order_school_ids = fields.Many2many('sale.order', 'sale_order_tag',string='Confirm Order')
    confirm_sales_order_count = fields.Integer(compute='sale_order_count', string='Confirm Sale Order',store=True)
    # company_id = fields.Many2one('res.company',string="Company")
    product_ids = fields.One2many('school.product','student_school_id',string="Add Products",tracking=True)
    product_total_amount = fields.Float(compute="compute_final_total",string="Final Amount")
    product_non_tax_amount = fields.Float(compute="compute_non_tax_amount", string="Non Taxable Amount")
    # product_applied_tax = fields.Float(compute="compute_taxable_amount", string="Applied Tax Amount")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    sale_order_store_id = fields.One2many('sale.order','sale_school_student_order_ids',string="Sale Order Stored Id")

    
    @api.depends('product_ids.product_price','product_ids.product_quantity','product_ids.product_tax_ids.amount')
    def compute_taxable_amount(self):
        for rec in self:
            total_amount = 0.0
            for i in rec.product_ids:
                total_amount += ((i.product_price*i.product_quantity)*(i.product_tax_ids.amount)/100)
            rec.product_applied_tax = total_amount    

    @api.depends('product_ids.product_price','product_ids.product_quantity')
    def compute_non_tax_amount(self):
        for rec in self:
            total_amount = 0.0
            for i in rec.product_ids:
                total_amount += (i.product_price*i.product_quantity)
            rec.product_non_tax_amount = total_amount    

    @api.depends('product_ids.product_subtotal')
    def compute_final_total(self):
        for rec in self:
            total_amount = 0.0
            for i in rec.product_ids:
                total_amount += i.product_subtotal
            rec.product_total_amount = total_amount


    # Creating method for sale order
    def create_sale_order(self):
       
        if self.sale_order_store_id:
            sale_order = self.sale_order_store_id[0]
            sale_order.partner_id = self.rel_partner_id.id 

            for product in self.product_ids:
                # If Id not found it will create a line
                if not product.id in sale_order.order_line.mapped('school_product_id').ids:
                     sale_order_line = self.env['sale.order.line'].create({
                        'order_id': sale_order.id,
                        'product_id': product.product_id.id,
                        'product_uom_qty': product.product_quantity,
                        'name': product.product_label,
                        'tax_id':product.product_tax_ids,
                        'price_unit': product.product_price,
                        'school_product_id': product.id, 
                    }) 
                else:
                    # Otherwise it will update line on existing line
                    sale_order_line = sale_order.order_line.filtered(lambda line: line.school_product_id.id == product.id)
                    sale_order_line.write({
                        'order_id': sale_order.id,
                        'product_id': product.product_id.id,
                        'product_uom_qty': product.product_quantity,
                        'name': product.product_label,
                        'tax_id': product.product_tax_ids,
                        'price_unit': product.product_price,
                        'school_product_id': product.id, 
                    })
            # It will unlink those ids not found in product_ids 
            unlink_lines = sale_order.order_line.filtered(lambda line: line.school_product_id.id not in self.product_ids.ids)
            unlink_lines.unlink()

            params = {
                'name': 'Sale Order',
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': self.sale_order_store_id[0].id,  
                'view_mode': 'form'
                }
            return params

        else:
            sale_order = self.env['sale.order'].create({
            'partner_id': self.rel_partner_id.id,
             })
            for product in self.product_ids:
                sale_order_line = self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': product.product_id.id,
                    'product_uom_qty': product.product_quantity,
                    'name': product.product_label,
                    'tax_id': product.product_tax_ids,
                    'price_unit': product.product_price,
                    'school_product_id': product.id,
                })
            self.sale_order_store_id  = [(4, sale_order.id)]   
            params = {
                'name':'Sale Order',
                'type':'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': sale_order.id,
                'view_mode':'form'
            }
            return params

    # Sending Email Method
    def send_email_method(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data._xmlid_lookup('school_module.name_of_email_template')[2]
        except ValueError:
            template_id = False
        ctx={
              'default_template_id': template_id,
              'mark_so_as_sent': True,
              'force_email': True
        }
        params = {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'mail.compose.message',
            'target':'new',
            'context':ctx,
        }
        return params            
   

# This Method I used for showing related partner and it's child
    @api.onchange('rel_user_id')
    def onchange_rel_user_id(self):
        if self.rel_user_id:
            recommended_partner = self.rel_user_id.partner_id.commercial_partner_id
            child_partners = self.env['res.partner'].search([('id', 'child_of', recommended_partner.id)])
            partner_ids = [recommended_partner.id] + child_partners.ids
            params = {
                'domain':{
                    'rel_partner_id': [('id','in',partner_ids)]
                }
            } 
        return params
    # We use search() method to filter the record in list view that customer are not partner 
    # @api.model  
    # def search(self,args,offset=0,limit=None,order=None):
    #     if self.env.user.partner_id:
    #         args+=[('rel_partner_id','=',self.env.user.partner_id.id)]
    #     return super(SchoolModel,self).search(args,offset,limit,order)    

   # For sale_order_school_ids
    def sale_order_school(self):
            if len(self.rel_partner_id.sale_order_ids) == 1:
                params={
                'name':"Quotations",
                'type':'ir.actions.act_window',
                'res_model':'sale.order',
                'res_id':self.rel_partner_id.sale_order_ids.id,
                'view_mode':'form',
                'context':{'create':True,'default_partner_id':self.rel_partner_id.id}
                }
            else:    
                params = {
                    'name':"Quotations",
                    'type':'ir.actions.act_window',
                    'res_model':'sale.order',
                    'view_mode':'tree,form',
                    'domain':[('partner_id','=',self.rel_partner_id.id)],
                    'context':{'create':True,'default_partner_id':self.rel_partner_id.id}
                }
            return params

    @api.depends('rel_partner_id')
    def sale_order_count(self):
        for record in self:
            record.confirm_sales_order_count = len(record.rel_partner_id.sale_order_ids)


#------------------------------Thunder Bolt Button End Here------------------------------
    # For sales_school_ids 
    def get_school_sales(self):
        if len(self.sales_school_ids) == 1:
            params = {
                'type': 'ir.actions.act_window',
                'name': f"{self.name}'s Sale Orders",
                'view_mode': 'form',
                'res_model': 'sale.order',
                'res_id': self.sales_school_ids.ids[0],
                'context': {'create': True, 'default_partner_id': self.rel_partner_id.id},
            }
        else:
            params = {
                'type': 'ir.actions.act_window',
                'name': f"{self.name}'s Sale Orders",
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'domain': [('id', 'in', self.sales_school_ids.ids)],
                'context': {'create': True, 'default_partner_id': self.rel_partner_id.id},
            }
        return params
    
    @api.depends('sales_school_ids')
    def compute_count(self):
        for record in self:
            record.sales_orders_count = len(record.sales_school_ids)

    def create_wizard(self):       
        params = {
            'name':'Add Teacher',
            'type': 'ir.actions.act_window',
            'res_model': 'test.model.wizard',
            'view_mode':'form',
            'target':'new',
            'context':{
                'default_teachar_name': self.teachar_name,
            }
        }
        return params
   
# This method is the for done button
    def button_in_progress(self):
       self.write({
           'state': 'done'
       })

# This method is for cancel button
    def button_cancel(self):
        self.write({
            'state': 'cancel'
        })        



class SchoolProduct(models.Model):
    _name = "school.product"

    student_school_id = fields.Many2one('school.student', string="Add Product")
    product_id = fields.Many2one('product.product',string="Product Name")
    product_label = fields.Selection([("Consumable", "Consumable"), ("Storable", "Storable")], string="Label")
    product_quantity = fields.Integer(string="Quantity")
    product_price = fields.Float(string="Price")
    product_subtotal = fields.Float(compute="compute_subtotal" , string="Subtotal")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    product_tax_ids = fields.Many2many('account.tax',string="Taxes")
    
    @api.depends('product_quantity', 'product_price', 'product_tax_ids')
    def compute_subtotal(self):
        for record in self:
            subtotal = (record.product_quantity * record.product_price)
            total_tax = 0.0
            for tax in record.product_tax_ids:
                total_tax += (tax.amount / 100 )* subtotal
            record.product_subtotal = subtotal + total_tax




class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_school_student_order_ids = fields.Many2one('school.student',string= "Sale Order")

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    school_product_id = fields.Many2one('school.product',string="School Product")

  