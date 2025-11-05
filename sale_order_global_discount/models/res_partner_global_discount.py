import re

from odoo import _, api, exceptions, fields, models


class ResPartnerGlobalDiscount(models.Model):
    _name = 'res.partner.global_discount'
    _description = 'Global Discounts'

    name = fields.Char(
        string='Name',
        required=True,
    )
    percent = fields.Char(
        string='Percent',
        required=True,
        help='Discount percentage. Supports compound discounts like "10+5" (10% then 5% on remainder)',
    )
    total_percent = fields.Float(
        string='Total Percent',
        compute='_compute_total_percent',
        store=True,
    )
    discount_type = fields.Selection(
        selection=[
            ('line', 'On Order Lines'),
            ('order', 'On Order Total'),
        ],
        string='Apply Discount',
        required=True,
        default='line',
        help='Line: Apply discount on each order/invoice line\n'
             'Order: Apply discount as a separate line on order/invoice total',
    )
    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='res_partner_global_discount2res_partner_rel',
        column1='discount_id',
        column2='partner_id',
        string='Partners',
    )
    partner_count = fields.Integer(
        string='Partner Count',
        compute='_compute_partner_count',
    )

    @staticmethod
    def _validate_discount(discount):
        """Validate discount format using regex."""
        discount_regex = re.compile(
            r'^(\s*[-+]{0,1}\s*\d+([,.]\d+)?){1}'
            r'(\s*[-+]\s*\d+([,.]\d+)?\s*)*$'
        )
        if discount and not discount_regex.match(discount):
            return False
        return True

    @api.constrains('percent')
    def _check_percent_format(self):
        """Validate that the percent field has correct format."""
        for discount in self:
            if not discount.percent:
                continue
            if not self._validate_discount(discount.percent):
                raise exceptions.ValidationError(
                    _('Warning! The discount format is not recognized. '
                      'Please use format like "10" or "10+5" for compound discounts.'))

    def action_view_partners(self):
        """Open list of partners with this discount."""
        self.ensure_one()
        if not self.partner_ids:
            return {'type': 'ir.actions.act_window_close'}
        action = self.env.ref('contacts.action_contacts').read()[0]
        action['domain'] = [('id', 'in', self.partner_ids.ids)]
        action['context'] = {
            'search_default_global_discount_ids': self.id,
        }
        return action

    @api.depends('partner_ids')
    def _compute_partner_count(self):
        """Count partners using this discount."""
        for discount in self:
            discount.partner_count = len(discount.partner_ids)

    @api.depends('percent')
    def _compute_total_percent(self):
        """Calculate total discount percentage from compound discounts."""
        def _normalize_discount(discount):
            discount = discount.replace(' ', '')
            discount = discount.replace(',', '.')
            if discount and discount[0] == '+':
                discount = discount[1:]
            return discount

        for discount in self:
            if not discount.percent:
                discount.total_percent = 0.0
                continue
            
            normalized_discount = _normalize_discount(discount.percent)
            tokens = re.split(r'([+-])', normalized_discount)
            numeric_tokens = []
            last_sign = 1
            
            for token in tokens:
                if not token:
                    continue
                if token == '-':
                    last_sign = -1
                elif token == '+':
                    last_sign = 1
                else:
                    numeric_tokens.append(float(token) * last_sign)
            
            # Calculate compound discount: 1 - (1-d1) * (1-d2) * ...
            marginal_discount = 1
            for token in numeric_tokens:
                marginal_discount = marginal_discount * (1 - (token / 100))
            
            total_discount = 1 - marginal_discount
            discount.total_percent = round(total_discount * 100, 2)

