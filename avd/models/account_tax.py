from odoo import models, fields

class AccountTax(models.Model):
    _inherit='account.tax'

    service_tax = fields.Boolean('Service Tax', default=False)