from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_valid_journal_types(self):
        print('self.payment_id', self.payment_id)
        print('self.env.context.get"(is_payment)"', self.env.context.get('is_payment'))
        if self.is_sale_document(include_receipts=True):
            return ['sale']
        elif self.is_purchase_document(include_receipts=True):
            return ['purchase']
        elif self.payment_id or self.env.context.get('is_payment'):
            return ['bank', 'cash']
        return ['general']

    def _search_default_journal(self):
        if self.payment_id and self.payment_id.journal_id:
            return self.payment_id.journal_id
        if self.statement_line_id and self.statement_line_id.journal_id:
            return self.statement_line_id.journal_id
        if self.statement_line_ids.statement_id.journal_id:
            return self.statement_line_ids.statement_id.journal_id[:1]

        journal_types = self._get_valid_journal_types()
        company_id = (self.company_id or self.env.company).id
        domain = [('company_id', '=', company_id), ('type', 'in', journal_types)]

        journal = None
        # the currency is not a hard dependence, it triggers via manual add_to_compute
        # avoid computing the currency before all it's dependences are set (like the journal...)
        if self.env.cache.contains(self, self._fields['currency_id']):
            currency_id = self.currency_id.id or self._context.get('default_currency_id')
            if currency_id and currency_id != self.company_id.currency_id.id:
                currency_domain = domain + [('currency_id', '=', currency_id)]
                journal = self.env['account.journal'].search(currency_domain, limit=1)

        if not journal:
            journal = self.env['account.journal'].search(domain, limit=1)

        return journal