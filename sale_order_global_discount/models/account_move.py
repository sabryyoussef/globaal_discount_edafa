from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    global_discount_ids = fields.Many2many(
        comodel_name='res.partner.global_discount',
        relation='res_partner_global_discount2account_move_rel',
        column1='move_id',
        column2='discount_id',
        string='Global Discounts',
        readonly=False,
        help='Global discounts applied to this invoice',
    )
    discount_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Discount Product',
        help='Product used for invoice-level discount lines',
        compute='_compute_discount_product',
    )

    def _compute_discount_product(self):
        """Get or create the discount product for invoice-level discounts."""
        for move in self:
            # Try to find existing discount product
            discount_product = self.env['product.product'].search([
                ('default_code', '=', 'GLOBAL_DISCOUNT')
            ], limit=1)
            
            if not discount_product:
                # Create discount product if it doesn't exist
                discount_product = self.env['product.product'].sudo().create({
                    'name': 'Global Discount',
                    'default_code': 'GLOBAL_DISCOUNT',
                    'type': 'service',
                    'invoice_policy': 'order',
                    'list_price': 0.0,
                    'purchase_ok': False,
                    'sale_ok': True,
                })
            
            move.discount_product_id = discount_product

    @api.onchange('partner_id')
    def _onchange_partner_id_global_discount(self):
        """Auto-populate global discounts from partner for customer invoices."""
        if self.move_type in ('out_invoice', 'out_refund'):
            if self.partner_id and self.partner_id.global_discount_ids:
                self.global_discount_ids = [(6, 0, self.partner_id.global_discount_ids.ids)]
            else:
                self.global_discount_ids = [(5, 0, 0)]

    @api.onchange('global_discount_ids', 'invoice_line_ids')
    def _onchange_apply_invoice_discount(self):
        """Apply invoice-level discount by adding/updating discount line."""
        if self.move_type not in ('out_invoice', 'out_refund'):
            return
        
        # Get order-type discounts
        order_discounts = self.global_discount_ids.filtered(
            lambda d: d.discount_type == 'order'
        )
        
        if not order_discounts:
            # Remove any existing discount lines
            discount_lines = self.invoice_line_ids.filtered(
                lambda l: l.product_id.default_code == 'GLOBAL_DISCOUNT'
            )
            if discount_lines:
                self.invoice_line_ids = [(2, line.id, 0) for line in discount_lines]
            return
        
        # Calculate discount amount based on subtotal (excluding discount lines)
        regular_lines = self.invoice_line_ids.filtered(
            lambda l: l.product_id.default_code != 'GLOBAL_DISCOUNT'
        )
        subtotal = sum(regular_lines.mapped('price_subtotal'))
        
        if subtotal == 0:
            return
        
        # Calculate total discount percentage
        total_discount_percent = sum(order_discounts.mapped('total_percent'))
        discount_amount = -(subtotal * total_discount_percent / 100.0)
        
        # Find or create discount line
        discount_line = self.invoice_line_ids.filtered(
            lambda l: l.product_id.default_code == 'GLOBAL_DISCOUNT'
        )
        
        discount_names = ', '.join(order_discounts.mapped('name'))
        
        if discount_line:
            # Update existing line
            discount_line[0].write({
                'price_unit': discount_amount,
                'name': f'Global Discount: {discount_names} ({total_discount_percent}%)',
            })
        else:
            # Create new discount line
            self.invoice_line_ids = [(0, 0, {
                'product_id': self.discount_product_id.id,
                'name': f'Global Discount: {discount_names} ({total_discount_percent}%)',
                'quantity': 1,
                'price_unit': discount_amount,
                'tax_ids': False,
            })]

