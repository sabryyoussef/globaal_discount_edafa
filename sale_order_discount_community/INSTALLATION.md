# Installation Guide - Sale Order Discount (Community Edition)

## Quick Start

### 1. Module Location
The module is located at:
```
/home/sabry3/edu_demo/custom_addons/sale_order_discount_community/
```

### 2. Installation Steps

#### Step 1: Add to Odoo Addons Path
Make sure your Odoo configuration includes this path in the addons_path parameter:
```
addons_path = /home/sabry3/edu_demo/custom_addons,/path/to/other/addons
```

#### Step 2: Update Apps List
Since you're using PyCharm:
1. Log in to your Odoo instance
2. Go to Apps menu
3. Click "Update Apps List" 
4. Click "Update" in the confirmation dialog

#### Step 3: Install the Module
1. In the Apps menu, search for "Sale Order Discount (Community)"
2. Click the "Install" button

## Module Structure

```
sale_order_discount_community/
├── __init__.py                    # Module initialization
├── __manifest__.py                # Module manifest
├── README.md                      # Full documentation
├── INSTALLATION.md                # This file
├── QUICK_START.md                 # Quick start guide
├── models/
│   ├── __init__.py
│   ├── res_partner_global_discount.py    # Main discount model
│   ├── res_partner.py                     # Partner extension
│   ├── sale_order.py                      # Sale order extension
│   └── sale_order_line.py                 # Sale order line extension
├── views/
│   ├── res_partner_global_discount_views.xml   # Discount management views
│   ├── res_partner_views.xml                    # Partner form extension
│   ├── sale_order_views.xml                     # Sale order views
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
   - Go to Sales > Configuration > Sales Orders > Global Discounts
   - Click "New"
   - Name: "Test Discount"
   - Apply Discount: "On Order Lines"
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
   - Set "Discount Applies to": Order Line
   - The discount should auto-populate
   - Add any product
   - Check that the discount is applied (10% in Discount Amount with Percentage method)

4. **Check Quotation Report:**
   - Click "Print > Quotation"
   - Verify discount information appears in the PDF

## Features Included

✅ Global discount master data management
✅ Compound discount support (e.g., "10+5" = 14.5%)
✅ Partner-level discount assignment
✅ Flexible discount application (line or order total)
✅ Multiple discount methods (percentage or fixed amount)
✅ Manual entry and template-based auto-fill
✅ Line Discount Total display
✅ Sale order form integration
✅ Discount display in reports
✅ Customer portal integration
✅ Security (user/manager roles)
✅ Odoo 18 Community Edition compatibility

## Key Odoo 18 Updates Applied

- ✅ Using `list` instead of deprecated `tree` views
- ✅ No deprecated `attrs` or `states` attributes
- ✅ Modern field widget options
- ✅ Proper readonly conditions

## What's NOT Included (Community Edition)

This Community Edition does not include:
- ❌ Customer invoice integration
- ❌ Invoice line discount application
- ❌ Invoice portal templates

For invoice support, use the full `sale_order_global_discount` module with Odoo Enterprise.

## Dependencies

### Required Modules (Community Edition)
- `sale`: Sales Management
- `contacts`: Contact Management

### NOT Required
- ❌ `account`: Accounting module (not needed)

## Troubleshooting

**Module not appearing in Apps:**
- Make sure addons path is correct in config
- Restart Odoo server (if not using auto-reload)
- Update apps list

**Discounts not applying:**
- Check that global_discount_ids field is populated on the order
- Verify discount is properly configured with valid percent format
- Check that you're adding products after setting the discount
- Ensure "Discount Applies to" is set correctly

**Access denied errors:**
- Ensure users have proper Sales/User access rights
- Sales managers should have full access

## Support

For questions or issues, refer to the README.md file for detailed documentation.

