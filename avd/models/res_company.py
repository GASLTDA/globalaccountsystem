from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    province_id = fields.Many2one('province', string='Province', placeholder='Province')
    canton_id = fields.Many2one('canton', string='Canton', placeholder='Canton',domain="[('province_id','=',province_id)]")
    district_id = fields.Many2one('district', string='District', placeholder='District',domain="[('canton_id','=',canton_id)]")
    locality_id = fields.Many2one('locality', string='Locality', placeholder='Locality',domain="[('district_id','=',district_id)]")
    fax_no = fields.Char('Fax No.', size=20)
    registration_date = fields.Datetime('Registration')
    phone = fields.Char('Phone', size=20, required=True)
    vat = fields.Char(size=13)
    store_branch = fields.Char('Store/Branch No.', size=3)


    url = fields.Char()
    username = fields.Char()
    password = fields.Char()