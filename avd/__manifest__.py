{
    'name' : 'AVD Text File',
    'version' : '1.1',
    'author' : 'Janeindiran',
    'summary': 'Send Invoices and Track Payments',
    'sequence': 30,
    'description': """Text file to submit invoice information""",
    'category': 'Accounting',
    'depends' : ['base','base_setup', 'account'],
    'installable': True,
    'website': 'https://janeindiran.com',
    'application': False,
    'auto_install': False,
    'external_dependencies': {'python': ['xmltodict']},
    'data': [
        #import data
        'data/locality_province.xml',
        'data/locality_canton.xml',
        'data/locality_district.xml',
        'data/locality_locality.xml',
        # 'data/product_data.xml',

        #views
        'views/res_partner.xml',
        'views/res_company.xml',
        'views/account_invoice.xml',
        'views/account_tax.xml',
        'views/product_uom.xml',
        # 'views/base_config.xml',

        #action
        # 'views/action_txt_file.xml'
    ]

}
