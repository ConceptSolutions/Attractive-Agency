# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JobCosting(models.Model):
    _inherit = 'job.costing'

    order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
    )

    def action_view_sale_order(self):
        self.ensure_one()
        # sale_order = self.env['sale.order']
        # cost_ids = sale_order.search([('job_cost_ids', 'in', self.id)]).ids
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'res_id': self.id,
            'domain': [('id', '=', self.order_id.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            # 'target' : self.id,
        }
        return action




class Sales(models.Model):
    _inherit = 'sale.order'

    def _compute_jobcost_count(self):
        jobcost = self.env['job.costing']
        job_cost_ids = self.mapped('job_cost_ids')
        for task in self:
            task.job_cost_count = jobcost.search_count([('id', 'in', job_cost_ids.ids)])

    job_cost_count = fields.Integer(
        compute='_compute_jobcost_count'
    )

    job_cost_ids = fields.One2many(
        'job.costing',
        'order_id',
    )

    # @api.multi
    def order_to_jobcost_action(self):
        self.ensure_one()
        job_cost = self.mapped('job_cost_ids')
        # action = self.env.ref('odoo_job_costing_management.action_job_costing').sudo().read()[0]
        action = self.env["ir.actions.actions"]._for_xml_id("odoo_job_costing_management.action_job_costing")
        action['domain'] = [('id', 'in', job_cost.ids)]
        # action['context'] = {'default_task_id':self.id,'default_project_id':self.project_id.id,'default_analytic_id':self.project_id.analytic_account_id.id,'default_user_id':self.user_id.id}
        print('-----------------',self.analytic_account_id.id)
        action['context'] = {'default_order_id': self.id, 'default_partner_id': self.partner_id.id,
                             'default_analytic_id':self.analytic_account_id.id,
                             'default_user_id': self.env.user.id}
        return action