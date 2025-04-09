# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    design_number = fields.Char()
    state = fields.Selection(
        selection=[
            ('manager_approve', "Manager Approve"),
            ('draft', "Quotation"),
            ('sent', "Quotation Sent"),
            ('customer_done', "Cus  tomer Done"),
            ('sale', "Sales Order"),
            ('done', "Locked"),
            ('cancel', "Cancelled"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='manager_approve')

    def action_manager_approve(self):
        for rec in self:
            rec.state = 'draft'

    def action_customer_done(self):
        for rec in self:
            rec.state = 'customer_done'
