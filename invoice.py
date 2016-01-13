# This file is part pyme module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.pyson import Eval, If, Equal
from trytond.transaction import Transaction

__all__ = ['Invoice', 'InvoiceLine']
__metaclass__ = PoolMeta


class Invoice:
    __name__ = 'account.invoice'

    @classmethod
    def view_attributes(cls):
        return super(Invoice, cls).view_attributes() + [
            ('/tree', 'colors',
                If(Equal(Eval('state'), 'draft'), 'blue', 
                If(Equal(Eval('state'), 'validated'), 'green', 
                If(Equal(Eval('state'), 'posted'), 'brown', 
                If(Equal(Eval('state'), 'cancel'), 'grey', 'black')))),
                )]


class InvoiceLine:
    __name__ = 'account.invoice.line'

    @fields.depends('product', 'unit_price')
    def on_change_product(self):
        pool = Pool()
        Company = pool.get('company.company')
        Currency = pool.get('currency.currency')
        Date = pool.get('ir.date')

        super(InvoiceLine, self).on_change_product()

        if self.unit_price:
            return

        company = None
        if Transaction().context.get('company'):
            company = Company(Transaction().context['company'])
        currency = None
        currency_date = Date.today()
        if self.invoice and self.invoice.currency_date:
            currency_date = self.invoice.currency_date
        # TODO check if today date is correct
        if self.invoice and self.invoice.currency:
            currency = self.invoice.currency
        elif self.currency:
            currency = self.currency

        if self.invoice and self.invoice.type:
            type_ = self.invoice.type
        else:
            type_ = self.invoice_type

        if type_ in ('in_invoice', 'in_credit_note'):
            if company and currency:
                with Transaction().set_context(date=currency_date):
                    self.unit_price = Currency.compute(
                        company.currency, self.product.cost_price,
                        currency, round=False)
            else:
                self.unit_price = self.product.cost_price
        else:
            if company and currency:
                with Transaction().set_context(date=currency_date):
                    self.unit_price = Currency.compute(
                        company.currency, self.product.list_price,
                        currency, round=False)
            else:
                self.unit_price = self.product.list_price

        self.type = 'line'
        self.amount = self.on_change_with_amount()