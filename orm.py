# orm.py  —  Phase 5: Mini ORM with Metaclasses + SQLite
import sqlite3

DB_FILE = "db.sqlite3"


# ─────────────────────────────────────────────
# Field descriptors — like Django's models.CharField()
# ─────────────────────────────────────────────

class Field:
    def __init__(self, field_type: str, primary_key=False, nullable=True):
        self.field_type = field_type    # "TEXT", "INTEGER", "REAL"
        self.primary_key = primary_key
        self.nullable = nullable

class TextField(Field):
    def __init__(self, **kwargs):
        super().__init__("TEXT", **kwargs)

class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)

class RealField(Field):
    def __init__(self, **kwargs):
        super().__init__("REAL", **kwargs)


# ─────────────────────────────────────────────
# The Metaclass — runs ONCE when the class is DEFINED
# (not when you create an instance — when Python reads the class body)
# ─────────────────────────────────────────────

class ModelMeta(type):
    def __new__(mcs, class_name, bases, class_dict):
        """
        Called automatically when Python processes:
            class User(BaseModel): ...

        mcs        = ModelMeta itself
        class_name = "User"
        bases      = (BaseModel,)
        class_dict = {"name": TextField(), "age": IntegerField(), ...}
        """

        # Collect all Field instances defined on the class
        fields = {}
        for key, value in class_dict.items():
            if isinstance(value, Field):
                fields[key] = value

        # Store field metadata on the class (not the instance)
        class_dict["_fields"] = fields

        # Table name = lowercase class name  (User -> "users")
        class_dict["_table"] = class_name.lower() + "s"

        return super().__new__(mcs, class_name, bases, class_dict)


# ─────────────────────────────────────────────
# BaseModel — every model inherits from this
# ─────────────────────────────────────────────

class BaseModel(metaclass=ModelMeta):

    def __init__(self, **kwargs):
        # Set instance values:  User(name="alice", age=25)
        self.id = None
        for field_name in self._fields:
            setattr(self, field_name, kwargs.get(field_name))

    # ── DDL: CREATE TABLE ──────────────────────────────────────────
    @classmethod
    def create_table(cls):
        """Dynamically builds CREATE TABLE SQL from the class fields."""
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for field_name, field_obj in cls._fields.items():
            col_def = f"{field_name} {field_obj.field_type}"
            if not field_obj.nullable:
                col_def += " NOT NULL"
            columns.append(col_def)

        sql = f"CREATE TABLE IF NOT EXISTS {cls._table} ({', '.join(columns)});"
        print(f"[ORM] {sql}")

        conn = sqlite3.connect(DB_FILE)
        conn.execute(sql)
        conn.commit()
        conn.close()

    # ── DML: INSERT ────────────────────────────────────────────────
    def save(self):
        """Dynamically generates INSERT INTO SQL and executes it."""
        field_names = list(self._fields.keys())
        values = [getattr(self, f) for f in field_names]
        placeholders = ", ".join(["?" for _ in field_names])
        columns = ", ".join(field_names)

        sql = f"INSERT INTO {self._table} ({columns}) VALUES ({placeholders});"
        print(f"[ORM] {sql}  values={values}")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.execute(sql, values)
        self.id = cursor.lastrowid      # capture the auto-generated ID
        conn.commit()
        conn.close()

        print(f"[ORM] Saved! {self.__class__.__name__}(id={self.id})")
        return self

    # ── DQL: SELECT ALL ────────────────────────────────────────────
    @classmethod
    def all(cls):
        """SELECT * FROM table — returns list of model instances."""
        sql = f"SELECT * FROM {cls._table};"
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        # Map each row back to a model instance
        instances = []
        for row in rows:
            field_names = list(cls._fields.keys())
            kwargs = dict(zip(field_names, row[1:]))  # row[0] is id
            obj = cls(**kwargs)
            obj.id = row[0]
            instances.append(obj)

        return instances

    # ── DQL: SELECT WHERE ──────────────────────────────────────────
    @classmethod
    def filter(cls, **kwargs):
        """SELECT * FROM table WHERE key=value"""
        conditions = " AND ".join([f"{k} = ?" for k in kwargs])
        values = list(kwargs.values())
        sql = f"SELECT * FROM {cls._table} WHERE {conditions};"

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.execute(sql, values)
        rows = cursor.fetchall()
        conn.close()

        field_names = list(cls._fields.keys())
        instances = []
        for row in rows:
            obj_kwargs = dict(zip(field_names, row[1:]))
            obj = cls(**obj_kwargs)
            obj.id = row[0]
            instances.append(obj)

        return instances

    def __repr__(self):
        fields_str = ", ".join(
            f"{k}={getattr(self, k)!r}" for k in self._fields
        )
        return f"<{self.__class__.__name__} id={self.id} {fields_str}>"