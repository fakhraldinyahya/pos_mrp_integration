{
    'name': 'POS Manufacturing Integration',
    'version': '0.1',
    'category': 'Sales/Point of Sale',
    'summary': 'Automated Manufacturing Orders from Point of Sale',
    'author': 'Fakhraldin Al-Ahnumi',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
        'mrp',
    ],
    'data': [
        'views/product_templet_views.xml',
        'views/mrp_production_views.xml',
        'views/pos_order_views.xml',
    ],
    'description': """
POS Manufacturing Integration
=============================

Seamlessly integrate your Point of Sale operations with your Manufacturing line.

Key Features
------------
* **Automated Workflow**: Automatically generate Manufacturing Orders (MO) when specific products are sold in the POS.
* **Smart Configuration**: Easily flag products as "Manufacture from POS" directly in the product form.
* **Validation & Safety**:
    * Prevents selling manufactured products if no active Bill of Materials (BoM) exists.
    * Ensures data integrity by blocking invalid configurations.
* **Traceability**:
    * Comprehensive link between POS Orders and generated Manufacturing Orders.
    * View the source POS Order directly from the Manufacturing Order.
    * Track Manufacturing status directly from the POS Order backend view.

Business Value
--------------
Perfect for businesses that sell custom-made or made-to-order items directly to customers, such as:
* Custom Furniture Shops
* Bakeries & Food Service
* Assemble-on-Demand Electronics

Stocks are properly managed by reserving components immediately upon order confirmation.
    """,
    'installable': True,
    'application': False,
    'auto_install': False,
}
