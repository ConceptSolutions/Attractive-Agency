from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mobile_required = fields.Boolean(related='company_id.mobile_required', string='Contact Mobile Is Mandatory', readonly=False)
