import logging
from odoo import models, fields, api
from openerp.osv import osv
import pprint
import inspect
import requests as rq
import os
from cerberus import Validator

_logger = logging.getLogger(__name__)

# INTERNAL_AUTHENTICATION_TOKEN = os.getenv("LINDERA_INTERNAL_AUTHENTICATION_TOKEN")
# URL = os.getenv("LINDERA_API_URL")


class LinderaBackend(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, val):
        _logger.debug('Lets see, if this works')
        res = super(LinderaBackend, self).create(val)


        def callLinderaAPI(data):
            rq.post('https://backend-testing.lindera.de/v2/homes', json=data, headers={'token': 'Beare HfpWLjqt5k0YqIjPgYtb'})

        def validateData(data):
            v = Validator()
            schema = {
                'name': {'type': 'string'}, # map
                'role': {'type': 'string', 'allowed': ['home', 'company', 'organization']},
                'street': {'type': 'string'},
                'zip': {'type': 'string'},
                'city':  {'type': 'string'},
                # 'countrycodeISO316a2':  {'type': 'string'},  # map
            }
            result = v.validate(data, schema)
            return result


        tag = res.category_id
        if tag:
            tags = []
            for item in tag:
                tags.append(item.name)

            # Check if 'Träger' is in the list
            if 'Träger' in tags:
                document = {
                    'name': res.name,
                    'city': res.city,
                    'street': res.street,
                    'zip': res.zip,
                    'role': 'company'
                }

                if (validateData(document)):
                    callLinderaAPI(document)
                else:
                    raise osv.except_osv(('Error!'), ('Invalid input data, address is missing'))

             # Check if 'Einrichtung' is in the list
            if 'Einrichtung' in tags:
                document = {
                    'name': res.name,
                    'city': res.city,
                    'street': res.street,
                    'zip': res.zip,
                    'role': 'home'
                }
                if (validateData(document)):
                    callLinderaAPI(document)
                else:
                    raise osv.except_osv(('Error!'), ('Invalid input data, address is missing'))
                
            
        else:
            print("something")
   
    
        return res



class linderaApi(models.Model):
    _name = "lindera.api"
    _description = "lindera api related info"
