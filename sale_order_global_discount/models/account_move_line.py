from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('product_id')
    def _onchange_product_id_global_discount(self):
        """Apply global discount when product is selected on invoice lines (only for line-based discounts)."""
        if (self.move_id and 
            self.move_id.move_type in ('out_invoice', 'out_refund') and 
            self.move_id.global_discount_ids):
            # Only apply discount on lines if discount type is 'line'
            line_discounts = self.move_id.global_discount_ids.filtered(
                lambda d: d.discount_type == 'line'
            )
            if line_discounts:
                total_discount = sum(line_discounts.mapped('total_percent'))
                self.discount = total_discount

    @api.onchange('quantity')
    def _onchange_quantity_global_discount(self):
        """Apply global discount when quantity changes (only for line-based discounts)."""
        if (self.move_id and 
            self.move_id.move_type in ('out_invoice', 'out_refund') and 
            self.move_id.global_discount_ids and 
            not self.discount):
            # Only apply discount on lines if discount type is 'line'
            line_discounts = self.move_id.global_discount_ids.filtered(
                lambda d: d.discount_type == 'line'
            )
            if line_discounts:
                total_discount = sum(line_discounts.mapped('total_percent'))
                self.discount = total_discount

