# -*- coding: utf-8 -*-
# from odoo import http


# class PhoneMandatory(http.Controller):
#     @http.route('/phone_mandatory/phone_mandatory', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/phone_mandatory/phone_mandatory/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('phone_mandatory.listing', {
#             'root': '/phone_mandatory/phone_mandatory',
#             'objects': http.request.env['phone_mandatory.phone_mandatory'].search([]),
#         })

#     @http.route('/phone_mandatory/phone_mandatory/objects/<model("phone_mandatory.phone_mandatory"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('phone_mandatory.object', {
#             'object': obj
#         })
