-- functions.sql
-- Run this file in psql or pgAdmin before starting phonebook.py
-- psql -U postgres -d phonebook_db -f functions.sql

-- ─────────────────────────────────────────────────────────────────
-- 1. Search contacts by pattern (name, surname, or phone)
-- ─────────────────────────────────────────────────────────────────
-- Usage: SELECT * FROM search_contacts('aib');
CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE(
    id         INT,
    first_name VARCHAR,
    last_name  VARCHAR,
    phone      VARCHAR
) AS $$
BEGIN
    RETURN QUERY
        SELECT pb.id, pb.first_name, pb.last_name, pb.phone
        FROM   phonebook pb
        WHERE  pb.first_name ILIKE '%' || p_pattern || '%'
            OR pb.last_name  ILIKE '%' || p_pattern || '%'
            OR pb.phone      ILIKE '%' || p_pattern || '%'
        ORDER  BY pb.first_name;
END;
$$ LANGUAGE plpgsql;


-- ─────────────────────────────────────────────────────────────────
-- 2. Paginated query (LIMIT + OFFSET)
-- ─────────────────────────────────────────────────────────────────
-- Usage: SELECT * FROM get_contacts_page(1, 3);
--        page_num starts at 1
CREATE OR REPLACE FUNCTION get_contacts_page(p_page INT, p_page_size INT DEFAULT 5)
RETURNS TABLE(
    id         INT,
    first_name VARCHAR,
    last_name  VARCHAR,
    phone      VARCHAR
) AS $$
DECLARE
    v_offset INT;
BEGIN
    -- Validate inputs
    IF p_page < 1 THEN
        RAISE EXCEPTION 'Page number must be >= 1, got %', p_page;
    END IF;
    IF p_page_size < 1 THEN
        RAISE EXCEPTION 'Page size must be >= 1, got %', p_page_size;
    END IF;

    v_offset := (p_page - 1) * p_page_size;

    RETURN QUERY
        SELECT pb.id, pb.first_name, pb.last_name, pb.phone
        FROM   phonebook pb
        ORDER  BY pb.id
        LIMIT  p_page_size
        OFFSET v_offset;
END;
$$ LANGUAGE plpgsql;
