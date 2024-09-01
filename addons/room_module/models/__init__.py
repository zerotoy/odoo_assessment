# -*- coding: utf-8 -*-

from . import room
from odoo import api, SUPERUSER_ID

# def _execute_sql_commands(cr):
#     # SQL commands to create the function and trigger
#     sql_commands = [
#         """
#         CREATE OR REPLACE FUNCTION check_reservation_overlap()
#         RETURNS TRIGGER AS $$
#         BEGIN
#             -- Check for overlapping reservations
#             IF EXISTS (
#                 SELECT 1
#                 FROM room_reservation r2
#                 WHERE r2.room_id = NEW.room_id
#                 AND r2.id != NEW.id
#                 AND r2.state != 'cancel'
#                 AND (
#                     (NEW.start_date BETWEEN r2.start_date AND r2.end_date)
#                     OR (NEW.end_date BETWEEN r2.start_date AND r2.end_date)
#                 )
#             ) THEN
#                 RAISE EXCEPTION 'The reservation overlaps with an existing reservation.';
#             END IF;
#             RETURN NEW;
#         END;
#         $$ LANGUAGE plpgsql;
#         """,
#         """
#         CREATE TRIGGER reservation_overlap_check
#         BEFORE INSERT OR UPDATE ON room_reservation
#         FOR EACH ROW
#         EXECUTE FUNCTION check_reservation_overlap();
#         """
#     ]

#     for command in sql_commands:
#         cr.execute(command)
#     cr.commit()

# def init(cr, registry):
#     sql_command =  """
#         CREATE OR REPLACE FUNCTION check_reservation_overlap()
#         RETURNS TRIGGER AS $$
#         BEGIN
#             -- Check for overlapping reservations
#             IF EXISTS (
#                 SELECT 1
#                 FROM room_reservation r2
#                 WHERE r2.room_id = NEW.room_id
#                 AND r2.id != NEW.id
#                 AND r2.state != 'cancel'
#                 AND (
#                     (NEW.start_date BETWEEN r2.start_date AND r2.end_date)
#                     OR (NEW.end_date BETWEEN r2.start_date AND r2.end_date)
#                 )
#             ) THEN
#                 RAISE EXCEPTION 'The reservation overlaps with an existing reservation.';
#             END IF;
#             RETURN NEW;
#         END;
#         $$ LANGUAGE plpgsql;
#         CREATE TRIGGER reservation_overlap_check
#         BEFORE INSERT OR UPDATE ON room_reservation
#         FOR EACH ROW
#         EXECUTE FUNCTION check_reservation_overlap();
#         """
#     cr.execute(sql_command)