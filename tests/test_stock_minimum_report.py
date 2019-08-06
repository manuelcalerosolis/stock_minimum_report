# -*- coding: utf-8 -*-

# Copyright 2019 Manuel Calero
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
# docker-compose run web --test-enable --stop-after-init --addons-path /mnt/extra-addons -d test_db -i stock_minimum_report --test-tags=stock_minimum_report
#

from datetime import timedelta

from odoo.exceptions import UserError
from odoo.fields import Date, Datetime
from odoo.tests.common import TransactionCase, tagged


@tagged('-standard', 'stock_minimum_report')
class TestStockMinimumReport(TransactionCase):
    def setUp(self):
        super(TestStockMinimumReport, self).setUp()
        self.stock_location = self.env.ref('stock.stock_location_stock')
        self.customer_location = self.env.ref('stock.stock_location_customers')
        self.supplier_location = self.env.ref('stock.stock_location_suppliers')
        self.inventory_location = self.env.ref('stock.location_inventory')
        self.partner = self.env['res.partner'].create({'name': 'xxx'})
        self.owner1 = self.env['res.partner'].create({'name': 'owner1'})
        self.uom_unit = self.env.ref('uom.product_uom_unit')

        self.product_1 = self.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'default_code': 'prda',
            'categ_id': self.env.ref('product.product_category_all').id,
        })

        self.product_2 = self.env['product.product'].create({
            'name': 'Product B',
            'type': 'product',
            'default_code': 'prdb',
            'categ_id': self.env.ref('product.product_category_all').id,
        })

        self.warehouse_1 = self.env['stock.warehouse'].create({
            'name': 'Warehouse A',
            'code': 'wha'
        })

        self.move_1 = self.env['stock.move'].create({
            'name': 'test_in_1',
            'location_id': self.supplier_location.id,
            'location_dest_id': self.stock_location.id,
            'product_id': self.product_1.id,
            'product_uom': self.uom_unit.id,
            'product_uom_qty': 100.0,
        })

        # confirmation
        self.move_1._action_confirm()

        # assignment
        self.move_1._action_assign()

        # fill the move line
        move_line = self.move_1.move_line_ids[0]
        move_line.qty_done = 100.0

        # validation
        self.move_1._action_done()

        # minimum stock rule for test product on this warehouse
        self.env['stock.warehouse.orderpoint'].create({
            'warehouse_id': self.warehouse_1.id,
            'location_id': self.warehouse_1.lot_stock_id.id,
            'product_id': self.product_1.id,
            'product_min_qty': 10,
            'product_max_qty': 100,
            'product_uom': self.uom_unit.id,
        })

    def test_product_created(self):
        """ This method test that product A and B was created.
        """

        self.assertEqual(self.product_1.name, 'Product A')
        self.assertEqual(self.product_2.name, 'Product B')
        self.assertEqual(self.warehouse_1.name, 'Warehouse A')
        self.assertEqual(self.move_1.state, 'done')
        self.assertEqual(len(self.move_1.move_line_ids), 1)
