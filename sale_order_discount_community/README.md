# Sale Order Discount (Community Edition)

## Overview

This Odoo 18 Community Edition module adds flexible discount functionality to sales orders and quotations. Discounts can be applied either per line or globally on the entire order, with support for both percentage and fixed amount discounts.

**Note**: This is the Community Edition version that works without the Accounting module. For the full version with invoice support, see `sale_order_global_discount`.

## Features

### Core Features
- **Global Discount Management**: Create and manage reusable discount schemes
- **Compound Discounts**: Support for sequential discounts (e.g., "10+5" = 14.5% total)
- **Partner Integration**: Assign default discounts to partners
- **Flexible Discount Application**: Choose between line-level or order-level discounts
- **Multiple Discount Methods**: Support for both percentage and fixed amount discounts
- **Manual & Automatic**: Manual entry or auto-fill from global discount templates
- **Sales Orders & Quotations**: Full integration with sale orders and quotations
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
3. Search for "Sale Order Discount (Community)"
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

### Viewing Discount Information

- **Sale Order Form**: 
  - "Discount Applies to" toggle
  - Discount columns on lines (when in line mode)
  - Line Discount Total in totals section
  - Or separate discount line (when in global mode)
- **Printed Reports**: Includes discount breakdown
- **Customer Portal**: Customers can see applied discounts on quotations

## Technical Details

### Models

- `res.partner.global_discount`: Master discount definitions
  - Fields: name, percent, total_percent, discount_type (line/order)
- `res.partner`: Extended with global_discount_ids
- `sale.order`: Extended with discount tracking and computed fields
  - New fields: discount_applies_to, line_discount_total
- `sale.order.line`: Line-level discount support
  - New fields: discount_method (percentage/fixed), discount_amount_value

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
- Modern widget options and field attributes

## Dependencies

- `sale`: Sales Management (Odoo Community Edition)
- `contacts`: Contact Management

**Note**: This module does NOT require the Accounting module, making it suitable for Odoo Community Edition installations.

## Comparison with Enterprise Version

| Feature | Community Edition | Enterprise Edition |
|---------|------------------|-------------------|
| Sale Orders | ✅ | ✅ |
| Quotations | ✅ | ✅ |
| Customer Invoices | ❌ | ✅ |
| Line Discounts | ✅ | ✅ |
| Order Discounts | ✅ | ✅ |
| Portal Integration | ✅ (Sales only) | ✅ (Sales + Invoices) |
| Reports | ✅ (Sales only) | ✅ (Sales + Invoices) |

## License

LGPL-3

## Support

For issues, questions, or contributions, please contact your Odoo implementation partner.

## Changelog

### Version 18.0.1.0.0 (Current)
- Initial Community Edition release
- Based on Enterprise version 18.0.2.0.0
- Removed accounting module dependencies
- Sale order and quotation support only
- Line-level discount method (Percentage or Fixed Amount)
- "Discount Applies to" toggle (Order Line vs Global)
- Manual discount entry and template-based auto-fill
- Line Discount Total display
- Portal and report integration for sales orders

