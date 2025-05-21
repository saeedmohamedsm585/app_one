# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'App_One',
    'authOr':'saeed mohamed',
    'category': 'Accounting/Accounting',
    'summary': 'Manage lawyer and customer',
    'version': '17.0.0.1.0',
    'depends': ['base','sale','account','mail','contacts'],
    'data': [
       'security/security.xml',
       'security/ir.model.access.csv',
      'data/sequence.xml',
      'views/base_menu.xml',
       'views/property_view.xml',
       'views/property_histoty_view.xml',
        'views/owner_view.xml',
         'views/tag_view.xml',
         'views/sale_order_inherit.xml',
        'views/res_partner_inherit.xml',
        'views/account_move_inherit.xml',
        'wizard/change_state.xml',
        'reports/property_report.xml'

    ],
    'assets':{
        'web.assets_backend':['app_one/static/src/css/proparty.css'],
        'web.report_assets_common':['app_one/static/src/css/font.css']

    },
    'installable': True,
    'auto_install': True,
    'application' : True,
    'license': 'LGPL-3',
}
