"""Initialize the database and permanent admin without putting passwords in shell history."""
from auth.service import bootstrap_admin, AuthError
from database.store import initialize_database


def main():
    initialize_database()
    try:
        status = bootstrap_admin()
    except AuthError as exc:
        print(f"Admin setup error: {exc}")
        raise SystemExit(1)
    if status == "needs_password":
        print('Set ADMIN_INITIAL_PASSWORD in .env to a strong password, then run this command again.')
        raise SystemExit(1)
    print(f"Admin setup: {status}. Login username is Mr. Doc.")
    print('After success, REMOVE ADMIN_INITIAL_PASSWORD from your .env file.')


if __name__ == "__main__":
    main()
