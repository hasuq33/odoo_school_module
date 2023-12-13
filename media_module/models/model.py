from odoo import fields,api,models
import random
import string
from datetime import datetime,timedelta
import os

class MyProject(models.Model):
	_inherit = "res.users"

	is_signed_up = fields.Boolean('Signed Up',default=True)
	auto_password = fields.Char(string="Passwords")
	expiration_timestamp = fields.Datetime(string="Expiration Timestamp",default=datetime.now())

	def generate_auto_generated_password(self):
		user = self.env.user
		characters = string.ascii_letters + string.digits
		password = ''.join(random.choice(characters) for i in range(8))

		expiration_date = datetime.now() + timedelta(minutes=10)
		user.write({
			'auto_password':password,
			'expiration_timestamp':expiration_date
		})
		template_id = self.env.ref('media_module.name_of_email_template')
		# import pdb; pdb.set_trace()
		template_id.send_mail(user.id,force_send=True)

class MyPartner(models.Model):
	_inherit = "res.partner"

	media_ids = fields.One2many("media.model", "media_partner_id", string="Media")

class MyMedia(models.Model):
	_name = "media.model"

	name = fields.Char(string="Name")
	media =fields.Binary(string="Media")
	media_type = fields.Selection(
		[('Image','Image'),('Video','Video')],
		string="Media Type")
	media_partner_id = fields.Many2one("res.partner",String="Media Partner")
 
	# @api.depends('name')
	# def _compute_media_type(self):
	# 	for media in self:
	# 		if media.name:
	# 			extension = os.path.splitext(media.name.lower())
	# 			if extension in ['.jpg','.jpeg','.png','.gif']:
	# 				media.media_type = 'Image'
	# 			elif extension in ['.mp4','.avi','.mov','.mkv']:
	# 				media.media_type = 'Video'
	# 			else:
	# 				media.media_type = False
	# 		else:
	# 			media.media_type = False				
