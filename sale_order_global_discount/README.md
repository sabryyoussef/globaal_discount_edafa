# Sale Order Global Discount

## Overview

This Odoo 18 module adds global discount functionality to sales orders, quotations, and customer invoices. Global discounts can be configured as simple percentages or compound discounts and are automatically applied to order lines and invoice lines.

## Features

- **Global Discount Management**: Create and manage reusable discount schemes
- **Compound Discounts**: Support for sequential discounts (e.g., "10+5" = 14.5% total)
- **Partner Integration**: Assign default discounts to partners
- **Automatic Application**: Discounts automatically apply when products are added to lines
- **Sales Orders & Quotations**: Full integration with sale orders and quotations
- **Customer Invoices**: Automatic discount application on customer invoices
- **Reporting**: Display discounts on printed reports and customer portal
- **Security**: Role-based access control (read for users, full access for sales managers)

## Installation

1. Copy the module folder to your Odoo addons directory
2. Update the apps list in Odoo
3. Search for "Sale Order Global Discount"
4. Click Install

## Usage

### Creating Global Discounts

1. Navigate to Sales > Configuration > Global Discounts
2. Click "New"
3. Enter a name (e.g., "VIP Discount")
4. Enter discount percentage:
   - Simple: "10" = 10% discount
   - Compound: "10+5" = 10% then 5% on remainder (14.5% total)
   - Multiple: "20+10+5" = sequential application
5. The "Total Percent" field shows the calculated combined discount

### Assigning Discounts to Partners

1. Open a partner (contact/customer)
2. Go to "Sales & Purchase" tab
3. In the "Global Discounts" section, select one or more discounts
4. Save the partner

### Using Discounts in Sales Orders

**Automatic Method:**
1. Create a new sales order
2. Select a partner with assigned discounts
3. Discounts are automatically populated
4. Add products - discounts apply automatically to each line

**Manual Method:**
1. Create a new sales order
2. Manually select global discounts from the dropdown
3. Add products - discounts apply automatically

### Using Discounts in Invoices

Discounts work the same way in customer invoices:
1. Create a customer invoice
2. Select a partner (discounts auto-populate) or select manually
3. Add products - discounts apply automatically

### Viewing Discount Information

- **Sale Order Form**: Shows discount amounts before the total
- **Invoice Form**: Displays applied discounts
- **Printed Reports**: Includes discount breakdown
- **Customer Portal**: Customers can see applied discounts on quotations and invoices

## Technical Details

### Models

- `res.partner.global_discount`: Master discount definitions
- `res.partner`: Extended with global_discount_ids
- `sale.order`: Extended with discount tracking and computed fields
- `sale.order.line`: Auto-applies discounts on product selection
- `account.move`: Extended with discount support for customer invoices
- `account.move.line`: Auto-applies discounts on product selection

### Discount Calculation

Compound discounts are calculated using the formula:
```
Total = 1 - (1 - d1) × (1 - d2) × ... × (1 - dn)
```

Example: "10+5" = 1 - (1 - 0.10) × (1 - 0.05) = 0.145 (14.5%)

### Security

- **Base Users**: Read-only access to discounts
- **Sales Managers**: Full CRUD access to discounts

## Odoo 18 Compatibility

This module is built specifically for Odoo 18 with:
- Use of `list` views instead of deprecated `tree` views
- Proper readonly attributes without deprecated `states` syntax
- Compatible with `account.move` (not old `account.invoice`)
- Modern widget options and field attributes

## Dependencies

- `sale`: Sales Management
- `account`: Accounting & Invoicing
- `contacts`: Contact Management

## License

LGPL-3

## Support

For issues, questions, or contributions, please contact your Odoo implementation partner.

## Changelog

### Version 18.0.1.0.0
- Initial release for Odoo 18
- Global discount management
- Sale order and invoice integration
- Compound discount support
- Portal and report integration

