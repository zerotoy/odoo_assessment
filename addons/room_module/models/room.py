# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room'
    
    name = fields.Char(string='Nama Ruangan',required=True)
    room_type = fields.Selection(string='Tipe Ruangan',selection=[('kecil', 'Ruangan Kecil'), ('besar', 'Ruangan Besar'), ('aula', 'Aula')],required=True)
    room_loc = fields.Selection(string='Lokasi Ruangan',selection=[('one_a', '1A'), ('one_b', '1B'), ('one_c', '1C'), ('two_a', '2A'), ('two_b', '2B'), ('two_c', '2C')],required=True)
    room_photo = fields.Binary(string='Foto Ruangan',required=True)
    room_capacity = fields.Integer(string='Kapasitas Ruangan', help="Jummlah hadirin yang dapat ditampung di ruangan.",required=True)
    notes = fields.Text(string='Keterangan')
    
    def name_get(self):
        result = []
        for record in self:
            room_loc_display = dict(self._fields['room_loc'].selection).get(record.room_loc, '')
            display_name = f"[{room_loc_display}] {record.name}"
            result.append((record.id, display_name))
        return result
    
class RoomReservation(models.Model):
    _name = 'room.reservation'
    _description = 'Room Reservation'
    _order = 'name desc,id desc'
    
    name = fields.Char(string='Nomor Pemesanan',index=True, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('room.reservation'), copy=False,required=True)
    room_id = fields.Many2one(string='Ruangan',comodel_name='room.room',ondelete='restrict', required=True)
    pemesan = fields.Char(string='Nama Pemesan',required=True)
    start_date = fields.Datetime(string='Waktu Check In',required=True)
    end_date = fields.Datetime(string='Waktu Check Out',required=True)
    state = fields.Selection(
        string='Status Pemesanan',
        selection=[('draft', 'Draft'), ('progress', 'On Going'), ('done', 'Done'), ('cancel', 'Cancel')],default='draft'
    )
    notes = fields.Text(string='Catatan Pemesanan')
    
    def init(self):
        print("here")
        sql_command =  """
            -- Drop the trigger if it exists
            DROP TRIGGER IF EXISTS reservation_overlap_check ON room_reservation;

            -- Drop the function if it exists
            DROP FUNCTION IF EXISTS check_reservation_overlap;

            -- Create or replace the function
            CREATE OR REPLACE FUNCTION check_reservation_overlap()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Check for overlapping reservations
                IF EXISTS (
                    SELECT 1
                    FROM room_reservation r2
                    WHERE r2.room_id = NEW.room_id
                    AND r2.id != NEW.id
                    AND r2.state != 'cancel'
                    AND (
                        (NEW.start_date BETWEEN r2.start_date AND r2.end_date)
                        OR (NEW.end_date BETWEEN r2.start_date AND r2.end_date)
                    )
                ) THEN
                    RAISE EXCEPTION 'The reservation overlaps with an existing reservation.';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            -- Create the trigger
            CREATE TRIGGER reservation_overlap_check
            BEFORE INSERT OR UPDATE ON room_reservation
            FOR EACH ROW
            EXECUTE FUNCTION check_reservation_overlap();

            """
        self.env.cr.execute(sql_command)
    
    @api.onchange('start_date', 'end_date')
    def _onchange_dates(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                self.end_date = self.start_date
                return {
                    'warning': {
                        'title': "Rentang Tanggal Tidak Valid",
                        'message': "Tanggal akhir tidak dapat lebih awal dari tanggal mulai. Tanggal akhir telah disesuaikan.",
                    }
                }
                
    _sql_constraints = [
    ('name_unique', 'unique(name)', 'The reservation number must be unique.'),
    ('start_end_dates_check', 
     'CHECK (start_date < end_date)', 
     'The start date must be earlier than the end date.')]

    @api.constrains('start_date', 'end_date', 'room_id', 'state')
    def _check_room_reservation_dates(self):
        for reservation in self:
            if reservation.state == 'cancel':
                continue
            overlapping_reservations = self.env['room.reservation'].search([
                ('room_id', '=', reservation.room_id.id),
                ('id', '!=', reservation.id),
                ('state', '!=', 'cancel'),
                '|', '|',
                ('start_date', '<=', reservation.end_date),
                ('end_date', '>=', reservation.start_date),
                ('start_date', '<=', reservation.end_date),
                ('end_date', '>=', reservation.start_date),
            ])
            if overlapping_reservations:
                raise ValidationError('Ruangan sudah dipesan untuk rentang tanggal yang dipilih.')

    def action_progress(self):
        self.ensure_one()
        if self.state != 'draft':
            raise ValidationError("Only draft reservations can be moved to On Going.")
        self.state = 'progress'

    def action_done(self):
        self.ensure_one()
        if self.state != 'progress':
            raise ValidationError("Only reservations in On Going state can be moved to Done.")
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.state !='draft':
            raise ValidationError("Only draft or On Going reservations can be moved to Cancel.")
        self.state = 'cancel'
