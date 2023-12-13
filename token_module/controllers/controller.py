from odoo import http
from odoo.http import request

class PdfLinkGenerator(http.Controller):

    @http.route(['/download/invoice/<int:id>'],type='http',auth='public')
    def action_generate_invoice_pdf(self,id):
        invoice_id = request.env['account.move'].sudo().search([('id', '=', id),('move_type','=','out_invoice')], limit=1)

        if not invoice_id:
            error_message = f"Invoice is not found"
            return request.make_response(error_message,headers=[('Content-Type','text/plain')],status=400)
      
        pdf_url = invoice_id.action_generate_invoice_pdf()           
        return request.redirect(pdf_url.get('url'))
