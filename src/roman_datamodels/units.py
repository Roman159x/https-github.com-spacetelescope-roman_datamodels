from astropy import units as u


ROMAN_UNIT_SYMBOLS = ['DN', 'electron']


class Unit(u.Unit):
    """
    Class for the non-VOunits, which need to be serialized by Roman.
    """

    def __init__(self, st, represents=None, doc=None, format=None, namespace=None):
        super().__init__(st, represents=represents, doc=doc, format=format, namespace=namespace)


def def_roman_unit(symbol):
    """
    Define a Roman unit version of an astropy unit.

    This will automatically add the unit to the namespace of this module

    Parameters
    ----------
    symbol : str
        The symbol of the astropy unit to define a Roman unit for.

    Returns
    -------

    A RomanUnit instance
    """

    represents = getattr(u, symbol)

    return Unit(symbol, represents=represents, namespace=globals())


for unit in ROMAN_UNIT_SYMBOLS:
    def_roman_unit(unit)