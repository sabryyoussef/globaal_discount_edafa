# Sale Order Global Discount

## Overview

This Odoo 18 module adds flexible discount functionality to sales orders, quotations, and customer invoices. Discounts can be applied either per line or globally on the entire order, with support for both percentage and fixed amount discounts.

## Features

### Core Features
- **Global Discount Management**: Create and manage reusable discount schemes
- **Compound Discounts**: Support for sequential discounts (e.g., "10+5" = 14.5% total)
- **Partner Integration**: Assign default discounts to partners
- **Flexible Discount Application**: Choose between line-level or order-level discounts
- **Multiple Discount Methods**: Support for both percentage and fixed amount discounts
- **Manual & Automatic**: Manual entry or auto-fill from global discount templates
- **Sales Orders & Quotations**: Full integration with sale orders and quotations
- **Customer Invoices**: Automatic discount application on customer invoices
- **Reporting**: Display discounts on printed reports and customer portal
- **Security**: Role-based access control (read for users, full access for sales managers)

### Discount Application Types

#### 1. Order Line Discounts
- Apply discounts to individual product lines
- Choose discount method per line:
  - **Percentage**: e.g., 10% off
  - **Fixed Amount**: e.g., $162.00 off
- View "Line Discount Total" in order totals
- Visible discount columns in order lines table

#### 2. Global (Order Total) Discounts
- Apply discount as a separate line at the end of the order
- Single discount line with negative amount
- Automatically calculated from order subtotal
- Clean presentation for customers

## Installation

1. Copy the module folder to your Odoo addons directory
2. Update the apps list in Odoo
3. Search for "Sale Order Global Discount"
4. Click Install

## Usage

### Creating Global Discounts

1. Navigate to **Sales → Configuration → Sales Orders → Global Discounts**
2. Click **New**
3. Fill in the discount details:
   - **Name**: e.g., "VIP Discount"
   - **Apply Discount**: Choose between:
     - **On Order Lines**: Applies to each line individually
     - **On Order Total**: Creates a single discount line
   - **Percent**: Enter discount percentage
     - Simple: "10" = 10% discount
     - Compound: "10+5" = 10% then 5% on remainder (14.5% total)
     - Multiple: "20+10+5" = sequential application
4. The "Total Percent" field shows the calculated combined discount
5. Save

### Assigning Discounts to Partners

1. Open a partner (contact/customer)
2. Go to **Sales & Purchase** tab
3. In the "Global Discounts" section, select one or more discounts
4. Save the partner

### Using Discounts in Sales Orders

#### Method 1: Line-Level Discounts (Manual Entry)

1. Create a new sales order
2. Set **Discount Applies to**: **Order Line**
3. Add products to order lines
4. For each line, you can:
   - Choose **Discount Method**:
     - **Percentage**: Enter % (e.g., 10)
     - **Fixed**: Enter dollar amount (e.g., 162.00)
   - Enter **Discount Amount**
5. View **Line Discount Total** in the totals section

#### Method 2: Line-Level Discounts (Auto-fill from Templates)

1. Create a new sales order
2. Select a partner with assigned discounts (or select discounts manually)
3. Set **Discount Applies to**: **Order Line**
4. Add products - discounts auto-populate with percentage from templates
5. You can still manually adjust discount method and amount per line

#### Method 3: Global Discount (Order Total)

1. Create a new sales order
2. Set **Discount Applies to**: **Global**
3. Select global discounts (with "On Order Total" type)
4. Add products
5. A separate "Global Discount" line appears at the end with negative amount

### Using Discounts in Invoices

Discounts work the same way in customer invoices:
1. Create a customer invoice
2. Select a partner (discounts auto-populate) or select manually
3. Choose discount application method (Line or Global)
4. Add products - discounts apply based on settings

### Viewing Discount Information

- **Sale Order Form**: 
  - "Discount Applies to" toggle
  - Discount columns on lines (when in line mode)
  - Line Discount Total in totals section
  - Or separate discount line (when in global mode)
- **Invoice Form**: Same features as sale orders
- **Printed Reports**: Includes discount breakdown
- **Customer Portal**: Customers can see applied discounts on quotations and invoices

## Technical Details

### Models

- `res.partner.global_discount`: Master discount definitions
  - Fields: name, percent, total_percent, discount_type (line/order)
- `res.partner`: Extended with global_discount_ids
- `sale.order`: Extended with discount tracking and computed fields
  - New fields: discount_applies_to, line_discount_total
- `sale.order.line`: Line-level discount support
  - New fields: discount_method (percentage/fixed), discount_amount_value
- `account.move`: Extended with discount support for customer invoices
- `account.move.line`: Auto-applies discounts on product selection

### Discount Calculation

#### Compound Discounts
Calculated using the formula:
```
Total = 1 - (1 - d1) × (1 - d2) × ... × (1 - dn)
```

Example: "10+5" = 1 - (1 - 0.10) × (1 - 0.05) = 0.145 (14.5%)

#### Line-Level Discounts

**Percentage Method:**
- Discount Amount Value = percentage (e.g., 10 for 10%)
- Applied directly to `discount` field

**Fixed Method:**
- Discount Amount Value = fixed amount in currency
- Converted to percentage: `(fixed_amount / price_unit) × 100`
- Applied to `discount` field

**Line Discount Total:**
```
For each line: (price_unit × quantity) × (discount% / 100)
Total = Sum of all line discounts
```

#### Order-Level Discounts
```
Subtotal = Sum of regular lines (excluding discount line)
Discount Amount = -(Subtotal × total_discount_percent / 100)
Created as separate line with negative price_unit
```

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

### Version 18.0.2.0.0 (Current)
- **NEW**: Line-level discount method (Percentage or Fixed Amount)
- **NEW**: "Discount Applies to" toggle (Order Line vs Global)
- **NEW**: Manual discount entry on order lines
- **NEW**: Line Discount Total displayed in totals section
- **NEW**: Auto-fill from global discount templates
- **IMPROVED**: Flexible discount application options
- **IMPROVED**: Better UI matching Odoo quotation templates
- Discount calculated before taxes (standard behavior)
- Version bump from 18.0.1.1.0 to 18.0.2.0.0

### Version 18.0.1.1.0
- Added discount_type field to global discounts (line/order)
- Order-type discounts applied as separate discount line
- Line-type discounts applied to each order line
- Auto-creates "Global Discount" product for order-level discounts

### Version 18.0.1.0.0
- Initial release for Odoo 18
- Global discount management
- Sale order and invoice integration
- Compound discount support
- Portal and report integration
- Security configuration

