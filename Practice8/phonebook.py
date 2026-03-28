# phonebook.py  —  Practice 8
# PhoneBook that delegates all logic to PostgreSQL functions & procedures.
# Run once: psql -U postgres -d phonebook_db -f functions.sql -f procedures.sql
# Then:     python phonebook.py

import psycopg2
from connect import get_connection


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def _print_rows(rows, headers=("ID", "First", "Last", "Phone")):
    if not rows:
        print("  (no results)")
        return
    widths = [5, 15, 15, 20]
    header_line = "  " + "  ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(header_line)
    print("  " + "-" * (sum(widths) + len(widths) * 2))
    for row in rows:
        print("  " + "  ".join(str(v or "").ljust(w) for v, w in zip(row, widths)))


def _ensure_sql_loaded():
    """Remind the user to load SQL files if they haven't yet."""
    print("\n[HINT] If you see 'function does not exist' errors, run:")
    print("  psql -U postgres -d phonebook_db -f functions.sql -f procedures.sql\n")


# ─────────────────────────────────────────────
#  FUNCTIONS  (called with SELECT)
# ─────────────────────────────────────────────

def search_by_pattern():
    """Call search_contacts(pattern) function."""
    pattern = input("Search pattern (name / surname / phone): ").strip()
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
                rows = cur.fetchall()
        print(f"\n  Results for '{pattern}':")
        _print_rows(rows)
    except psycopg2.Error as e:
        print("[DB ERROR]", e)
        _ensure_sql_loaded()


def show_page():
    """Call get_contacts_page(page, page_size) function."""
    try:
        page      = int(input("Page number (starts at 1): ").strip())
        page_size = int(input("Page size  [5]: ").strip() or 5)
    except ValueError:
        print("[ERROR] Enter a valid integer.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_page(%s, %s);",
                    (page, page_size),
                )
                rows = cur.fetchall()
        print(f"\n  Page {page} (size {page_size}):")
        _print_rows(rows)
    except psycopg2.Error as e:
        print("[DB ERROR]", e)
        _ensure_sql_loaded()


# ─────────────────────────────────────────────
#  PROCEDURES  (called with CALL)
# ─────────────────────────────────────────────

def upsert_contact():
    """Call upsert_contact(first, last, phone) procedure."""
    print("\n── Upsert contact (insert or update phone) ──")
    first = input("First name : ").strip()
    last  = input("Last name  : ").strip()
    phone = input("Phone      : ").strip()

    if not first or not phone:
        print("[ERROR] First name and phone are required.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL upsert_contact(%s, %s, %s);",
                    (first, last, phone),
                )
            conn.commit()
        print("[OK] Done.")
    except psycopg2.Error as e:
        print("[DB ERROR]", e)
        _ensure_sql_loaded()


def bulk_insert():
    """Call bulk_insert_contacts(names[], last[], phones[]) procedure."""
    print("\n── Bulk insert (enter contacts one by one, empty first name to stop) ──")
    firsts, lasts, phones = [], [], []

    while True:
        first = input("  First name (empty to finish): ").strip()
        if not first:
            break
        last  = input("  Last name : ").strip()
        phone = input("  Phone     : ").strip()
        firsts.append(first)
        lasts.append(last)
        phones.append(phone)

    if not firsts:
        print("[INFO] Nothing to insert.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL bulk_insert_contacts(%s, %s, %s);",
                    (firsts, lasts, phones),
                )
                conn.commit()

                # Show rejected rows from temp table
                cur.execute("SELECT * FROM invalid_contacts_temp;")
                bad = cur.fetchall()

            if bad:
                print(f"\n  [INVALID] {len(bad)} row(s) rejected:")
                bad_headers = ("First", "Last", "Phone", "Reason")
                widths = [15, 15, 20, 30]
                print("  " + "  ".join(h.ljust(w) for h, w in zip(bad_headers, widths)))
                print("  " + "-" * (sum(widths) + len(widths) * 2))
                for row in bad:
                    print("  " + "  ".join(str(v or "").ljust(w) for v, w in zip(row, widths)))
            else:
                print("[OK] All rows inserted successfully.")
    except psycopg2.Error as e:
        print("[DB ERROR]", e)
        _ensure_sql_loaded()


def delete_contact():
    """Call delete_contact(p_first_name, p_phone) procedure."""
    print("\n── Delete contact ──")
    print("  1. Delete by phone")
    print("  2. Delete by first name")
    choice = input("Choice: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if choice == "1":
                    phone = input("Phone: ").strip()
                    cur.execute("CALL delete_contact(p_phone => %s);", (phone,))
                elif choice == "2":
                    name = input("First name: ").strip()
                    cur.execute("CALL delete_contact(p_first_name => %s);", (name,))
                else:
                    print("[ERROR] Invalid choice.")
                    return
            conn.commit()
        print("[OK] Done.")
    except psycopg2.Error as e:
        print("[DB ERROR]", e)
        _ensure_sql_loaded()


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

MENU = """
╔════════════════════════════════════════╗
║     PhoneBook — Practice 8 Menu        ║
╠════════════════════════════════════════╣
║  1. Search by pattern (function)       ║
║  2. Show page (pagination function)    ║
║  3. Upsert contact (procedure)         ║
║  4. Bulk insert with validation        ║
║  5. Delete contact (procedure)         ║
║  0. Exit                               ║
╚════════════════════════════════════════╝
"""


def main():
    print("\n[START] PhoneBook — Practice 8")
    print("[INFO]  Make sure you ran: psql -U postgres -d phonebook_db")
    print("        -f functions.sql -f procedures.sql")

    while True:
        print(MENU)
        choice = input("Select option: ").strip()

        if   choice == "1": search_by_pattern()
        elif choice == "2": show_page()
        elif choice == "3": upsert_contact()
        elif choice == "4": bulk_insert()
        elif choice == "5": delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("[ERROR] Unknown option.")


if __name__ == "__main__":
    main()
