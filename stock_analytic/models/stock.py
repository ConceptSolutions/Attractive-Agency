# Copyright 2013 Julius Network Solutions
# Copyright 2015 Clear Corp
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2017 ForgeFlow S.L.
# Copyright 2018 Hibou Corp.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )

    @api.depends('account_id', 'partner_id', 'product_id', 'analytic_account_id')
    def _compute_analytic_distribution(self):
        super()._compute_analytic_distribution()
        for line in self:
            if line.analytic_account_id:
                line.analytic_distribution = {str(line.analytic_account_id.id): float(100)}


class StockMove(models.Model):
    _inherit = "stock.move"

    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )

    # analytic_tag_ids = fields.Many2many("account.analytic.tag", string="Analytic Tags")

    def _prepare_account_move_line(
            self, qty, cost, credit_account_id, debit_account_id, svl_id, description
    ):
        self.ensure_one()
        # svl_id = self.env['stock.valuation.layer'].browse(svl_id)
        res = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id, svl_id, description
        )
        for line in res:
            if (
                    line[2]["account_id"]
                    != self.product_id.categ_id.property_stock_valuation_account_id.id
            ):
                # Add analytic account in debit line
                if self.analytic_account_id:
                    line[2].update({"analytic_account_id": self.analytic_account_id.id})
                # Add analytic tags in debit line
                # if self.analytic_tag_ids:
                #     line[2].update(
                #         {"analytic_tag_ids": [(6, 0, self.analytic_tag_ids.ids)]}
                #     )
        return res

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        fields = super()._prepare_merge_moves_distinct_fields()
        fields.append("analytic_account_id")
        return fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    analytic_account_id = fields.Many2one(related="move_id.analytic_account_id")
