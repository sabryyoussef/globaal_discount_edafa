{
    'name': 'Sale Order Global Discount',
    'summary': 'Global discounts for sale orders, quotations, and customer invoices',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'category': 'Sales',
    'version': '18.0.2.0.0',
    'depends': [
        'sale',
        'account',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_global_discount_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/report_sale_order.xml',
        'views/web_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

