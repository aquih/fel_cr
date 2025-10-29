# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from datetime import datetime
import base64
from lxml import etree
import requests
import re

import logging

class AccountMove(models.Model):
    _inherit = "account.move"

    consecutivo_fel = fields.Char('Consecutivo FE', copy=False)
    clave_numerica_fel = fields.Char('Serie FE', copy=False)
    factura_original_id = fields.Many2one('account.move', string="Factura original FE", domain="[('invoice_date', '!=', False)]")
    certificador_fel = fields.Char('Certificador FE', copy=False)
    pdf_fel = fields.Binary('PDF FE', copy=False)
    pdf_fel_name = fields.Char('Nombre PDF FE', default='pdf_fel.pdf', size=32)
    xml_fel = fields.Binary('XML FE', copy=False)
    xml_fel_name = fields.Char('Nombre XML FE', default='xml_fel.xml', size=32)
    
    def error_certificador(self, error):
        self.ensure_one()
        factura = self
        if factura.journal_id.error_en_historial_fel:
            factura.message_post(body='<p>No se publicó la factura por error del certificador FEL:</p> <p><strong>'+error+'</strong></p>')
        else:
            raise UserError('No se publicó la factura por error del certificador FEL: '+error)

    def requiere_certificacion_cr(self, certificador=''):
        self.ensure_one()
        factura = self
        requiere = factura.is_invoice() and factura.journal_id.generar_cr_fel and factura.amount_total != 0
        if certificador:
            requiere = requiere and ( factura.company_id.certificador_cr_fel == certificador or not factura.company_id.certificador_cr_fel)
        return requiere

    def error_pre_validacion_cr(self):
        self.ensure_one()
        factura = self
        if factura.consecutivo_fel:
            factura.error_certificador("La factura ya fue validada, por lo que no puede ser validada nuevamnte")
            return True

        return False

class AccountJournal(models.Model):
    _inherit = "account.journal"

    generar_cr_fel = fields.Boolean('Generar FE')
    tipo_documento_cr_fel = fields.Selection([('1', 'Factura electrónica'), ('2', 'Nota de débito electrónica'), ('3', 'Nota de crédito electrónica'), ('4', 'Tiquete electrónico'), ('8', 'Factura electrónica de compra'), ('9', 'Factura electrónica de exportación')], 'Tipo de Documento FE', copy=False)
    codigo_actividad_fel = fields.Char('Código Actividad FE', copy=False)
    error_en_historial_fel = fields.Boolean('Registrar error FE', help='Los errores no se muestran en pantalla, solo se registran en el historial')
    contingencia_fel = fields.Boolean('Habilitar contingencia FE')
    
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    codigo_cabys_fel = fields.Char('Código Cabys FE', copy=False)
    
class UoM(models.Model):
    _inherit = "uom.uom"
    
    codigo_fel = fields.Char('Código FE', copy=False)
    
class ResCompany(models.Model):
    _inherit = "res.company"
    
    certificador_cr_fel = fields.Selection([], 'Certificador CR FE')
