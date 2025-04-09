# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    type_customer_new = fields.Selection([
        ('a', 'عملاء دائمين'),
        ('b', 'عملاء معارض')],
        default='a',string='Customer Type'
    )