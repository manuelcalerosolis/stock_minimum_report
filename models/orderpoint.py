# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Orderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_available = fields.Float(related='product_id.qty_available')

    under_minimum = fields.Boolean(compute='_compute_under_minimum', string='Under Minimum', store=True,
                                   help='This value is true if quantity available is under minimum quantity.')

    warehouse_name = fields.Char(related='warehouse_id.name')

    @api.one
    def _compute_under_minimum(self):
        self.under_minimum = (self.qty_available - self.product_min_qty) < 0
