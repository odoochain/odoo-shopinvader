# Copyright 2021 Camptocamp SA (http://www.camptocamp.com).
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductPackaging(models.Model):

    _inherit = "product.packaging"

    shopinvader_display = fields.Boolean(
        compute="_compute_shopinvader_display",
        readonly=False,
        store=True,
        help="Include this packaging into Shopinvader product metadata.",
    )

    @api.depends("packaging_type_id.shopinvader_display")
    def _compute_shopinvader_display(self):
        for record in self:
            record.shopinvader_display = record.packaging_type_id.shopinvader_display
