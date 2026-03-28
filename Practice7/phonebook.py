# phonebook.py
# PhoneBook console application backed by PostgreSQL
# Run: python phonebook.py

import csv
import psycopg2
from Practice.Practice7.connect import get_connection


# ─────────────────────────────────────────────
#  TABLE SETUP
# ─────────────────────────────────────────────

def create_table():
    """Create the phonebook table if it doesn't exist."""
    sql = """
        CREATE TABLE IF NOT EXISTS phonebook (
            id         SERIAL PRIMARY KEY,
            first_name VARCHAR(50)  NOT NULL,
            last_name  VARCHAR(50),
            phone      VARCHAR(20)  NOT NULL UNIQUE
        );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print("[OK] Table 'phonebook' is ready.")


# ─────────────────────────────────────────────
#  INSERT
# ─────────────────────────────────────────────

def insert_contact(first_name: str, last_name: str, phone: str):
    """Insert a single contact. Skips duplicates (by phone)."""
    sql = """
        INSERT INTO phonebook (first_name, last_name, phone)
        VALUES (%s, %s, %s)
        ON CONFLICT (phone) DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (first_name, last_name, phone))
        conn.commit()
    print(f"[INSERT] {first_name} {last_name} — {phone}")


def insert_from_csv(filepath: str = "contacts.csv"):
    """Bulk-insert contacts from a CSV file."""
    inserted = 0
    skipped  = 0
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                insert_contact(
                    row["first_name"].strip(),
                    row.get("last_name", "").strip(),
                    row["phone"].strip(),
                )
                inserted += 1
            except Exception as e:
                print(f"  [SKIP] {row} — {e}")
                skipped += 1
    print(f"\n[CSV] Inserted: {inserted} | Skipped: {skipped}")


def insert_from_console():
    """Prompt the user and insert one contact interactively."""
    print("\n── Add new contact ──")
    first_name = input("First name : ").strip()
    last_name  = input("Last name  : ").strip()
    phone      = input("Phone      : ").strip()

    if not first_name or not phone:
        print("[ERROR] First name and phone are required.")
        return

    insert_contact(first_name, last_name, phone)


# ─────────────────────────────────────────────
#  SELECT / SEARCH
# ─────────────────────────────────────────────

def _print_rows(rows):
    if not rows:
        print("  (no results)")
        return
    print(f"\n  {'ID':<5} {'First':<15} {'Last':<15} {'Phone':<20}")
    print("  " + "-" * 57)
    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<15} {(row[2] or ''):<15} {row[3]:<20}")


def search_all():
    """Show every contact."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, first_name, last_name, phone FROM phonebook ORDER BY id;")
            _print_rows(cur.fetchall())


def search_by_name(name: str):
    """Search by first or last name (partial, case-insensitive)."""
    sql = """
        SELECT id, first_name, last_name, phone
        FROM   phonebook
        WHERE  first_name ILIKE %s OR last_name ILIKE %s
        ORDER  BY first_name;
    """
    pattern = f"%{name}%"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (pattern, pattern))
            _print_rows(cur.fetchall())


def search_by_phone_prefix(prefix: str):
    """Search by phone prefix."""
    sql = """
        SELECT id, first_name, last_name, phone
        FROM   phonebook
        WHERE  phone LIKE %s
        ORDER  BY phone;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (f"{prefix}%",))
            _print_rows(cur.fetchall())


# ─────────────────────────────────────────────
#  UPDATE
# ─────────────────────────────────────────────

def update_phone(old_phone: str, new_phone: str):
    """Change a contact's phone number."""
    sql = "UPDATE phonebook SET phone = %s WHERE phone = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (new_phone, old_phone))
            updated = cur.rowcount
        conn.commit()
    if updated:
        print(f"[UPDATE] Phone changed: {old_phone} → {new_phone}")
    else:
        print(f"[UPDATE] Phone '{old_phone}' not found.")


def update_name(phone: str, new_first: str, new_last: str):
    """Change a contact's name by phone."""
    sql = "UPDATE phonebook SET first_name = %s, last_name = %s WHERE phone = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (new_first, new_last, phone))
            updated = cur.rowcount
        conn.commit()
    if updated:
        print(f"[UPDATE] Name updated for {phone}: {new_first} {new_last}")
    else:
        print(f"[UPDATE] Phone '{phone}' not found.")


def update_from_console():
    """Interactive update menu."""
    print("\n── Update contact ──")
    print("  1. Update phone number")
    print("  2. Update name")
    choice = input("Choice: ").strip()

    if choice == "1":
        old = input("Current phone : ").strip()
        new = input("New phone     : ").strip()
        update_phone(old, new)
    elif choice == "2":
        phone = input("Phone         : ").strip()
        first = input("New first name: ").strip()
        last  = input("New last name : ").strip()
        update_name(phone, first, last)
    else:
        print("[ERROR] Invalid choice.")


# ─────────────────────────────────────────────
#  DELETE
# ─────────────────────────────────────────────

def delete_by_phone(phone: str):
    """Delete a contact by phone number."""
    sql = "DELETE FROM phonebook WHERE phone = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (phone,))
            deleted = cur.rowcount
        conn.commit()
    if deleted:
        print(f"[DELETE] Removed contact with phone '{phone}'.")
    else:
        print(f"[DELETE] Phone '{phone}' not found.")


def delete_by_name(first_name: str):
    """Delete all contacts matching a first name."""
    sql = "DELETE FROM phonebook WHERE first_name ILIKE %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (first_name,))
            deleted = cur.rowcount
        conn.commit()
    print(f"[DELETE] Removed {deleted} contact(s) with name '{first_name}'.")


def delete_from_console():
    """Interactive delete menu."""
    print("\n── Delete contact ──")
    print("  1. Delete by phone")
    print("  2. Delete by first name")
    choice = input("Choice: ").strip()

    if choice == "1":
        phone = input("Phone: ").strip()
        delete_by_phone(phone)
    elif choice == "2":
        name = input("First name: ").strip()
        delete_by_name(name)
    else:
        print("[ERROR] Invalid choice.")


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

MENU = """
╔══════════════════════════════╗
║       PhoneBook Menu         ║
╠══════════════════════════════╣
║  1. Show all contacts        ║
║  2. Search by name           ║
║  3. Search by phone prefix   ║
║  4. Add contact (console)    ║
║  5. Import from CSV          ║
║  6. Update contact           ║
║  7. Delete contact           ║
║  0. Exit                     ║
╚══════════════════════════════╝
"""


def main():
    create_table()

    while True:
        print(MENU)
        choice = input("Select option: ").strip()

        if choice == "1":
            search_all()

        elif choice == "2":
            name = input("Enter name to search: ").strip()
            search_by_name(name)

        elif choice == "3":
            prefix = input("Enter phone prefix (e.g. +7701): ").strip()
            search_by_phone_prefix(prefix)

        elif choice == "4":
            insert_from_console()

        elif choice == "5":
            path = input("CSV file path [contacts.csv]: ").strip() or "contacts.csv"
            insert_from_csv(path)

        elif choice == "6":
            update_from_console()

        elif choice == "7":
            delete_from_console()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("[ERROR] Unknown option, try again.")


if __name__ == "__main__":
    main()
