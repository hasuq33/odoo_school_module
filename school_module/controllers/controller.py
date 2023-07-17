from odoo import http
from odoo.http import request
import base64

class AdmissionForm(http.Controller):
    # Mention the class name
    @http.route(['/admission'],type='http',auth="public",website=True)
    #Here we mention a url for redirection.
    def admission_form(self):
        return request.render("school_module.tmp_admission_form")
    
    @http.route(['/admission/submit'],type="http",auth="public",website=True)
    # Next controller with url for submitting data from the form
    def admission_form_submit(self,**post):
        email = post.get('email')

        existing_admission = request.env['admission.student'].search([
            ('email','=',email)
        ])
        if existing_admission:
            file = post.get('user_image')
            image_attachment = file.read()
            params = {
             'name': post.get('name'),
            'lname': post.get('lname'),
            'address': post.get('address'),
            'phone': post.get('phone'),
            'user_image':base64.b64encode(image_attachment),
            'message': 'email already exists!'
            }
            return request.render("school_module.tmp_admission_form",params)
        file = post.get('user_image')
        image_attachment = file.read()

        subject_data = []
        subject_count = int(post.get('subject_count'))
        for i in range(0,subject_count+1):
            subject_name = post.get(f"subject_name_{i}")
            sub_priority = post.get(f"sub_priority_{i}")

            if subject_name and sub_priority:
                if sub_priority == "Select Priority":
                    sub_priority = "Optional"
                subject_data.append((0,0,{'subject':subject_name,'sub_priority':sub_priority}))
        
        admission = request.env['admission.student'].create({
            'name': post.get('name'),
            'lname': post.get('lname'),
            'address': post.get('address'),
            'phone': post.get('phone'),
            'email': post.get('email'),
            'user_image':base64.b64encode(image_attachment),
            'subject_ids': subject_data
        })
        vals={
            'admission':admission,
        }
        # inherited the model to pass the values to the model from the our form
        return request.render("school_module.temp_admission_success_form",vals)
    # Finally It will send a request to render the thank you page

    @http.route(['/admission/check_email'], type="json", auth="public", website=True)
    def check_email(self, **post):
        email = post.get('email')
        existing_admission = request.env['admission.student'].sudo().search([('email', '=', email)])
        return {'email_exist': bool(existing_admission)}