{
    'name': 'Sale Order Discount (Community)',
    'summary': 'Flexible discounts for sale orders and quotations - Community Edition',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'depends': [
        'sale',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_global_discount_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/report_sale_order.xml',
        'views/web_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

