from contextlib import contextmanager
from odoo import models
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"


    @contextmanager
    def _check_balanced(self, container):
        threshold = 50  # 👈 فرق مسموح به
        try:
             if self._context.get('active_model') == 'account.move':
                for move in self:
                    
                    # print('payment_difference_handling', move.payment_id.payment_difference_handling)
                    # print('payment_difference', move.payment_id.payment_difference)
                    # if move.payment_id and move.payment_id.payment_difference_handling == "reconcile":
                    debit = sum(line.debit for line in move.line_ids)
                    credit = sum(line.credit for line in move.line_ids)
                    print('debit', debit)
                    print('credit', credit)

                    if abs(debit - credit) <= threshold:
                        _logger.warning(">>> SKIPPING BALANCE CHECK (diff=%.2f) <<<", debit - credit)
                        yield
                        return
        except Exception as e:
            _logger.error(">>> ERROR in custom _check_balanced: %s", e)

        # fallback → السلوك العادي
        with super(AccountMove, self)._check_balanced(container):
            yield
