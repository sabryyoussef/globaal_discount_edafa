from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_discount_ids = fields.Many2many(
        comodel_name='res.partner.global_discount',
        relation='res_partner_global_discount2sale_order_rel',
        column1='sale_id',
        column2='discount_id',
        string='Global Discounts',
        readonly=False,
        help='Global discounts applied to this order',
    )
    discount_applies_to = fields.Selection(
        selection=[
            ('line', 'Order Line'),
            ('global', 'Global'),
        ],
        string='Discount Applies to',
        default='line',
        help='Order Line: Apply discount on each line with discount method\n'
             'Global: Apply discount as a separate line at the end',
    )
    amount_untaxed_before_discount = fields.Monetary(
        string='Untaxed Amount Before Discount',
        compute='_compute_discount_amounts',
        store=True,
        help='Summation of untaxed amount subtotals of lines before global discounts are applied',
    )
    amount_discount_untaxed = fields.Monetary(
        string='Untaxed Discount Amount',
        compute='_compute_discount_amounts',
        store=True,
        help='Total discount amount before taxes',
    )
    line_discount_total = fields.Monetary(
        string='Line Discount',
        compute='_compute_line_discount_total',
        store=True,
        help='Total discount amount from all order lines',
    )
    discount_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Discount Product',
        help='Product used for order-level discount lines',
        compute='_compute_discount_product',
    )

    @api.depends(
        'order_line',
        'order_line.price_unit',
        'order_line.product_uom_qty',
        'order_line.price_subtotal',
        'global_discount_ids',
    )
    def _compute_discount_amounts(self):
        """Calculate amounts before discount and discount amount."""
        for order in self:
            # Amount before any discount (line discounts included)
            amount_before = sum(
                line.price_unit * line.product_uom_qty 
                for line in order.order_line
            )
            order.amount_untaxed_before_discount = amount_before
            
            # Discount amount is the positive difference between pre-discount and current untaxed
            order.amount_discount_untaxed = max(amount_before - order.amount_untaxed, 0.0)

    @api.depends('order_line', 'order_line.price_unit', 'order_line.product_uom_qty', 'order_line.discount')
    def _compute_line_discount_total(self):
        """Calculate total discount amount from all order lines."""
        for order in self:
            total_discount = 0.0
            for line in order.order_line:
                if line.product_id.default_code == 'GLOBAL_DISCOUNT':
                    continue
                # Calculate discount amount: (price_unit * qty) * (discount% / 100)
                line_discount = (line.price_unit * line.product_uom_qty) * (line.discount / 100.0)
                total_discount += line_discount
            order.line_discount_total = total_discount

    def _compute_discount_product(self):
        """Get or create the discount product for order-level discounts."""
        for order in self:
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
            
            order.discount_product_id = discount_product

    @api.onchange('partner_id')
    def _onchange_partner_id_global_discount(self):
        """Auto-populate global discounts from partner."""
        if self.partner_id and self.partner_id.global_discount_ids:
            self.global_discount_ids = [(6, 0, self.partner_id.global_discount_ids.ids)]
        else:
            self.global_discount_ids = [(5, 0, 0)]

    @api.onchange('global_discount_ids', 'order_line', 'discount_applies_to')
    def _onchange_apply_order_discount(self):
        """Apply order-level discount by adding/updating discount line."""
        # Only apply if discount_applies_to is 'global'
        if self.discount_applies_to != 'global':
            # Remove any existing discount lines
            discount_lines = self.order_line.filtered(
                lambda l: l.product_id.default_code == 'GLOBAL_DISCOUNT'
            )
            if discount_lines:
                self.order_line = [(2, line.id, 0) for line in discount_lines]
            return
        
        # Get order-type discounts
        order_discounts = self.global_discount_ids.filtered(
            lambda d: d.discount_type == 'order'
        )
        
        if not order_discounts:
            # Remove any existing discount lines
            discount_lines = self.order_line.filtered(
                lambda l: l.product_id.default_code == 'GLOBAL_DISCOUNT'
            )
            if discount_lines:
                self.order_line = [(2, line.id, 0) for line in discount_lines]
            return
        
        # Calculate discount amount based on subtotal (excluding discount lines)
        regular_lines = self.order_line.filtered(
            lambda l: l.product_id.default_code != 'GLOBAL_DISCOUNT'
        )
        subtotal = sum(regular_lines.mapped('price_subtotal'))
        
        if subtotal == 0:
            return
        
        # Calculate total discount percentage
        total_discount_percent = sum(order_discounts.mapped('total_percent'))
        discount_amount = -(subtotal * total_discount_percent / 100.0)
        
        # Find or create discount line
        discount_line = self.order_line.filtered(
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
            self.order_line = [(0, 0, {
                'product_id': self.discount_product_id.id,
                'name': f'Global Discount: {discount_names} ({total_discount_percent}%)',
                'product_uom_qty': 1,
                'price_unit': discount_amount,
                'tax_id': False,
            })]

