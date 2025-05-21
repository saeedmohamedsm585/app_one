from odoo import models ,fields,api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
  _inherit = 'res.partner'
  property_id = fields.Many2one('property')
  price =fields.Float(related='property_id.selleing_price')






  # price =fields.Float(compute='_compute_price')


  # @api.depends('property_id.selleing_price')
  # def _compute_price(self):
  #   for rec in self:
  #      rec.price=rec.property_id.selleing_price


