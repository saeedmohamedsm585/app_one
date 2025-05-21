from odoo import models ,fields,api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Property(models.Model):
  _name='property'
  _description = 'New Property' #used for tracking for example when create new record
  _inherit = ['mail.thread','mail.activity.mixin']

  ref =fields.Char(default='new',readonly=1)

  name=fields.Char(required=1,size=20)
  description=fields.Text(tracking=1)
  postcode=fields.Char(required=1)
  date_availabilty =fields.Date(tracking=1)
  expected_date =fields.Date()
  expected_price=fields.Float(digits=(0,4))
  selleing_price=fields.Float(digits=(0,4))
  diff =fields.Float(compute='_compute_diff')
  bedrooms=fields.Integer()
  living_area=fields.Integer()
  facades=fields.Integer()
  garage=fields.Boolean()
  garden=fields.Boolean()
  is_late=fields.Boolean()
  active = fields.Boolean(default=True) #used for archiving
  garden_area=fields.Integer()

  create_time=fields.Datetime(default=fields.Datetime.now())

  next_time=fields.Datetime(compute='_compute_next_time')

  garden_orintation=fields.Selection([
      ('north','North'),
      ('south','South'),
      ('east','East'),
      ('west','West')
  ],default='north')

  state= fields.Selection([
      ('draft','Draft'),
      ('pending','Pending'),
      ('sold','Sold'),
      ('closed', 'Closed'),
  ],default='draft')

  owner_id=fields.Many2one('owner')

  tag_ids =fields.Many2many('tag')


  line_ids =fields.One2many('property.line','property_id')

  owner_address=fields.Char(related='owner_id.address',readonly=0)
  owner_phone=fields.Char(related='owner_id.phone')




  _sql_constraints =[
     ('unique_name','unique("name")','this name is exist')
  ]

  @api.depends('create_time')
  def _compute_next_time(self):
      for rec in self:
          if rec.create_time:
              rec.next_time=rec.create_time + timedelta(hours=6)
          else:
              rec.next_time=False



  @api.constrains('bedrooms')
  def _check_bedroom_greater_zero(self):
      for rec in self :
          if rec.bedrooms ==0 :
              raise ValidationError('plz add valid number of bedrooms')


  @api.depends('expected_price','selleing_price','owner_id.phone')
  def _compute_diff(self):
      for rec in self:
          rec.diff=rec.expected_price - rec.selleing_price

  @api.onchange('expected_price')
  def _onchange_expected_price(self):
      for rec in self:
          print("inside onchange")
          return {
              'warning':{'title':'waring','message':'negative value','type':'notification'}
          }


  def action_draft(self):
      for rec in self:
          #put your logic
          rec.create_history_record(rec.state,'draft')
          rec.state='draft'



  def action_pending(self):
      for rec in self:
          rec.create_history_record(rec.state,'pending')

          rec.write({
              'state':'pending'
          })

  def action_sold(self):
      for rec in self:
          rec.create_history_record(rec.state,'sold')

          rec.state='sold'

  def action_closed(self):
      for rec in self:
          rec.create_history_record(rec.state,'closed')

          rec.state = 'closed'


  def check_expcted_selling_date(self):
      # print(self)
      property_ids=self.search([])
      # print(property_ids)

      for rec in property_ids:
          if rec.expected_date and rec.expected_date < fields.date.today() :
              rec.is_late=True



  @api.model_create_multi
  def create(self, vals):
      res = super(Property,self).create(vals)
      if res.ref =='new':
          res.ref= self.env['ir.sequence'].next_by_code('property_seq')
          return res
      #logic
      #print("inside create method")

# for Read
  @api.model
  def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
      res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
      # logic
      print("inside read method")
      return res

  def write(self, vals):
      res = super(Property, self).write(vals)
      # logic
      #print("inside write method")
      return res

  def unlink(self):

      res = super(Property, self).unlink()
      # logic
      print("inside delete method")
      return res

  def action(self):
      self.env['owner'].create({
          'name':'noraaaa' ,
          'phone':'0111111111' ,

      })
      print(self.env['owner'].search([])) # return record ids
      print(self.env['property'].search([])) # return record ids


  def create_history_record(self,old_state,new_state,reason=""):
      for rec in self:
         # print(rec.id)
          rec.env['property.history'].create({

              # 'user_id':rec.user.id,
              'user_id':rec.env.uid,
              'propert_id':rec.id,
              'old_state':old_state,
              'new_state':new_state,
              'reason':reason or "",
              'line_ids':[(0,0,{'description':line.description,'area':line.area}) for line in rec.line_ids]#magic tuple
          })



  def action_open_change_state(self):
      action=self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
      action['context']={'default_property_id':self.id}
      return action


  def action_open_related_owner(self):
      action=self.env['ir.actions.actions']._for_xml_id('app_one.owner_action') # get action
      view_id=self.env.ref('app_one.owner_view_form').id  #get form view of owner
      action['res_id']= self.owner_id.id
      action['views']= [[view_id,'form']] # to view form view only not tree view
      return action




class PropertyLine(models.Model):
    _name='property.line'
    area=fields.Float()
    description = fields.Char()
    property_id =fields.Many2one('property')