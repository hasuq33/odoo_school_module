from odoo import http
from odoo.http import request

class MyController(http.Controller):

    @http.route(['/'],auth="user",type="http",website=True)
    def home_page(self, **post):
        user = request.env.user
        if user and user.is_signed_up:
            return request.render('school_module.tmp_admission_form')
        else:
            return request.redircet("/web/signup")
    
    @http.route(['/web/signup'],type="http",auth="public",website=True)
    def sign_up_page(seld,**post):
        return request.render("auth_signup.signup")
