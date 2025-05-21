from odoo import models ,fields,api
from odoo.exceptions import ValidationError
class PropertyHistory(models.Model):
  _name='property.history'
  _description = 'Property history' #used for tracking for example when create new record


  user_id=fields.Many2one('res.users')
  propert_id=fields.Many2one('property')
  old_state=fields.Char()
  new_state=fields.Char()
  reason=fields.Char()

  line_ids=fields.One2many('property.history.line','history_id')













class PropertyHistoryLine(models.Model):
    _name = 'property.history.line'

    # name= fields.Many2one('property',string="Name")
    # selleing_price= fields.Float(related='history_id.propert_id.selleing_price',string="Price")


    area = fields.Float()
    description = fields.Char()
    history_id = fields.Many2one('property.history')

    # @api.onchange('history_id')
    # def onchange_type(self):
    #     self.name = self.history_id.propert_id.id

