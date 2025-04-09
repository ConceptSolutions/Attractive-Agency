# -*- coding: utf-8 -*-
# from odoo import http


# class SaleCustomize(http.Controller):
#     @http.route('/sale_customize/sale_customize', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_customize/sale_customize/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_customize.listing', {
#             'root': '/sale_customize/sale_customize',
#             'objects': http.request.env['sale_customize.sale_customize'].search([]),
#         })

#     @http.route('/sale_customize/sale_customize/objects/<model("sale_customize.sale_customize"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_customize.object', {
#             'object': obj
#         })
