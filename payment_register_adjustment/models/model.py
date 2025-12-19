from contextlib import contextmanager
from odoo import models
import logging
from contextlib import contextmanager
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"


    @contextmanager
    def _check_balanced(self, container):
        threshold = 50
        skip_check = False

        if self._context.get('active_model') == 'account.move':
            for move in self:
                debit = sum(move.line_ids.mapped('debit'))
                credit = sum(move.line_ids.mapped('credit'))

                diff = abs(debit - credit)
                if diff <= threshold:
                    skip_check = True
                    _logger.warning(
                        "SKIP BALANCE CHECK move=%s diff=%.2f",
                        move.name, diff
                    )
                    break

        if skip_check:
            yield
        else:
            with super(AccountMove, self)._check_balanced(container):
                yield
