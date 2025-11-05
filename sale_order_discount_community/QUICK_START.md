# Quick Start Guide - Community Edition

## Installation (2 steps)

1. **Add to your Odoo config** (if not already in addons_path):
   ```
   addons_path = /home/sabry3/edu_demo/custom_addons,...
   ```

2. **Install via Odoo UI**:
   - Apps → Update Apps List
   - Search "Sale Order Discount (Community)"
   - Click Install

## Usage

### Quick Option 1: Line-Level Discounts (Manual)

```
Sales → New Quotation
├─ Discount Applies to: Order Line
├─ Add Product
├─ Discount Method: Choose Percentage or Fixed
├─ Discount Amount: Enter 10 (for 10%) or 162.00 (for $162)
└─ Line Discount Total: Shows at bottom
```

### Quick Option 2: Line-Level Discounts (Template-Based)

**Step 1: Create Global Discount**
```
Sales → Configuration → Sales Orders → Global Discounts → Create
├─ Name: VIP Discount
├─ Apply Discount: On Order Lines
├─ Percent: 10+5
└─ Total Percent: 14.5% (auto-calculated)
```

**Step 2: Assign to Customer**
```
Contacts → Select Customer → Sales & Purchase tab
└─ Global Discounts: Select "VIP Discount"
```

**Step 3: Use in Quotation**
```
Sales → New Quotation
├─ Customer: Select customer from Step 2
├─ Discount Applies to: Order Line
├─ Global Discounts: Auto-populated!
└─ Add Products: 14.5% discount auto-fills (can manually adjust)
```

### Quick Option 3: Global Discount on Order Total

```
Sales → New Quotation
├─ Discount Applies to: Global
├─ Select global discount (with "On Order Total" type)
├─ Add Products
└─ Separate "Global Discount" line appears with negative amount
```

## Discount Format Examples

| Input    | Meaning                                  | Result  |
|----------|------------------------------------------|---------|
| `10`     | 10% off                                  | 10.0%   |
| `10+5`   | 10% off, then 5% off the remainder       | 14.5%   |
| `20+10`  | 20% off, then 10% off the remainder      | 28.0%   |
| `15+10+5`| Sequential: 15%, then 10%, then 5% off   | 27.325% |

## Key Features

✅ **Flexible Application**: Choose between line-level or order-level discounts
✅ **Multiple Methods**: Percentage (10%) or Fixed Amount ($162.00)
✅ **Manual & Auto**: Manual entry or auto-fill from templates
✅ **Compound Discounts**: Chain multiple discounts (e.g., "10+5" = 14.5%)
✅ **Line Discount Total**: See total discount amount in order summary
✅ **Works On**: Sales Orders, Quotations (Community Edition)
✅ **Reports**: Shows in printed PDF quotations
✅ **Portal**: Customers see discounts in their portal
✅ **Security**: Read-only for users, full access for sales managers

## Where to Find Things

- **Manage Discounts**: Sales → Configuration → Sales Orders → Global Discounts
- **Assign to Partners**: Contacts → Customer → Sales & Purchase tab
- **Discount Toggle**: "Discount Applies to" field on quotation/order
- **Line Discount Fields**: Discount Method and Discount Amount columns
- **Line Discount Total**: In totals section (when using line mode)

## Troubleshooting

**Discount not applying?**
- Check that global_discount_ids is filled on the order
- Make sure you add products AFTER selecting discounts
- Verify the discount has a valid percent value

**Can't edit discount on confirmed order?**
- This is by design - discounts are readonly after confirmation
- Create a new order or cancel and modify

**Don't see the menu?**
- Check you have Sales Manager access rights
- Try refreshing your browser (Ctrl+F5)

## Community vs Enterprise

This Community Edition does NOT include:
- ❌ Customer invoice discount support
- ❌ Invoice portal templates

If you need invoice support, use the full `sale_order_global_discount` module with Odoo Enterprise.

## Need Help?

See `README.md` for complete documentation or `INSTALLATION.md` for detailed setup.

