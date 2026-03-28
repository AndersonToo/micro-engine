# test_orm.py  —  demonstrates the ORM
import os
from orm import BaseModel, TextField, IntegerField, RealField

# ── Define your models (just like Django) ──────────────────────────
class User(BaseModel):
    name     = TextField(nullable=False)
    email    = TextField()
    age      = IntegerField()

class Product(BaseModel):
    title    = TextField(nullable=False)
    price    = RealField()
    stock    = IntegerField()


# ── Run the demo ───────────────────────────────────────────────────
if __name__ == "__main__":

    # Fresh start — delete old DB so demo is clean
    if os.path.exists("db.sqlite3"):
        os.remove("db.sqlite3")
        print("[*] Cleared old db.sqlite3\n")

    # 1. CREATE TABLES
    print("── Creating tables ──")
    User.create_table()
    Product.create_table()
    print()

    # 2. INSERT rows via .save()
    print("── Saving users ──")
    alice = User(name="Alice", email="alice@example.com", age=25).save()
    bob   = User(name="Bob",   email="bob@example.com",   age=30).save()
    carol = User(name="Carol", email="carol@example.com", age=22).save()
    print()

    print("── Saving products ──")
    Product(title="Keyboard", price=45.99, stock=10).save()
    Product(title="Monitor",  price=299.0, stock=4).save()
    print()

    # 3. SELECT ALL
    print("── User.all() ──")
    for user in User.all():
        print(f"  {user}")
    print()

    # 4. SELECT WHERE
    print("── User.filter(age=30) ──")
    results = User.filter(age=30)
    for user in results:
        print(f"  {user}")
    print()

    print("── Product.all() ──")
    for product in Product.all():
        print(f"  {product}")