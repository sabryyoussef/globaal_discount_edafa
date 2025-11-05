from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    global_discount_ids = fields.Many2many(
        comodel_name='res.partner.global_discount',
        relation='res_partner_global_discount2res_partner_rel',
        column1='partner_id',
        column2='discount_id',
        string='Global Discounts',
        help='Global discounts that will be applied to sales orders and invoices',
    )

