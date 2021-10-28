# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

class Partner(models.Model):
    _inherit = "res.partner"

    nombre_facturacion_fel = fields.Char('Nombre facturación FEL', copy=False)
    tipo_identificacion_fel = fields.Char('Tipo de identificación FEL', copy=False)
    nombre_comercial_fel = fields.Char('Nombre comercial FEL', copy=False)
    provincia_fel = fields.Char('Provincia FEL', copy=False)
    canton_fel = fields.Char('Canton FEL', copy=False)
    distrito_fel = fields.Char('Distrito FEL', copy=False)
    barrio_fel = fields.Char('Barrio FEL', copy=False)
    
    