# pos-mrp-integration
Odoo POS to Manufacturing Order integration
## Overview

This module integrates **Point of Sale (POS)** with **Manufacturing (MRP)** by automatically creating Manufacturing Orders when specific products are sold through POS.

It is designed to support **Make-to-Order workflows from POS**, while fully relying on Odoo standard MRP, stock, and costing mechanisms.  
The implementation ensures correct inventory movements, accurate manufacturing cost calculation, and full traceability between POS Orders and Manufacturing Orders.

---

## Integration Flow

### 1. Configuration & Setup

Products intended to be manufactured from POS must be configured with:

- **Manufacturing from POS**: A boolean flag on the Product Template (`mrp_from_pos`)
- **Bill of Materials (BoM)**: A valid **Normal** BoM ("Manufacture this product")

Configuration rules:
- Kits (phantom BoMs) are not supported
- Products without a valid BoM cannot enable manufacturing from POS

---

### 2. POS Order Validation (Backend)

Before a POS Order is finalized:

- All POS order lines are inspected
- Products marked with **Manufacturing from POS** are collected
- A valid BoM is searched based on:
  - Company
  - Warehouse manufacturing operation type
- If any required BoM is missing, POS Order validation is blocked with an error

This guarantees that no Manufacturing Order is created without a valid BoM.

---

### 3. Order Processing (Backend Execution)

When a POS Order is paid and processed:

- Refund POS Orders are ignored
- Each order line is evaluated independently
- For each product marked for POS manufacturing:
  - One **Manufacturing Order (MO)** is created

Each MO is linked directly to the originating POS Order.

---

### 4. Manufacturing Workflow

The generated Manufacturing Orders follow this automated lifecycle:

1. **Creation & Confirmation**  
   - The MO is created with the correct product, quantity, BoM, and operation type
   - The MO is immediately confirmed to reserve components

2. **Availability Check**  
   - Component availability is evaluated by Odoo standard logic

3. **Auto-Completion**  
   - If components are available:
     - The MO is automatically marked as **Done**
     - Raw materials stock is consumed
     - Finished goods stock is increased

4. **Exception Handling**  
   - If components are unavailable:
     - The MO remains in **Confirmed** state
     - No forced negative stock is introduced

---

## Key Design Decisions

### Backend-Only Validation

All validations are implemented at the backend level to:
- Guarantee data integrity
- Prevent invalid manufacturing scenarios
- Ensure consistency across POS sessions

---

### Atomic Manufacturing (One-to-One)

The module creates **one Manufacturing Order per POS Order Line**.

**Reasoning:**
- Accurate cost tracking per sold unit
- Clear traceability
- Flexibility for future customizations

---

### Best-Effort Automation

The system attempts to complete manufacturing immediately when stock allows:
- Manufacturing is auto-completed if components are available
- Inventory constraints are respected
- Manufacturing halts safely at **Confirmed** when stock is insufficient

---

## Assumptions & Limitations

1. **Product Type**  
   Products must be **stockable** to participate in manufacturing.  
   Service products are ignored.

2. **BoM Type**  
   Only **Normal BoMs** are supported.  
   Kits (phantom BoMs) are excluded.

3. **Manufacturing Configuration**  
   A Manufacturing Operation Type must be configured on the warehouse.

4. **Stock Availability**  
   Auto-completion depends on accurate stock quantities and reservation rules.

---

## Result

This module provides a reliable and Odoo-standard-compliant integration between POS and Manufacturing, delivering:

- Correct stock behavior
- Accurate manufacturing costs
- Full POS ↔ MRP traceability
- Minimal manual intervention
