from read_table import tableA17()
import matplotlib

atm_pressure = 101 #101 kPa
atm_temperature = 25+273 #Kelvin

air_density = 1.225 #kg/m3 

class car(object):
    """
        The car class 
    """
    def __init__(self,displacement,power,torque,comp_ratio,bore,stroke): #units assumed to be all relevant SI units
        self._displacement = displacement
        self._power = power
        self._torque = torque
        self._comp_ratio = comp_ratio
        self._bore = bore
        self._stroke = stroke

HONDA = car(3471,208.8,355.22,11.5,.089,.093) #value names seen above, values taken from reference sheets or internet if necessary
JEEP = car(2987,177,550,16.5,.083,.092)

for CAR in [HONDA,JEEP]:
    # KG / CYCLE = KG/M3 * M3/CC * CC/STROKE * STROKES/CYCLE
    M_Cycle = 1.225 * (1/1000000) * CAR._displacement * 6 # both are 6 cylinder engines

