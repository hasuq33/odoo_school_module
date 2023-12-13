from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import base64
from datetime import datetime

class MyAuthentication(AuthSignupHome):
	@http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
	def web_auth_signup(self, *args, **kw):
		phone = kw.get('phone')
		res = super(MyAuthentication, self).web_auth_signup(*args, **kw)
		if res.status_code == 303:
			user_id = request.session.uid
			user= request.env['res.users'].sudo().browse(user_id)
			partner = user.partner_id
			partner.write({'phone':phone})
			user.generate_auto_generated_password()
		return res

	@http.route(['/'],auth="user",type="http",website=True)
	def home_page(self,**post):
		user = request.env.user
		if user and user.is_signed_up:
			auto_psw = post.get('auto_psw')
			usr_psw = user.auto_password
			a= datetime.now() #Current Time
			b= user.expiration_timestamp  # Getting generated 10 minutes later timestamp
			# Comparing timestamp with current time or timestamp field is empty
			if(b == False or (a>b)):
				user.generate_auto_generated_password()
				return request.render("media_module.psw_input_media")
			else:
				if auto_psw == usr_psw:
					media_records = request.env['media.model'].search([('media_partner_id','=',user.partner_id.id)])
					return request.render('media_module.my_website_template',{
						'media_records':media_records
					})
				else:
					return request.render("media_module.psw_input_media")
		else:
			return request.redirect("/web/signup")
		
class MediaController(http.Controller):

	@http.route(['/upload-media'],type="http",auth="user",website=True)
	def media_page(self):
		return request.render("media_module.temp_upload_media")
	
	@http.route(['/upload-media/submit'],type="http",auth="public",website=True)
	def media_page_submit(self,**post):
		user = request.env.user

		if user:
			image_files = http.request.httprequest.files.getlist('user_image')
			video_files = http.request.httprequest.files.getlist('user_video')
			
			if image_files:
				for image in image_files:
					media_attachment = image.read()
					if image.filename == '':
						break

					request.env['media.model'].create({
						'name': image.filename,
						'media':base64.b64encode(media_attachment),
						'media_partner_id': user.partner_id.id,
						'media_type':'Image'
					})
			if video_files:
				for video in video_files:
					media_attachment = video.read()

					if video.filename == '': 
						break
					
					request.env['media.model'].create({
						'name': video.filename,
						'media': base64.b64encode(media_attachment),
						'media_partner_id': user.partner_id.id,
						'media_type':'Video'
					})		
		    				

		return request.redirect('/')	
