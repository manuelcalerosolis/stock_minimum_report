# -*- coding: utf-8 -*-
from odoo import http

# class StockMiniumReport(http.Controller):
#     @http.route('/stock_minium_report/stock_minium_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_minium_report/stock_minium_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_minium_report.listing', {
#             'root': '/stock_minium_report/stock_minium_report',
#             'objects': http.request.env['stock_minium_report.stock_minium_report'].search([]),
#         })

#     @http.route('/stock_minium_report/stock_minium_report/objects/<model("stock_minium_report.stock_minium_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_minium_report.object', {
#             'object': obj
#         })