from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount_method = fields.Selection(
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed'),
        ],
        string='Discount Method',
        default='percentage',
    )
    discount_amount_value = fields.Monetary(
        string='Discount Amount',
        currency_field='currency_id',
        help='Fixed discount amount or percentage based on discount method',
    )

    @api.onchange('discount_method', 'discount_amount_value', 'price_unit')
    def _onchange_discount_calculation(self):
        """Calculate discount percentage based on method and amount."""
        if not self.price_unit or self.price_unit == 0:
            return
        
        if self.discount_method == 'percentage':
            # Percentage mode: discount_amount_value is the percentage
            self.discount = self.discount_amount_value
        elif self.discount_method == 'fixed':
            # Fixed mode: calculate percentage from fixed amount
            if self.discount_amount_value:
                self.discount = (self.discount_amount_value / self.price_unit) * 100
            else:
                self.discount = 0.0

    @api.onchange('product_id')
    def _onchange_product_id_global_discount(self):
        """Apply global discount when product is selected."""
        if not self.order_id:
            return
        
        # Check if order has global discounts and applies to lines
        if (self.order_id.global_discount_ids and 
            self.order_id.discount_applies_to == 'line'):
            # Filter for line-type discounts
            line_discounts = self.order_id.global_discount_ids.filtered(
                lambda d: d.discount_type == 'line'
            )
            if line_discounts:
                total_discount = sum(line_discounts.mapped('total_percent'))
                self.discount_method = 'percentage'
                self.discount_amount_value = total_discount
                self.discount = total_discount

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty_global_discount(self):
        """Apply global discount when quantity changes."""
        if not self.order_id or self.discount:
            return
        
        # Check if order has global discounts and applies to lines
        if (self.order_id.global_discount_ids and 
            self.order_id.discount_applies_to == 'line'):
            # Filter for line-type discounts
            line_discounts = self.order_id.global_discount_ids.filtered(
                lambda d: d.discount_type == 'line'
            )
            if line_discounts:
                total_discount = sum(line_discounts.mapped('total_percent'))
                self.discount_method = 'percentage'
                self.discount_amount_value = total_discount
                self.discount = total_discount

