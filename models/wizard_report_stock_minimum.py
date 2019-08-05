# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################

import logging

from odoo import models, fields, api,_


class WizardReportStockMinimum(models.TransientModel):
    _name = "wizard.report.stock.minimum"
    _description = "Products Report Under Minimum"

    warehouse_option = fields.Selection([
        ('1', 'All warehouses'),
        ('2', 'Specific warehouse')
    ], 'Show: ', default='1', required=True)

    warehouse_selected = fields.Many2one('stock.warehouse', 'Warehouse')

    def _get_domain(self):
        domain = [('under_minimum', '=', True)]
        if self.warehouse_selected.id:
            domain.append(('warehouse_id', '=', self.warehouse_selected.id))
        return domain

    def run_wizard(self):
        self.ensure_one()

        tree_view_id = self.env.ref('stock_minimum_report.view_minimum_warehouse_orderpoint_tree').id
        # We pass `warehouse_selected` in the context so that `qty_available` will be computed across

        action = {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree')],
            'view_mode': 'tree',
            'name': _('Products Report Under Minimum'),
            'res_model': 'stock.warehouse.orderpoint',
            'domain': self._get_domain(),
        }

        return action
