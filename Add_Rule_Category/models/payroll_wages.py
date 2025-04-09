from odoo import models, fields, api ,_
from odoo.exceptions import UserError, ValidationError

from collections import defaultdict


class hrpayroll(models.Model):
    _inherit = 'hr.payslip'

    gross_wage = fields.Monetary(compute='_compute_alw_ded_gross', store=True)
    allowance_wage = fields.Float(compute='_compute_alw_ded_gross',store=True)
    deduction_wage = fields.Float(compute='_compute_alw_ded_gross',store=True)
    basic_wage = fields.Monetary(compute='_compute_basic_net',store=True)
    net_wage = fields.Monetary(compute='_compute_basic_net', store=True)

    @api.depends('line_ids')
    def _compute_basic_net(self):
        line_values = (self._origin)._get_line_values(['BASIC', 'NET'])
        for payslip in self:
            payslip.basic_wage = line_values['BASIC'][payslip._origin.id]['total']
            payslip.net_wage = line_values['NET'][payslip._origin.id]['total']

    @api.depends('line_ids')
    def _compute_alw_ded_gross(self):
        line_values = (self._origin)._get_line_values(['ALW', 'DED','GROSS'])
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",line_values)
        for payslip in self:
            amount_ded=amount_alw=0
            for line in payslip.line_ids:

                if line.category_id.code=='DED':
                    amount_ded+=line.amount
                elif line.category_id.code=='ALW':
                    amount_alw+=line.amount

            payslip.allowance_wage = amount_alw
            payslip.deduction_wage = amount_ded
            payslip.gross_wage = line_values['GROSS'][payslip._origin.id]['total']

    def _get_line_values(self, code_list, vals_list=None, compute_sum=False):
        if vals_list is None:
            vals_list = ['total']
        valid_values = {'quantity', 'amount', 'total'}
        if set(vals_list) - valid_values:
            raise UserError(_('The following values are not valid:\n%s', '\n'.join(list(set(vals_list) - valid_values))))
        result = defaultdict(lambda: defaultdict(lambda: dict.fromkeys(vals_list, 0)))
        if not self:
            return result
        # self.flush()
        selected_fields = ','.join('SUM(%s) AS %s' % (vals, vals) for vals in vals_list)
        self.env.cr.execute("""
            SELECT
                p.id,
                pl.code,                
                %s
            FROM hr_payslip_line pl
            JOIN hr_payslip p
            ON p.id IN %s
            AND pl.slip_id = p.id
            AND pl.code IN %s
            GROUP BY p.id, pl.code
        """ % (selected_fields, '%s', '%s'), (tuple(self.ids), tuple(code_list)))

        request_rows = self.env.cr.dictfetchall()

        for row in request_rows:
            code = row['code']
            payslip_id = row['id']
            for vals in vals_list:
                if compute_sum:
                    result[code]['sum'][vals] += float(row[vals] or 0)
                result[code][payslip_id][vals] += float(row[vals] or 0)
        return result

