# -*- coding: utf-8 -*-
# from odoo import http
# -*- coding: utf-8 -*-
import json
import math
import logging
import requests

from odoo import http, _, exceptions
from odoo.exceptions import ValidationError,UserError
from odoo.http import request
from datetime import datetime
import pytz

_logger = logging.getLogger(__name__)

class RoomModule(http.Controller):
    
    @http.route(
        '/get_reservations',
        type='http', auth='none', methods=['GET'], csrf=False)
    def get_reservations(self, **params):
        domain = [('state','not in',['done','cancel'])]
        list_rec = []
        try:
            if "state" in params:
                if params['state'] not in ['draft','progress','done','cancel','']:
                    raise ValidationError(_("Invalid state value provided. Valid values are: draft, progress, done, cancel."))
                if params['state']!='':
                    domain = [('state','=',params['state'])]
            if "pemesan" in params:
                if params['pemesan']!='':
                    domain += [('pemesan','like','%'+params['pemesan']+'%')]
            if "room" in params:
                domain += [('room_id.name','like','%'+params['room']+'%')]
            if "reservation_no" in params:
                domain += [('name','like','%'+params['reservation_no']+'%')]
            if "reservation_id" in params:
                try:
                    reservation_id = int(params['reservation_id'])
                    domain += [('id', '=', reservation_id)]
                except ValueError:
                    raise ValidationError(_("Reservation ID must be an integer."))
            if "time" in params:
                try:
                    time_param = datetime.strptime(params['time'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return http.Response(
                        json.dumps({'error': 'Invalid time format. Use YYYY-MM-DD HH:MM:SS'}),
                        status=400,
                        mimetype='application/json'
                    )
                domain += [('start_date','<=',params['time']),('end_date','>=',params['time'])]
            reservations = request.env['room.reservation'].with_user(2).search(domain)
            for record in reservations:
                list_rec.append({
                    'id':record.id,
                    'res_no':record.name,
                    'room':record.room_id.name,
                    'pemesan':record.pemesan,
                    'start_date':record.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_date':record.end_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'state':dict(record._fields['state'].selection).get(record.state, ''),
                    'notes':record.notes,
                })
            result = {'result':list_rec}
        except Exception as e:
            raise e
        if len(list_rec)<1:
            result = {'result':"Reservation Not Found!"}
        return http.Response(
            json.dumps(result),
            status=200,
            mimetype='application/json'
        )
    
#     @http.route('/room_module/room_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/room_module/room_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('room_module.listing', {
#             'root': '/room_module/room_module',
#             'objects': http.request.env['room_module.room_module'].search([]),
#         })

#     @http.route('/room_module/room_module/objects/<model("room_module.room_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('room_module.object', {
#             'object': obj
#         })
