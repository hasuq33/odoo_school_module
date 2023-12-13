from odoo import http
from odoo.http import request

class MyController(http.Controller):

    @http.route(['/'],auth="user",type="http",website=True)
    def home_page(self, **post):
        user = request.env.user
        if user and user.is_signed_up:
            return request.render('school_module.temp_welcome_page')
        else:
            return request.redircet("/web/signup")
    
    @http.route(['/web/signup'],type="http",auth="public",website=True)
    def sign_up_page(self,**post):
        if request.httprequest.method == 'POST':
            # We are getting request from name given in template
            name = post.get('name')
            email = post.get('login')
            password = post.get('password')
            phone = post.get('phone')

            # Create a Partner here
            partner = request.env['res.partner'].sudo().create({
                'name':name,
                'phone': phone,
            })
            # Create a user
            user = request.env['res.users'].sudo().create({
                'name': name,
                'login':email,
                'password':password,
                'partner_id': partner.id
            })
            
           
            return request.redirect("/web/login")

        else:    
            return request.render("auth_signup.signup")
    
   
