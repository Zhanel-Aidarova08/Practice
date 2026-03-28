-- procedures.sql
-- Run this file in psql or pgAdmin before starting phonebook.py
-- psql -U postgres -d phonebook_db -f procedures.sql

-- ─────────────────────────────────────────────────────────────────
-- 1. Upsert: insert a contact; if name exists — update phone
-- ─────────────────────────────────────────────────────────────────
-- Usage: CALL upsert_contact('Aibek', 'Dzhaksybekov', '+77011111111');
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name  VARCHAR,
    p_phone      VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook
        WHERE first_name = p_first_name AND last_name = p_last_name
    ) THEN
        UPDATE phonebook
        SET    phone = p_phone
        WHERE  first_name = p_first_name AND last_name = p_last_name;
        RAISE NOTICE 'Updated phone for % %', p_first_name, p_last_name;
    ELSE
        INSERT INTO phonebook (first_name, last_name, phone)
        VALUES (p_first_name, p_last_name, p_phone);
        RAISE NOTICE 'Inserted new contact: % %', p_first_name, p_last_name;
    END IF;
END;
$$;


-- ─────────────────────────────────────────────────────────────────
-- 2. Bulk insert from arrays; validates phone format,
--    returns invalid rows via a temp table
-- ─────────────────────────────────────────────────────────────────
-- Phone rule: starts with +7 followed by exactly 10 digits
-- Usage:
--   CALL bulk_insert_contacts(
--       ARRAY['Aibek','Nurlan'],
--       ARRAY['Dzhaksybekov','Seitkali'],
--       ARRAY['+77011234567','+7invalid']
--   );
--   SELECT * FROM invalid_contacts_temp;   -- see rejected rows
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_first_names VARCHAR[],
    p_last_names  VARCHAR[],
    p_phones      VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i           INT;
    v_first     VARCHAR;
    v_last      VARCHAR;
    v_phone     VARCHAR;
    v_count     INT;
BEGIN
    -- Create temp table to collect bad rows (visible in current session)
    DROP TABLE IF EXISTS invalid_contacts_temp;
    CREATE TEMP TABLE invalid_contacts_temp (
        first_name VARCHAR,
        last_name  VARCHAR,
        phone      VARCHAR,
        reason     TEXT
    );

    v_count := array_length(p_first_names, 1);

    FOR i IN 1 .. v_count LOOP
        v_first := p_first_names[i];
        v_last  := p_last_names[i];
        v_phone := p_phones[i];

        -- Validate: must start with +7 and have exactly 10 more digits
        IF v_phone !~ '^\+7[0-9]{10}$' THEN
            INSERT INTO invalid_contacts_temp VALUES
                (v_first, v_last, v_phone, 'Invalid phone format');
            CONTINUE;  -- skip to next row
        END IF;

        -- Upsert valid row
        IF EXISTS (
            SELECT 1 FROM phonebook
            WHERE first_name = v_first AND last_name = v_last
        ) THEN
            UPDATE phonebook SET phone = v_phone
            WHERE  first_name = v_first AND last_name = v_last;
        ELSE
            INSERT INTO phonebook (first_name, last_name, phone)
            VALUES (v_first, v_last, v_phone)
            ON CONFLICT (phone) DO NOTHING;
        END IF;
    END LOOP;

    RAISE NOTICE 'Bulk insert done. Check invalid_contacts_temp for rejected rows.';
END;
$$;


-- ─────────────────────────────────────────────────────────────────
-- 3. Delete by username (first_name) or by phone
-- ─────────────────────────────────────────────────────────────────
-- Pass the value you know; leave the other NULL
-- Usage: CALL delete_contact(p_phone => '+77011234567');
--        CALL delete_contact(p_first_name => 'Aibek');
CREATE OR REPLACE PROCEDURE delete_contact(
    p_first_name VARCHAR DEFAULT NULL,
    p_phone      VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql AS $$
DECLARE
    v_deleted INT := 0;
BEGIN
    IF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
        GET DIAGNOSTICS v_deleted = ROW_COUNT;
        RAISE NOTICE 'Deleted % row(s) with phone = %', v_deleted, p_phone;

    ELSIF p_first_name IS NOT NULL THEN
        DELETE FROM phonebook WHERE first_name ILIKE p_first_name;
        GET DIAGNOSTICS v_deleted = ROW_COUNT;
        RAISE NOTICE 'Deleted % row(s) with first_name = %', v_deleted, p_first_name;

    ELSE
        RAISE EXCEPTION 'Provide at least one of: p_first_name, p_phone';
    END IF;
END;
$$;
