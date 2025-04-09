# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Sales(models.Model):
    _inherit = 'sale.order'

    type_customer_new = fields.Selection([
        ('a', 'عملاء دائمين'),
        ('b', 'عملاء معارض')],
        default='a',string='Customer Type'
    )

    @api.onchange('partner_id')
    def get_partner_type(self):
        if self.partner_id:
            self.type_customer_new = self.partner_id.type_customer_new



class PivotInheritReport(models.Model):
   _inherit = 'sale.report'

   type_customer_new = fields.Selection([
       ('a', 'عملاء دائمين'),
       ('b', 'عملاء معارض')],
      string='Customer Type'
   )

   def _select_additional_fields(self):
       res = super()._select_additional_fields()
       res['type_customer_new'] = "s.type_customer_new"
       return res

   def _group_by_sale(self):
       res = super()._group_by_sale()
       res += """,
              s.type_customer_new"""
       return res