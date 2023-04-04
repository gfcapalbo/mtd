# -*- coding = utf-8 -*-

import logging

from odoo.osv import osv
from odoo import fields, api, models
logger = logging.getLogger(__name__)

class MtdAccountTaxCode(osv.osv):
    _inherit = "account.tax"

    vat_tax_scope = fields.Selection([
        ('ST', 'ST'),
        ('PT', 'PT'),
        ('PTR', 'PTR'),
        ('PTM', 'PTM'
                '')
    ], string="UK VAT Scope")

    @api.model
    def _update_vat_tax_scope(self):
        account_tax_obj = self.env['account.tax'].search([])

        for record in account_tax_obj:
            try:
                if 'PT8M' in record.mapped('tag_ids.name'):
                    record.vat_tax_scope = 'PTM'
                elif 'PT8R' in record.mapped('tag_ids.name'):
                    record.vat_tax_scope = 'PTR'
                 elif 'PT8MBR' in record.mapped('tag_ids.name'):
                    record.vat_tax_scope = 'PTM'
                elif 'PT8RBR' in record.mapped('tag_ids.name'):
                    record.vat_tax_scope = 'PTR'
                elif  any( [ x and  x.startswith('ST') for x in  record.mapped("tag_ids.name")] ): # in ('ST0', 'ST1', 'ST11', 'ST2', 'ST4'):
                    record.vat_tax_scope = 'ST'
                elif  any( [ x and  x.startswith('PT') for x in  record.mapped("tag_ids.name")] ): # in ('PT0', 'PT1', 'PT11', 'PT2', 'PT5', 'PT7', 'PT8'):
                    record.vat_tax_scope = 'PT'
            except:
                logger.info("=======================ERROR  IN PROCESSING: RECORD %s,   TAGIDS %s " % (record.id, record.tag_ids or "NO TAG ID"))

        return True
