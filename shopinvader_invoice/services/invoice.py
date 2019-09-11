# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component


class InvoiceService(Component):
    _inherit = "shopinvader.invoice.service"

    def search(self, **params):
        """
        Get every invoices related to logged user
        :param params: dict/json
        :return: dict
        """
        return self._paginate_search(**params)

    def _validator_search(self):
        """
        Validator for the search
        :return: dict
        """
        schema = {
            "per_page": {
                "coerce": to_int,
                "nullable": True,
                "type": "integer",
            },
            "page": {"coerce": to_int, "nullable": True, "type": "integer"},
        }
        return schema

    def _validator_return_get(self):
        """
        Output validator for the search
        :return: dict
        """
        invoice_schema = {
            "invoice_id": {"type": "integer"},
            "number": {"type": "string"},
            "date_invoice": {"type": "string"},
            "amount_total": {"type": "float"},
            "amount_tax": {"type": "float"},
            "amount_untaxed": {"type": "float"},
            "amount_due": {"type": "float"},
            "type": {"type": "string"},
            "type_label": {"type": "string"},
            "state": {"type": "string"},
            "state_label": {"type": "string"},
        }
        schema = {"data": {"type": "dict", "schema": invoice_schema}}
        return schema

    def _validator_return_search(self):
        """
        Output validator for the search
        :return: dict
        """
        invoice_schema = {
            "invoice_id": {"type": "integer"},
            "number": {"type": "string"},
            "date_invoice": {"type": "string"},
            "amount_total": {"type": "float"},
            "amount_tax": {"type": "float"},
            "amount_untaxed": {"type": "float"},
            "amount_due": {"type": "float"},
            "type": {"type": "string"},
            "state": {"type": "string"},
            "type_label": {"type": "string"},
            "state_label": {"type": "string"},
        }
        schema = {
            "size": {"type": "integer"},
            "data": {
                "type": "list",
                "schema": {"type": "dict", "schema": invoice_schema},
            },
        }
        return schema

    def _get_parser_invoice(self):
        """
        Get the parser of account.invoice
        :return: list
        """
        to_parse = [
            "id:invoice_id",
            "number",
            "date_invoice",
            "amount_total",
            "amount_tax",
            "amount_untaxed",
            "residual:amount_due",
            "type",
            "state",
        ]
        return to_parse

    def _to_json_invoice(self, invoice):
        invoice.ensure_one()
        parser = self._get_parser_invoice()
        values = invoice.jsonify(parser)[0]
        values.update(
            {
                "type_label": self._get_selection_label(invoice, "type"),
                "state_label": self._get_selection_label(invoice, "state"),
            }
        )
        return values

    def _to_json(self, invoices):
        res = []
        for invoice in invoices:
            res.append(self._to_json_invoice(invoice))
        return res
