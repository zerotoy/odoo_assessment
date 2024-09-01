import psycopg2
from odoo import api, SUPERUSER_ID

def pre_init_hook(cr, registry):
    # This function will be called after module installation or upgrade
    print("here")
    # SQL commands to create the function and trigger
    sql_commands ="""
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
    
        CREATE TRIGGER reservation_overlap_check
        BEFORE INSERT OR UPDATE ON room_reservation
        FOR EACH ROW
        EXECUTE FUNCTION check_reservation_overlap();
        """
    
    cr.execute(sql_commands)

    # Execute SQL commands
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        with env.cr.cursor() as cursor:
            for command in sql_commands:
                cursor.execute(command)
            env.cr.commit()
