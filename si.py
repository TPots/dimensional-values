from dataclasses import dataclass
import math

@dataclass
class unitValue:
    __slots__ = ( '_value', '_magnitude', '_order' )
    _value : float
    _magnitude : int
    _order : int

    def __init__( self, value : float, **kwargs) -> None:
        self._value, _mag = self._value_as_scientific( value )

        if 'magnitude' in kwargs:
            self._magnitude = _mag + kwargs[ 'magnitude' ]
        else:
            self._magnitude = _mag

        if 'order' in kwargs:
            self._order = kwargs[ 'order' ]
        else:
            self._order = 1

        if 'si_suffix' in kwargs:
            self._magnitude += self._si_coefficient( kwargs[ 'si_suffix' ] ) * self._order
        return

    @property
    def value( self ) -> float:
        return self._value * math.pow( 10, self._magnitude )

    @property
    def magnitude( self ) -> int:
        return self._magnitude

    @property
    def order( self ) -> int:
        return self._order

    def value_as( self, prefix : str ) -> float:
        prefix_coefficient = math.pow( self._prefix_dict( prefix ), self._order )
        return self._value / prefix_coefficient

    def __add__( self, other : object ) -> object:
        if isinstance(other, unitValue):
            if self._order == other._order:
                mag_diff = self._magnitude - other._magnitude
                return unitValue( self._value + other._value / math.pow( 10, mag_diff), magnitude = self._magnitude, order = self._order )
            else:
                raise ValueError(f'Dimention mismatch between {self} and {other}. Expecting objects with equal orders. Received {self._order=} and {other._order=}')
        else:
            raise ValueError()

    def __sub__( self, other : object ) -> object:
        if isinstance(other, unitValue):
            if self._order == other._order:
                mag_diff = self._magnitude - other._magnitude
                return unitValue( self._value - other._value / math.pow( 10, mag_diff ), magnitude = self._magnitude, order = self._order )
            else:
                raise ValueError(f'Dimention mismatch between {self} and {other}. Expecting objects with equal orders. Received {self._order=} and {other._order=}')
        else:
            raise ValueError()

    def __mul__( self, other : object ) -> object:
        if isinstance(other, unitValue):
            mag_diff = abs(self.magnitude) - abs(other.magnitude)
            return unitValue( self._value * other._value / math.pow( 10, mag_diff ), magnitude = self._magnitude + other._magnitude, order = int( self._order + other._order ) )
        else:
            raise ValueError()

    def __truediv__( self, other : object ) -> object:
        if isinstance(other, unitValue):
            mag_diff = abs(self.magnitude) - abs(other.magnitude)
            return unitValue( self._value / other._value / math.pow( 10, mag_diff ), magnitude = self._magnitude - other._magnitude, order = int( self._order - other._order ) )
        else:
            raise ValueError()
        
    def __str__( self ) -> str:
        return f'{self._value} x 10^{self._magnitude}'


        

    @staticmethod
    def _si_coefficient( suffix : str ):
        si_dict = {
            'peta' : 15 ,
            'tera' : 12 ,
            'giga' : 9 ,
            'mega' : 6 ,
            'kilo' : 3 ,
            'base' : 0,
            'centi' : -2 ,
            'milli' : -3 ,
            'micro' : -6 ,
            'nano' : -9 ,
            'pico' : -12 ,
            'femto' : -15 
            }
        if suffix in si_dict:
            return si_dict[ suffix ]
        else:
            raise ValueError()

    @staticmethod
    def _value_as_scientific( value : float ) -> tuple:

        abs_value = abs( value )
        value_sign = value / abs( value )

        val = 0
        mag = 0

        if value < 0:
            mag = - math.ceil( math.log( 1 / abs_value, 10 ) )
            val = abs_value / math.pow( 10, mag )
            offset = ( - mag % 3 )
            val = val * math.pow( 10, offset )
            mag = mag + offset
        elif value > 0:
            mag = math.floor( math.log( abs_value, 10) )
            val = abs_value / math.pow( 10, mag )
            offset = ( mag % 3 )
            val = val * math.pow( 10, offset )
            mag = mag - offset
        
        return value_sign * round(val, 15), mag
    
def main():
    a = unitValue(2, order = 1, si_suffix = 'micro')
    b = unitValue(3, order = 1, si_suffix = 'nano')
    c = b - a
    print( c )
    return

if __name__ == '__main__':
    main()
