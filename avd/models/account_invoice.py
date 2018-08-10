import datetime
import logging
import string

import requests
import xmltodict

from odoo import models, fields, api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    type_receiptor = fields.Selection([
        ('01', 'Electronic Taxpayer Receiver'),
        ('02', 'Taxpayer Non-electronic Receiver'),
        ('03', 'General Audience (POS / Electronic Ticket)'),
        ('04', 'Alien'),
        ('05', 'Other'),
    ], default='01', string='Type of Receiptor')

    def _show_button(self):
        if self.type in ('in_refund', 'out_invoice', 'out_refund'):
            if self.state == 'open' and self.success == False:
                self.show_button = True
            else:
                self.show_button = False
        else:
            self.show_button = False

    folio = fields.Char('Folio', copy=False)
    clave_numerica = fields.Char('Clave Numerica', copy=False)
    date = fields.Char('Date', copy=False)
    response = fields.Text(copy=False)
    success = fields.Boolean(default=False)
    show_button = fields.Boolean(compute='_show_button')

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()
        self.generate_file()
        return res

    @api.multi
    def generate_file(self):

        if not self.company_id.url or not self.company_id.username or not self.company_id.password:
            raise UserError("Please check AVD configuration")
        hat = '~'
        pipe = '|'
        carriage_return = '\n'
        txt = ''

        invoice_total = len(self)
        invoice_counter = 0
        id = self

        if id.type not in ('in_refund', 'out_invoice', 'out_refund'):
            return

        if id.number and len(id.number) <= 20 and id.number.isdigit():
            txt += hat
            txt += '[Folio]'

            # Isser Name
            txt += pipe
            txt += self._get_issuer_name(id)

            # Issuer Number
            txt += pipe
            txt += self._get_company_registry_no(id)

            # Issuer Street or avenue
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).street)

            # Issuer Exterior No.
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).street2)

            # Issuer Interior No.
            txt += pipe

            # Issuer District
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).district_id)

            # Issuer Locality
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).locality_id)

            # Issuer Full Address
            txt += pipe
            txt += self._get_full_address(self._get_doc_type(id))

            # Issuer Canton
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).canton_id)

            # Issuer Province
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).province_id)

            # Issuer Country
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).country_id)

            # Issuer Zip
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).zip)

            # Issuer Phone/Mobile
            txt += pipe
            txt += self._get_phone(self._get_doc_type(id))

            # Issuer Branch Street or avenue
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).street)

            # Issuer Branch Exterior No.
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).street2)

            # Issuer Branch Interior No.
            txt += pipe

            # Issue Branch District
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).district_id)

            # Issuer Branch Locality
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).locality_id)

            # Issuer Branch Full Address
            txt += pipe
            txt += self._get_full_address(self._get_doc_type(id))

            # Issuer Branch Canton
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).canton_id)

            # Issuer Branch Province
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).province_id)

            # Issuer Branch Country
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).country_id)

            # Issuer Branch Zip
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).zip)

            # Issuer Branch Phone/Mobile
            txt += pipe
            txt += self._get_phone(self._get_doc_type(id))

            # Version
            txt += pipe
            txt += "4.2"

            # Blank
            txt += pipe

            # Issuer Vat No
            txt += pipe
            txt += self._get_vat_no(id)

            # Todo check footer note, have to add payment type
            # Payment Type
            txt += pipe

            # Issue Date
            txt += pipe
            time =  datetime.datetime.now() - datetime.timedelta(hours=6)
            txt += time.strftime('%Y-%m-%d')

            # Todo capure invoice time seperately
            # Broadcast time

            cn_time = time.strftime('%H:%M:%S')
            txt += pipe
            txt += cn_time

            # Place of issue Street or avenue
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).street)

            # Place of issue Exterior No.
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).street2)

            # Place of issue Interior No.
            txt += pipe

            # Place of issue District
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).district_id)

            # Place of issue Locality
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).locality_id)

            # Place of issue Full Address
            txt += pipe
            txt += self._get_full_address(self._get_doc_type(id))

            # Place of issue Canton
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).canton_id)

            # Place of issue Province
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).province_id)

            # Place of issue Country
            txt += pipe
            txt += self._get_code(self._get_doc_type(id).country_id)

            # Place of issue Zip
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).zip)

            # Receiver Name
            txt += pipe
            txt += self._get_name(self._get_doc_type(id, True))

            # Receiver Id/Ref
            txt += pipe
            txt += self._get_string(self._get_doc_type(id, True).ref)

            # Receiver Street or avenue
            txt += pipe
            txt += self._get_string(self._get_doc_type(id, True).street)

            # Receiver Exterior No.
            txt += pipe
            txt += self._get_string(self._get_doc_type(id, True).street2)

            # Receiver Interior No.
            txt += pipe

            # Receiver District
            txt += pipe
            txt += self._get_code(self._get_doc_type(id, True).district_id)

            # Receiver Locality
            txt += pipe
            txt += self._get_code(self._get_doc_type(id, True).locality_id)

            # Receiver Full Address
            txt += pipe
            txt += self._get_full_address(self._get_doc_type(id, True))

            # Receiver Canton
            txt += pipe
            txt += self._get_code(self._get_doc_type(id, True).canton_id)

            # Receiver Province
            txt += pipe
            txt += self._get_code(self._get_doc_type(id, True).province_id)

            # Receiver Country
            txt += pipe
            txt += self._get_code(self._get_doc_type(id, True).country_id)

            # Receiver Zip
            txt += pipe
            txt += self._get_string(self._get_doc_type(id, True).zip)

            # Untaxed Amount
            txt += pipe
            untaxed_amount = 0.0
            for line in id.invoice_line_ids:
                untaxed_amount = line.quantity * line.price_unit
            txt += str(untaxed_amount)

            # Total Tax Amount
            txt += pipe
            sales_tax_amount = 0.0
            for taxes in id.tax_line_ids:
                tax_id = self.env['account.tax'].search([('name', '=', taxes.name)])
                if tax_id:
                    if tax_id.service_tax == False:
                        sales_tax_amount += taxes.amount_total
            txt += str(sales_tax_amount)

            # Total Amount
            txt += pipe
            txt += str(id.amount_total)

            # Todo get input from Henry
            # State
            txt += pipe
            txt += self._state(id)

            # Todo get input from Henry for doc type
            # Doc Type
            txt += pipe
            txt += self._doc_type(id)

            # Notes
            txt += pipe

            # Notes 2
            txt += pipe

            # Notes 3
            txt += pipe

            # Supplier code
            txt += pipe

            try:
                ref = self._get_doc_type(id).ref
            except:
                ref = self._get_doc_type(id).partner_id.ref

            txt += self._get_string(ref)

            # Supplier rating
            txt += pipe

            # EAN code provider
            txt += pipe

            # Bill number
            txt += pipe
            if id.type == 'out_refund' or id.type == 'in_refund':
                txt += self._get_string(id.origin)

            # Purchase Order number
            txt += pipe
            if id.type == 'in_invoice':
                txt += self._get_string(id.origin)

            txt += pipe

            # Purchase Order Date
            if id.type == 'in_invoice':
                order = self._get_string(id.origin)
                if len(order) > 0:
                    order_id = self.env['purchase.order'].sudo().search([('name', '=', order)])
                    if order_id:
                        txt += time.strftime('%Y-%m-%d', order_id.date_order)

            # Provider Number
            txt += pipe

            # EAN shop or place of delivery
            txt += pipe

            # Store'branch. Necessary to generate the tax row.
            txt += pipe
            txt += str(id.company_id.store_branch)

            # Store name or place of delivery
            txt += pipe
            txt += self._get_string(id.partner_shipping_id.name)

            txt += pipe
            txt += self._get_string(id.partner_shipping_id.street)

            # Store name or place of delivery Exterior No.
            txt += pipe
            txt += self._get_string(id.partner_shipping_id.street2)

            # Store name or place of delivery Interior No.
            txt += pipe

            # Store name or place of delivery District
            txt += pipe
            txt += self._get_string(id.partner_shipping_id.district_id.name)

            # Store name or place of delivery Locality
            txt += pipe
            txt += self._get_string(id.partner_shipping_id.locality_id.name)

            # Store name or place of delivery Full Address
            txt += pipe
            # txt += self._get_full_address(self._get_doc_type(id, True))

            # Store name or place of delivery Canton
            txt += pipe
            txt += self._get_string(id.partner_shipping_id.canton_id.name)

            # Store name or place of delivery Province
            txt += pipe
            txt += self._get_string(id.partner_shipping_id.province_id.name)

            # Store name or place of delivery Country
            txt += pipe
            txt += self._get_string(id.partner_shipping_id.country_id.name)

            # Store name or place of delivery Zip
            txt += pipe
            txt += self._get_string(id.partner_shipping_id.zip)

            # Store ID
            txt += pipe
            txt += self._get_string(id.company_id.store_branch)

            # Currency
            txt += pipe
            if id.currency_id.name in ['CRC', 'USD', 'MXN', 'EUR', 'JPY', 'GBP']:
                txt += id.currency_id.name
            else:
                raise UserError('Currency not allowed')

            # Payment Term
            txt += pipe
            if id.payment_term_id:
                txt += self._get_string(id.payment_term_id.name[:10])

            # Porc. prompt payment discount
            txt += pipe

            # Prompt payment discount amount
            txt += pipe

            # Discount Code
            txt += pipe

            # General percentage discount
            txt += pipe

            # Total amount of discounts applicable before taxes.
            total_lines = 0
            line_total = 0.0
            txt += pipe
            for line in id.invoice_line_ids:
                total_lines += 1
                line_total_without_dis = line.quantity * line.price_unit
                line_total += (line_total_without_dis * (line.discount / 100))
            txt += str(line_total)

            # Number of lines of invoice detail
            txt += pipe
            txt += str(total_lines)

            # Due date of the invoice
            txt += pipe
            txt += self._get_string(id.date_due)

            # Area code
            txt += pipe

            # No. Receptor (RI)
            txt += pipe

            # Vendor code
            txt += pipe

            # Seller Name
            txt += pipe

            # Way of shipment
            txt += pipe

            # It corresponds to the average paid employee: Cash 01 02 Card 03 check 04 Transfer - bank deposit, 05 - collected by third parties, 99 Others
            txt += pipe
            txt += '99'

            # Order Code
            txt += pipe

            # Order Date (yyyy-MM-dd)
            txt += pipe

            # Total amount in words
            txt += pipe

            # Number of units or parts
            txt += pipe

            # Number of packages or boxes
            txt += pipe

            # EAN receptor bill
            txt += pipe

            # EAN place of dispatch
            txt += pipe

            # Recipient's phone number (20 digits no dashes or spaces).
            txt += pipe
            txt += self._get_string(self._get_doc_type(id, True).phone)

            # trade name of the issuer
            txt += pipe
            txt += self._get_issuer_name(id)

            # Number of issuer (internal code)
            txt += pipe

            # the sum total of all taxes including the General Sales Tax and Selective Consumption Tax. Place a "0.00" (zero) if not applicable.
            txt += pipe
            txt += str(id.amount_tax)

            # subtotal amount applicable General Sales Tax
            txt += pipe
            sales_tax_amount = 0.0
            for taxes in id.tax_line_ids:
                tax_id = self.env['account.tax'].search([('name', '=', taxes.name)])
                if tax_id:
                    if tax_id.service_tax == False:
                        sales_tax_amount += taxes.amount_total

            txt += str(sales_tax_amount)

            # Carrier name or code.
            txt += pipe

            # Document application number (Ex. No. Appl. Note Credit or Charge).
            txt += pipe

            # Description of the currency (eg. "Colones")
            txt += pipe

            # misc
            misc = 1
            while (misc <= 41):
                if misc == 31:
                    txt += str(id.id)
                txt += pipe
                misc += 1

            # Type receptor.
            txt += pipe
            txt += id.type_receiptor

            # Fax number of the sender. 20 digits no dashes or spaces.
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).fax_no)

            # Email the issuer.
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).email)

            # Taxed electronic document for service lines amount. Place a "0.00" (zero) if not applicable.
            total_service = 0.0
            txt += pipe
            for line in id.invoice_line_ids:
                if line.product_id.type == 'service':
                    total_service += line.price_total - line.price_subtotal
            txt += str(total_service)

            # Amount exempt from electronic document for service lines. Place a "0.00" (zero) if not applicable.
            txt += pipe
            service_exempt = 0.0
            diff = 0.0
            for line in id.invoice_line_ids:
                if line.product_id.type == 'service':
                    diff = line.price_total - line.price_subtotal
                    if diff == 0.0:
                        service_exempt += line.price_total
            txt += str(service_exempt)

            # Taxed electronic document for lines of goods amount. Place a "0.00" (zero) if not applicable.
            total_goods = 0.0
            txt += pipe
            for line in id.invoice_line_ids:
                if line.product_id.type != 'service':
                    total_goods += line.price_total - line.price_subtotal
            txt += str(total_goods)

            # TotalMercanciasExentas {}Amount exempt from electronic document for freight lines. Place a "0.00" (zero) if not applicable.
            txt += pipe
            txt += str(0.0)

            # Date and time in which the DGT recorded the taxpayer and FE issuer under the "Registration Certificate Electronic Billing". (YyyymmddHHMMSS). Example: 20090109162000.
            txt += pipe
            registration_date = id.company_id.registration_date
            registration_date = registration_date.replace('-', '')
            registration_date = registration_date.replace(':', '')
            registration_date = registration_date.replace(' ', '')
            txt += registration_date

            # Text for clarification regarding the reason for the modification of the electronic document. Required only for credit notes or debit card. It is recommended to note the reference number of the electronic document. Maximum 180 characters.
            txt += pipe
            if id.type == 'in_refund' or id.type == 'out_refund':
                if id.name:
                    txt += id.name
                else:
                    txt += 'Refund'
            # if id.type == 'in_refund' or id.type == 'out_refund':

            # Sales tax rate applicable to the bill. Place a "0.00" (zero) if not applicable.
            total_taxes = 0.0
            txt += pipe
            for line in id.invoice_line_ids:
                if line.product_id.type != 'service':
                    total_taxes += line.price_total - line.price_subtotal
            txt += str(total_taxes)

            # Amount Selective Consumption Tax.Place a "0.00" (zero) if not applicable.
            txt += pipe
            txt += '0.0'

            # If the document corresponds to an electronic ticket (POS), the value must be "1" (one). If an electronic invoice must be "0" (zero).
            txt += pipe
            txt += '0'

            # The date and time that items were delivered
            txt += pipe

            txt += pipe

            if id.type == 'out_invoice':
                # txt += '01'
                txt += ''
            elif id.type == 'in_refund':
                txt += '03'
            elif id.type == 'out_refund':
                txt += '02'

            # Telephone number of foreign receiver (20 digits no dashes or spaces).
            txt += pipe

            # Folio number. Number issued by the buyer when you receive the merchandise is billed: AGAINST RECEIPT.
            txt += pipe

            # Date was assigned no. folio of receipt: Date of receipt of all orders to be invoiced. (Yyyy-MM-dd)
            txt += pipe

            # Contact purchases.
            txt += pipe

            # Global Location Number (GLN) of the Customs indicated.
            txt += pipe

            # ID No. pediment.
            txt += pipe

            # Custom Name.
            txt += pipe

            # City where the customs.
            txt += pipe

            # Email the issuer.
            txt += pipe
            txt += self._get_string(self._get_doc_type(id).email)

            # Exchange rate
            txt += pipe

            # Type emitter identification. See codes in Annex 3.
            txt += pipe
            txt += '02'

            # Receptor type identification. See codes in Annex 3
            txt += pipe
            txt += '02'

            # trade name of the recipient.
            txt += pipe
            txt += self._get_string(self._get_doc_type(id, True).name)

            # ALLOWANCE_GLOBAL / CHARGE_GLOBAL.
            txt += pipe

            # Status of the tax receipt.
            txt += pipe

            # Box number, or POS terminal. Data necessary for fiscal consecutive. Maximum 5 digits.Use "00001" when they apply.
            txt += pipe
            txt += '00002'

            # Discount rate being applied.
            txt += pipe
            txt += ''

            # Reference Document Date (YyyymmddHHMMSS). Generally the date of issuance of the document referenced credit note or debit reference. (Required only for credit and debit notes. It should not exist for other document types).
            txt += pipe
            if id.type == 'in_refund' or id.type == 'out_refund':
                ref_doc_date = id.date_invoice
                ref_doc_date = ref_doc_date.replace('-', '')
                txt += ref_doc_date + '000000'

            # Total amount of fees or discounts.
            txt += pipe
            dis_total = 0.0
            for line in id.invoice_line_ids:
                line_total_without_dis = line.quantity * line.price_unit
                dis_total += (line_total_without_dis * (line.discount / 100))
            txt += str(dis_total)

            # gross sale amount less applicable discounts.
            txt += pipe
            subtotal = 0.0
            for line in id.invoice_line_ids:
                subtotal += line.price_subtotal
            txt += str(subtotal)

            # Year of approval.
            txt += pipe

            # Reason for applicable discount
            txt += pipe

            # commercial conditions of sale electronic document
            txt += pipe
            txt += '99'

            # Code Reference (mandatory only for credit and debit notes. It should not exist for other document types). 01: Overrides reference document 02: Corrects reference document text.
            txt += pipe
            if id.type == 'out_refund':
                txt += '99'
            if id.type == 'in_refund':
                txt += '99'

            # Taxed electronic document for service lines and merchandise amount. Place a "0.00" (zero) if not applicable.
            total_service_merchandise = 0.0
            txt += pipe
            for line in id.invoice_line_ids:
                total_service_merchandise += line.price_total - line.price_subtotal
            txt += str(total_service_merchandise)

            # Amount exempt from electronic document for service lines and merchandise. Place a "0.00" (zero) if not applicable.
            txt += pipe
            total_service_merchandise_exempt = 0.0
            diff = 0.0
            for line in id.invoice_line_ids:
                diff = line.price_total - line.price_subtotal
                if diff == 0.0:
                    total_service_merchandise_exempt += line.price_total
            txt += str(total_service_merchandise_exempt)

            lines_count = len(id.invoice_line_ids)
            counter = 0
            ########LINES########
            for line in id.invoice_line_ids:
                txt += '\n'
                if counter == 0:
                    txt += '¬'
                sale_order_id = self.env['sale.order'].sudo().search([('name', '=', id.origin)])
                if len(line.name) > 160:
                    UserError(
                        'Description for product - ' + line.product_id.name + ' cannot be greater than 160 characters')

                # Description. Maximum 160 characters.
                txt += line.name
                txt += pipe

                # Quantity
                txt += str(line.quantity)
                txt += pipe

                # Unit of measurement.
                if sale_order_id:
                    sale_order_line_id = self.env['sale.order.line'].sudo().search(
                        [('order_id', '=', sale_order_id.id), ('product_id', '=', line.product_id.id)])
                    if sale_order_line_id:
                        try:
                            if sale_order_line_id.product_uom.code:
                                txt += sale_order_line_id.product_uom.code
                            else:
                                txt += 'Otros'
                        except:
                            txt += 'Otros'
                    else:
                        txt += 'Otros'
                else:
                    txt += 'Otros'
                txt += pipe

                # unit price of the item or service.
                txt += str(line.price_unit)
                txt += pipe

                # Total value of detail line
                txt += str(line.quantity * line.price_unit)
                txt += pipe

                # Customs document number
                txt += pipe

                # Custom document date (yyyy-MM- dd).
                txt += pipe

                # Custom Name
                txt += pipe

                # Property Tax Account Number
                txt += pipe

                # Fraction of the tariff code.
                txt += pipe

                # Product Reviews on
                txt += pipe

                # UPC code
                txt += pipe

                # Number of parts or units per box or packaging
                txt += pipe

                # DUN code
                txt += pipe

                # DUN code
                txt += pipe

                # Trade measure unit.
                if sale_order_id:
                    sale_order_line_id = self.env['sale.order.line'].sudo().search(
                        [('order_id', '=', sale_order_id.id), ('product_id', '=', line.product_id.id)])
                    if sale_order_line_id:
                        try:
                            if sale_order_line_id.product_uom.code:
                                txt += sale_order_line_id.product_uom.code
                            else:
                                txt += 'Otros'
                        except:
                            txt += 'Otros'
                    else:
                        txt += 'Otros'
                else:
                    txt += 'Otros'
                txt += pipe

                # Discount code applied to the line
                txt += pipe

                # Percentage Discount
                txt += str(line.discount)
                txt += pipe

                # Discount amount. Place a "0.00" (zero) if not applicable.
                line_total_without_dis = 0.0
                line_total_without_dis = line.quantity * line.price_unit
                txt += str(line_total_without_dis * (line.discount / 100))
                txt += pipe

                # Unit price without the discount applied.
                txt += str(line.price_unit)

                # Number of packages or boxes invoiced
                txt += pipe

                # Number of packages or shipped boxes
                txt += pipe

                # Rate of General Sales Tax applied to the line.
                txt += pipe
                for tax_ids in line.invoice_line_tax_ids:
                    if tax_ids:
                        txt += str(tax_ids.amount)

                # Amount of General Sales Tax applied to the line
                txt += pipe
                txt += str(line.price_total - line.price_subtotal)

                # Selective consumption tax rate applied to the line.
                txt += pipe
                txt += ''

                # Amount selective consumption tax applied to the line.
                txt += pipe
                txt += ''

                # Unit price with taxes (net price per package or box)
                txt += pipe
                txt += ''

                txt += pipe
                # Rode Total line with taxes (net total).
                txt += str(line.price_total)
                txt += pipe

                # Border
                txt += pipe

                # Country of origin
                txt += pipe

                # EAN code customs
                txt += pipe

                misc = 1

                while misc <= 61:
                    txt += pipe
                    misc = misc + 1

                # Total amount of the line
                txt += str(line.price_subtotal)
                txt += pipe

                txt += pipe
                txt += pipe
                txt += pipe
                txt += pipe
                txt += pipe

                counter = counter + 1

                if line.discount > 0.0:
                    txt += '\\'
                    txt += 'D'
                    txt += pipe

                    txt += '99'
                    txt += pipe

                    txt += str(line.discount)
                    txt += pipe

                    line_total_without_dis = 0.0
                    line_total_without_dis = line.quantity * line.price_unit
                    txt += str(line_total_without_dis * (line.discount / 100))
                    txt += pipe

                    txt += pipe
                    txt += pipe
                    txt += pipe
                    txt += pipe

                if line.invoice_line_tax_ids:
                    for tax_ids in line.invoice_line_tax_ids:
                        txt += '\\'
                        txt += 'I'
                        txt += pipe

                        if tax_ids.service_tax == True:
                            txt += '01'
                        else:
                            txt += '07'
                        txt += pipe

                        txt += str(tax_ids.amount)
                        txt += pipe

                        line_total_without_dis = 0.0
                        line_total_without_dis = line.quantity * line.price_unit
                        line_total_after_discount = line_total_without_dis - (
                            line_total_without_dis * (line.discount / 100))
                        txt += str(line_total_after_discount * (tax_ids.amount / 100))
                        txt += pipe

                        txt += pipe
                        txt += pipe
                        txt += pipe
                        txt += pipe

                        # txt += ';'
                        # txt += ';'
                        # txt += ';'
                        # txt += ';'
                        # txt += ';'
                        # txt += ';'
                        # txt += ';'
                        # txt += ';'
                        # txt += ';'

            if invoice_counter < (invoice_total - 1):
                txt += '\n'
        else:
            raise UserError('Required data is missing or empty. Please check whether the invoice is validated')

        invoice_counter += 1
        # current_time = time.strftime("%Y%m%d-%H%M%S")
        # file_name = 'avd_' + current_time + '.txt'
        print(txt)
        data = '<?xml version="1.0" encoding="utf-8"?>' + \
               '<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">' + \
               '<soap12:Body>' + \
               '<procesarTextoPlanoSinCtl xmlns="http://www.ekomercio.com/">' + \
               '<usuario>'+ id.company_id.username +'</usuario>' + \
               '<password>'+ id.company_id.password +'</password>' + \
               '<id>'+id.company_id.company_registry+'</id>' + \
               '<textoPlano>' + str(txt) + '</textoPlano>' + \
               '</procesarTextoPlanoSinCtl>' + \
               '</soap12:Body>' + \
               '</soap12:Envelope>'



        print(data)

        response = requests.post(id.company_id.url, data.encode(),
                                 headers={
                                     'Content-Type': 'application/soap+xml; charset=utf-8'
                                 })


        res = response.content.decode('UTF-8')
        print(res)
        import xml.etree.ElementTree as ET

        root = ET.fromstring(res)
        child = root[0][0][0]

        contenu = ET.tostring(child, encoding='UTF-8', method='xml').decode('UTF-8')
        response = (xmltodict.parse(contenu).get('ns0:procesarTextoPlanoSinCtlResult')['#text'])
        individual_data = (xmltodict.parse(response).get('Return'))
        success = False
        write_data = {
            'response': response
        }
        if individual_data:
            if 'ReturnFolio' in individual_data:
                success = True
                write_data.update({'success': success,
                                   'folio': individual_data['ReturnFolio'],
                                   'clave_numerica': individual_data['ReturnClaveNumerica'],
                                   'date': individual_data['ReturnDateTime']
                                   })
            else:
                write_data.update({
                    'success': success
                })
        else:
            write_data.update({
                'success': success
            })
        id.write(write_data)

        # val = urlencode({'file_data' : txt.encode('UTF-8') , 'file_name' : file_name})
        #
        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': '/attachment/download?'+ val,
        #     'target': 'self',
        # }


    def _get_phone(self, id):
        if id.phone:
            return str(id.phone)
        return ''


    def _get_fax(self, id):
        if id.fax_no:
            return str(id.fax_no)
        return ''


    def _get_name(self, name, empty_space=False):
        if name:
            return self._get_string(name.name, empty_space)

        return ''


    def _get_code(self, code):
        if code:
            return code.code

        return ''


    def _get_string(self, string, empty_space=False):
        if string:
            if empty_space and len(string) > 0:
                string = string + ' '
            return string
        return ''


    def _get_full_address(self, object):
        address = ''
        address += self._get_string(object.street, True) + self._get_string(object.street2, True) + self._get_name(
            object.locality_id, True) + self._get_name(object.district_id, True) + self._get_name(object.canton_id,
                                                                                                  True) + self._get_name(
            object.province_id, True) + self._get_name(object.country_id, True) + self._get_string(object.zip, True)
        return address[0:160]


    def _get_issuer_name(self, id):
        if self._get_doc_type(id) and self._get_doc_type(id).name:
            return self._get_doc_type(id).name
        else:
            raise UserError('Required data is missing or empty')


    def _get_vat_no(self, id):
        if self._get_doc_type(id).vat and len(self._get_doc_type(id).vat) <= 12 and self._no_special(
                self._get_doc_type(id).vat):
            return self._get_doc_type(id).vat
        else:
            raise UserError('Required data is missing or empty')


    def _get_company_registry_no(self, id):
        if self._get_doc_type(id).company_registry and len(
                self._get_doc_type(id).company_registry) <= 12 and self._no_special(
            self._get_doc_type(id).company_registry):
            return self._get_doc_type(id).company_registry
        else:
            raise UserError('Required data is missing or empty')


    def _no_special(self, character):
        all_normal_characters = string.ascii_letters + string.digits
        for char in character:
            if char not in all_normal_characters:
                return False
        return True


    def _is_number(self, data, field):
        if len(data) > 20:
            raise UserError('Only max of 20 characters allowed for the field - ' + field.field_description)
        if data.isdigit():
            return data

        raise UserError('Only numbers allowed for the field - ' + field.field_description)


    def _company_registry_no(self, data, field):
        if data.company_registry and len(data.company_registry) <= 12 and self._no_special(data.company_registry):
            return data.company_registry

        raise UserError(
            'Please check your - Company Registration No. cannot be greater than 12 character and no special characters allowed')


    def _vat(self, data, field):
        if len(data.vat) > 13:
            raise UserError('Only max of 13 characters allowed for the field - ' + field.field_description)
        return data.vat


    def _full_address(self, data, field):
        address = ''
        address += self._get_string(data.street, True) + self._get_string(data.street2, True) + self._get_name(
            data.locality_id, True) + self._get_name(data.district_id, True) + self._get_name(data.canton_id,
                                                                                              True) + self._get_name(
            data.province_id, True) + self._get_name(data.country_id, True) + self._get_string(data.zip, True)
        return address[0:160]


    def _version(self, data, field):
        return '4.5'


    def _invoice_time(self, data, field):
        return '00:00:00'


    def _check_required(self, data, description):
        if data != False:
            return True

        raise UserError('Required data is missing for the field - ' + description)


    def _state(self, id):
        if id.type == 'out_refund':
            return '0'
        return '1'


    def _doc_type(self, id):
        if id.type == 'out_invoice':
            return '01'
        elif id.type == 'out_refund':
            return '02'
        elif id.type == 'in_refund':
            return '03'


    def _get_doc_type(self, id, opp=False):
        # if id.type == 'out_invoice' or id.type == 'out_refund':
        if opp:
            return id.partner_id
        return id.company_id
        # elif id.type == 'in_invoice' or id.type == 'in_refund':
        #     if opp:
        #         return id.company_id
        #     return id.partner_id
        # elif id.type == 'in_refund':
        #     return id.partner_id
        # elif id.type == 'out_refund':
        #     return id.company_id
