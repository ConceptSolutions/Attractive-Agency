# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class JobCostLine(models.Model):
    _inherit='job.cost.line'

    delivery_cost = fields.Float('Delivered QTY')




class Stock(models.Model):
    _inherit = 'stock.picking'

    job_cost_id = fields.Many2one(
        'job.costing',
        string='Job Cost'
    )

    def button_validate_cost(self):
        if self.job_cost_id:
            done_pro=[]
            for i in self.move_ids_without_package:
                if i.product_id.id not in done_pro:
                    products=self.env['job.cost.line'].search([('direct_id','=',self.job_cost_id.id),('product_id','=',i.product_id.id)])
                    if len(products)>0:
                        products[0].delivery_cost+=i.product_uom_qty
                    else:
                        self.env['job.cost.line'].create({
                            'product_id':i.product_id.id,
                            'delivery_cost':i.product_uom_qty,
                            'direct_id':self.job_cost_id.id,
                            'date':fields.Date.today(),
                            'job_type':'material',
                        })
                    done_pro.append(i.product_id.id)

class Stock_wizard(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):
        pickings_to_do = self.env['stock.picking']
        pickings_not_to_do = self.env['stock.picking']
        for line in self.immediate_transfer_line_ids:
            if line.to_immediate is True:
                pickings_to_do |= line.picking_id
            else:
                pickings_not_to_do |= line.picking_id

        for picking in pickings_to_do:
            # If still in draft => confirm and assign
            if picking.state == 'draft':
                picking.action_confirm()
                if picking.state != 'assigned':
                    picking.action_assign()
                    if picking.state != 'assigned':
                        raise UserError(
                            _("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))
            picking.move_ids._set_quantities_to_reservation()

        pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        if pickings_to_validate:
            pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate)
            pickings_to_validate = pickings_to_validate - pickings_not_to_do
            for i in pickings_to_validate:
                pickings_to_validate.button_validate_cost()
            return pickings_to_validate.with_context(skip_immediate=True).button_validate()
        return True



class jobcost(models.Model):
    _inherit = 'job.costing'

    count_stock = fields.Integer(compute='count_stock_compute')

    def open_stock_picking(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Delivery Order',
            'res_model': 'stock.picking',
            'domain': [('job_cost_id', '=', self.id)],
            'view_mode': 'tree,form',
        }

    def count_stock_compute(self):
       self.count_stock = self.env['stock.picking'].search_count([('job_cost_id', '=', self.id)])