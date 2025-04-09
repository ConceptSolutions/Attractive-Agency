# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    mobile_required = fields.Boolean(related='company_id.mobile_required')

    @api.model
    def _get_default_company(self):
        return self.env["res.company"].browse(self.env.company.id)

    company_id = fields.Many2one('res.company', string='Company', required=True, default=_get_default_company)