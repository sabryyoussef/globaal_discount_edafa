# Quick Start Guide

## Installation (2 steps)

1. **Add to your Odoo config** (if not already in addons_path):
   ```
   addons_path = /home/sabry3/global_disc_modules,...
   ```

2. **Install via Odoo UI**:
   - Apps → Update Apps List
   - Search "Sale Order Global Discount"
   - Click Install

## Usage (3 steps)

### Step 1: Create a Global Discount
```
Sales → Configuration → Global Discounts → Create
├─ Name: VIP Customer Discount
├─ Percent: 10+5
└─ Total Percent: 14.5% (auto-calculated)
```

### Step 2: Assign to a Customer
```
Contacts → Select Customer → Sales & Purchase tab
└─ Global Discounts: Select "VIP Customer Discount"
```

### Step 3: Use in Sales Orders
```
Sales → New Quotation
├─ Customer: Select customer from Step 2
├─ Global Discounts: Auto-populated!
└─ Add Products: Discount applied automatically (14.5%)
```

## Discount Format Examples

| Input    | Meaning                                  | Result  |
|----------|------------------------------------------|---------|
| `10`     | 10% off                                  | 10.0%   |
| `10+5`   | 10% off, then 5% off the remainder       | 14.5%   |
| `20+10`  | 20% off, then 10% off the remainder      | 28.0%   |
| `15+10+5`| Sequential: 15%, then 10%, then 5% off   | 27.325% |

## Key Features

✅ **Auto-Application**: Discounts apply automatically when adding products
✅ **Compound Discounts**: Chain multiple discounts (e.g., "10+5")
✅ **Works On**: Sales Orders, Quotations, Customer Invoices
✅ **Reports**: Shows in printed PDF quotations/invoices
✅ **Portal**: Customers see discounts in their portal
✅ **Security**: Read-only for users, full access for sales managers

## Where to Find Things

- **Manage Discounts**: Sales → Configuration → Global Discounts
- **Assign to Partners**: Contacts → Customer → Sales & Purchase tab
- **View in Sales**: Any quotation/order shows discount field below payment terms
- **View in Invoices**: Any customer invoice shows discount field

## Troubleshooting

**Discount not applying?**
- Check that global_discount_ids is filled on the order
- Make sure you add products AFTER selecting discounts
- Verify the discount has a valid percent value

**Can't edit discount on confirmed order?**
- This is by design - discounts are readonly after confirmation
- Create a new order or cancel and modify

**Don't see the menu?**
- Check you have Sales/User access rights
- Try refreshing your browser (Ctrl+F5)

## Need Help?

See `README.md` for complete documentation or `INSTALLATION.md` for detailed setup.

