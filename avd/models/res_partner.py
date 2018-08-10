import string

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fax_no = fields.Char('Fax No.', size=20)
    province_id = fields.Many2one('province', string='Province', placeholder='Province')
    canton_id = fields.Many2one('canton', string='Canton', placeholder='Canton',domain="[('province_id','=',province_id)]")
    district_id = fields.Many2one('district', string='District', placeholder='District',domain="[('canton_id','=',canton_id)]")
    locality_id = fields.Many2one('locality', string='Locality', placeholder='Locality',domain="[('district_id','=',district_id)]")
    phone = fields.Char('Phone', size=20)

    @api.onchange('name')
    def onchange_name(self):
        all_normal_characters = string.ascii_letters
        for char in self.name:
            if char not in all_normal_characters:
                name = self.name
                self.name = name.replace(char,'')