from odoo import models, _, api, fields
from odoo.exceptions import ValidationError, UserError


class PosOrder(models.Model):
    _inherit = "pos.order"

    mrp_production_ids = fields.One2many(
        'mrp.production', 'pos_order_id', string='Manufacturing Orders', readonly=True,
        help="List of Manufacturing Orders created from this POS Order."
    )
    mrp_production_count = fields.Integer(
        string='Manufacturing Orders Count', 
        compute='_compute_mrp_production_count',
        help="Count of related Manufacturing Orders."
    )

    @api.depends('mrp_production_ids')
    def _compute_mrp_production_count(self):
        """ Compute the number of manufacturing orders associated with this POS order. """
        for order in self:
            order.mrp_production_count = len(order.mrp_production_ids)

    @api.constrains('lines')
    def _check_mrp_product_bom(self):
        """
        Constraint to ensure that all products configured to be manufactured
        have a valid Bill of Materials (BoM) available.
        """
        for order in self:
            # 1. Identify products that require manufacturing
            mrp_products = order.lines.mapped('product_id').filtered('mrp_from_pos')
            
            if not mrp_products:
                continue

            # 2. Batch search for active BoMs for these products under the current company
            picking_type = order.picking_type_id.warehouse_id.manu_type_id
            boms_by_product = self.env['mrp.bom']._bom_find(mrp_products, company_id=order.company_id.id, picking_type=picking_type, bom_type='normal')

            # 3. Validation: Ensure every manufacturing product has a found BoM
            for product in mrp_products:
                if not boms_by_product.get(product):
                    raise ValidationError(_(
                        "Cannot validate POS Order %s.\n"
                        "Product '%s' is set to manufacture but has no active Bill of Materials."
                    ) % (order.name, product.display_name))

    @api.model
    def _process_order(self, order, existing_order):
        """
        Override standard POS order processing to trigger Manufacturing Order creation.
        
        Args:
            order (dict): The order data from the POS UI.
            existing_order (object): The existing order object if it exists.
            
        Returns:
            int: The ID of the processed POS order.
        """
        order_id = super(PosOrder, self)._process_order(order, existing_order)
        pos_order = self.browse(order_id)
        # Trigger MO creation if the order is confirmed (not draft or cancelled)
        if pos_order.state not in ['draft', 'cancel']:
            pos_order._create_mrp_from_pos()

        return order_id

    def _create_mrp_from_pos(self):
        """
        Generates Manufacturing Orders (MO) for POS order lines that contain 
        products marked as 'mrp_from_pos'.
        
        Logic:
        1. Iterates through order lines.
        2. Checks if product needs manufacturing.
        3. Finds the appropriate Bill of Materials (BoM).
        4. Identifies the correct Picking Type (Operation Type) from the warehouse.
        5. Creates, Confirms, and Marks the MO as Done immediately.
        """
        MrpProduction = self.env['mrp.production']
        MrpBom = self.env['mrp.bom']

        for order in self:
            # Skip refunds/returns as they shouldn't trigger new manufacturing
            if order.is_refund:
                continue
                
            for line in order.lines:
                product = line.product_id

                # Skip products that don't need manufacturing
                if not product.mrp_from_pos:
                    continue

                company = order.company_id

                # Determine the Manufacturing Operation Type from the warehouse config
                picking_type = order.picking_type_id.warehouse_id.manu_type_id
                if not picking_type:
                    raise UserError(_("No Manufacturing Operation Type configured for warehouse '%s'.") % order.picking_type_id.warehouse_id.name)
                
                # Find the most suitable BoM for this product/variant in this company
                boms = MrpBom._bom_find(product, company_id=company.id, picking_type=picking_type, bom_type='normal')
                bom = boms.get(product)

                # Critical check: BoM must exist
                if not bom:
                    raise UserError(_(
                        "No valid Bill of Materials found for product '%s'. "
                        "Please check the Manufacturing configuration."
                    ) % product.display_name)


                # Prepare MO values
                # We use specific source/dest locations from the operation type
                mo_vals = {
                    'product_id': product.id,
                    'product_qty': line.qty,
                    'product_uom_id': product.uom_id.id,
                    'bom_id': bom.id,
                    'pos_order_id': order.id,         # Link to POS Order
                    'company_id': company.id,
                    'origin': order.name,             # Source Document Reference
                    'picking_type_id': picking_type.id,
                    'location_src_id': picking_type.default_location_src_id.id,
                    'location_dest_id': picking_type.default_location_dest_id.id,
                }

                # Create the Manufacturing Order
                mo = MrpProduction.with_company(company).create(mo_vals)
                
                # Auto-Process the Lifecycle
                mo.action_confirm()      # Reserves components
                mo.button_mark_done()    # Completes production and moves stock

    def action_view_mrp_orders(self):
        """
        Smart Button Action: Opens the Manufacturing Orders related to this POS Order.
        - If 1 MO: Opens form view.
        - If >1 MO: Opens list view.
        
        Returns:
            dict: The action dictionary to open the view.
        """
        self.ensure_one()
        mrp_orders = self.mrp_production_ids
        domain = [('id', 'in', mrp_orders.ids)]

        # Base action definition
        action = {
            'name': _('Manufacturing Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'domain': domain,
            'context': {'create': False}, # Disable manual creation from this view
        }

        # Dynamic view mode based on count
        if len(mrp_orders) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': mrp_orders.id,
            })
        else:
            action.update({
                'view_mode': 'list,form',
            })

        return action