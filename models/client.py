from odoo import models ,fields,api
from odoo.exceptions import ValidationError

class Client(models.Model):
   #model_inhertinace_with_new_table
  _name='client'
  _inherit = 'owner'

  name=fields.Char(required=1)
  phone=fields.Char()
  address=fields.Char()
  property_ids=fields.One2many('property','owner_id')
