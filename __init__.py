# This file is part pyme module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import account
from . import attachment
from . import bank
from . import company
from . import invoice
from . import product
from . import purchase
from . import sale
from . import stock

def register():
    Pool.register(
        account.AccountConfiguration,
        attachment.Attachment,
        bank.BankAccount,
        company.Employee,
        invoice.Invoice,
        product.ProductTemplate,
        module='pyme', type_='model')
    Pool.register(
        purchase.Purchase,
        purchase.PurchaseLine,
        depends=['purchase'],
        module='party_company', type_='model')
    Pool.register(
        sale.Sale,
        sale.SaleLine,
        depends=['sale'],
        module='party_company', type_='model')
    Pool.register(
        stock.Move,
        stock.ShipmentIn,
        stock.ShipmentInReturn,
        stock.ShipmentInternal,
        stock.ShipmentOut,
        stock.ShipmentOutReturn,
        depends=['stock'],
        module='party_company', type_='model')
