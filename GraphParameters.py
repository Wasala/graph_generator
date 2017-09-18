from random import randint, choice, uniform, getrandbits, random

class GraphParameters:
    """
    ##designName: string, no constraints
    ##serie: string enumeration, no constraints on the value, but there should be more than one architecture with the same value
    ##targetMarket { Europe | Asia | South America }
    ##battery_type: { Li-ion polymer | Lithium-Ion | VRLA, NiCd }
    ##price: double in the range of 1 to 350
    ##horsepower: integer in the range of 60 to 350
    ##mpg: double in the range of 20 to 50
    ##cylinder: integer in the range of 3 to 8
    ##engine size: double between 1.2 and 4.0
    ##controller: integer between 1 and 7
    ##isDiesel: randomly { true | false}
    ##hasTurbo: randomly {true | false }
    ##isPlugIn : randomly { true | false }
    """
    NODE_TYPES = ["nodetypeA", "nodetypeB"]
    TARGET_MARKETS = ["Europe" , "Asia" , "South America"]
    BATTERY_TYPE = ["Li-ion polymer" , "Lithium-Ion", "VRLA, NiCd" ]
    DRIVE_WHEELS = ["fwd" , "4wd", "rwd" ]
    SERIE = set()
    design_counter = 0

    @staticmethod
    def get_node_type():
        return choice(GraphParameters.NODE_TYPES)

    @staticmethod
    def get_design_name():
        """
        designName: string, no constraints
        :return: string
        """
        GraphParameters.design_counter += 1
        suffix = 'th' if 11 <= GraphParameters.design_counter <=13 else {1:'st',2:'nd',3:'rd'}.get(GraphParameters.design_counter % 10, 'th')
        return "%s%s Example" % (GraphParameters.design_counter, suffix)  #"design-" + ''.join(choice('0123456789ABCDEF') for i in range(4))

    @staticmethod
    def get_serie(probability_of_using_same_serie = 0.1):
        """
        string enumeration, no constraints on the value, but can be a more than one architecture with the same value
        :return: string
        """
        if random() < probability_of_using_same_serie and GraphParameters.SERIE:
            return choice(list(GraphParameters.SERIE))
        serie = "Alpha-"+ ''.join(choice('0123456789ABCDEF-') for i in range(8)).strip("-")
        GraphParameters.SERIE.add(serie)
        return serie

    @staticmethod
    def get_target_market():
        """
        targetMarket { Europe | Asia | South America }
        :return: string
        """
        return choice(GraphParameters.TARGET_MARKETS)

    @staticmethod
    def get_drive_wheels():
        """
        :return: string
        """
        return choice(GraphParameters.DRIVE_WHEELS)

    @staticmethod
    def get_battery_type():
        """
        battery_type: { Li-ion polymer | Lithium-Ion | VRLA, NiCd }
        :return: string
        """
        return choice(GraphParameters.BATTERY_TYPE)

    @staticmethod
    def get_price():
        """
        double in the range of 1 to 350
        :return: float
        """
        return uniform(1.0, 350.0)

    @staticmethod
    def get_horse_power():
        """
        horsepower: integer in the range of 60 to 350
        :return: integer
        """
        return float(randint(60, 350)) #added float as the sample files requires field to be a double

    @staticmethod
    def get_mpg():
        """
        double in the range of 20 to 50
        :return: float
        """
        return uniform(20.0, 50.0)

    @staticmethod
    def get_cylinder():
        """
        cylinder: integer in the range of 3 to 8
        :return: integer
        """
        return randint(3, 8)

    @staticmethod
    def double_range(start, stop, step):
        """
        mimicks range() function but for doubles/floats.
        :param start: starting number
        :param stop: ending number
        :param step: step
        :return: double
        """
        r = start
        while r < stop:
            yield r
            r += step

    @staticmethod
    def get_engine_size():
        """
        double between 1.2 and 4.0
        :return: double
        """
        possibilities = [d for d in GraphParameters.double_range(1.2, 4.2, 0.2)]
        return choice(possibilities)

    @staticmethod
    def get_controller():
        """
        controller: integer between 1 and 7
        :return: integer between 1 and 7
        """
        return randint(1, 7)

    @staticmethod
    def get_is_diesel():
        """
        isDiesel: randomly { true | false}
        :return: boolean
        """
        return bool(getrandbits(1))

    @staticmethod
    def get_has_turbo():
        """
        hasTurbo: randomly {true | false }
        :return: boolean
        """
        return bool(getrandbits(1))

    @staticmethod
    def get_is_plugin():
        """
        isPlugIn : randomly { true | false }}
        :return: boolean
        """
        return bool(getrandbits(1))


