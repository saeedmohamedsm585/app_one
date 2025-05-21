from odoo import models ,fields,api
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
  _inherit = 'account.move'


  def action_do_something(self):
    print(self,'action_do_something method')


