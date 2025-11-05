# Installation Guide - Sale Order Global Discount Module

## Quick Start

### 1. Module Location
The module has been created at:
```
/home/sabry3/global_disc_modules/sale_order_global_discount/
```

### 2. Installation Steps

#### Step 1: Add to Odoo Addons Path
Make sure your Odoo configuration includes this path in the addons_path parameter:
```
addons_path = /home/sabry3/global_disc_modules,/path/to/other/addons
```

#### Step 2: Update Apps List
Since you're using PyCharm, you can:
1. Log in to your Odoo instance
2. Go to Apps menu
3. Click "Update Apps List" 
4. Click "Update" in the confirmation dialog

#### Step 3: Install the Module
1. In the Apps menu, search for "Sale Order Global Discount"
2. Click the "Install" button

## Module Structure

```
sale_order_global_discount/
├── __init__.py                    # Module initialization
├── __manifest__.py                # Module manifest
├── README.md                      # Full documentation
├── INSTALLATION.md                # This file
├── models/
│   ├── __init__.py
│   ├── res_partner_global_discount.py    # Main discount model
│   ├── res_partner.py                     # Partner extension
│   ├── sale_order.py                      # Sale order extension
│   ├── sale_order_line.py                 # Sale order line extension
│   ├── account_move.py                    # Invoice extension
│   └── account_move_line.py               # Invoice line extension
├── views/
│   ├── res_partner_global_discount_views.xml   # Discount management views
│   ├── res_partner_views.xml                    # Partner form extension
│   ├── sale_order_views.xml                     # Sale order views
│   ├── account_move_views.xml                   # Invoice views
│   ├── report_sale_order.xml                    # Report templates
│   └── web_template.xml                         # Portal templates
├── security/
│   └── ir.model.access.csv                      # Access rights
└── static/
    └── description/
        └── icon.png.txt                         # Icon placeholder
```

## Quick Test

After installation, test the module:

1. **Create a Global Discount:**
   - Go to Sales > Configuration > Global Discounts
   - Click "New"
   - Name: "Test Discount"
   - Percent: "10"
   - Save

2. **Assign to a Partner:**
   - Open any customer
   - Go to "Sales & Purchase" tab
   - Select "Test Discount" in Global Discounts field
   - Save

3. **Create a Sale Order:**
   - Go to Sales > Orders > Quotations
   - Click "New"
   - Select the customer from step 2
   - The discount should auto-populate
   - Add any product
   - Check that the discount is applied to the line (10% in discount field)

4. **Check Quotation Report:**
   - Click "Print > Quotation"
   - Verify discount information appears in the PDF

## Features Included

✅ Global discount master data management
✅ Compound discount support (e.g., "10+5" = 14.5%)
✅ Partner-level discount assignment
✅ Automatic application on sale order lines
✅ Automatic application on invoice lines
✅ Sale order form integration
✅ Invoice form integration
✅ Discount display in reports
✅ Customer portal integration
✅ Security (user/manager roles)
✅ Odoo 18 compatibility (list views, proper readonly syntax)

## Key Odoo 18 Updates Applied

- ✅ Using `list` instead of deprecated `tree` views
- ✅ No deprecated `attrs` or `states` attributes
- ✅ Using `account.move` instead of old `account.invoice`
- ✅ Modern field widget options
- ✅ Proper readonly conditions

## Troubleshooting

**Module not appearing in Apps:**
- Make sure addons path is correct in config
- Restart Odoo server (if not using auto-reload)
- Update apps list

**Discounts not applying:**
- Check that global_discount_ids field is populated on the order
- Verify discount is properly configured with valid percent format
- Check that you're adding products after setting the discount

**Access denied errors:**
- Ensure users have proper Sales/User access rights
- Sales managers should have full access

## Support

For questions or issues, refer to the README.md file for detailed documentation.

