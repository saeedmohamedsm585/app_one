from odoo import fields,models
from odoo.exceptions import ValidationError

class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id=fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
    ], default='draft')
    reason=fields.Char(required=1)


    def action_confirm(self):
        if  self.property_id.state !='closed':
            raise ValidationError('you can change state closed only')
        else:
            self.property_id.state=self.state
            self.property_id.create_history_record('closed',self.state,self.reason)