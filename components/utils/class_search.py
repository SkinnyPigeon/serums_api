from sqlalchemy.ext.declarative.api import DeclarativeMeta


def get_class_by_name(patient_table: str, base: DeclarativeMeta):
    """
    A very useful helper function for searches the SQLAlchemy class \
    definitions within the database for a particular table by its name

        Parameters:
            patient_table (str): The full name of the table within \
                                 the source system
            base (DeclarativeMeta): The SQLAlchemy Base instance that \
                                    contains the relevant metadata to \
                                    enable the search
        Returns:
            table (DeclarativeMeta): An SQLAlchemy Table class that \
                                     contains the relevant columns \
                                     for searching
    """
    for class_name in base._decl_class_registry.values():
        if hasattr(class_name, '__table__') \
                and class_name.__table__.fullname == patient_table:
            return class_name
