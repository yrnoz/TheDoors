from common.database import Database

"""
this class represent the facilitiess table in the DB
the forrmat is like that:
 {'company':google , 'facility': matam }
"""


def json(company, facility):
    _id = company + " " + facility
    return {
        '_id': _id,
        'company': company,
        'facility': facility
    }


class Facilities(object):
    @staticmethod
    def add_facility(company, facility):
        if Facilities.is_facility_exist(company, facility):
            return False
        else:
            Database.insert('facilities', json(company, facility))
            return True

    @staticmethod
    def add_facility_simulation(company, facility):
        if Facilities.is_facility_exist_simulation(company, facility):
            return False
        else:
            Database.insertSimulation('facilities', json(company, facility))
            return True

    @staticmethod
    def add_company(company, facility):
        if Facilities.is_company_exist(company):
            return False
        else:
            Database.insert('facilities', json(company, facility))
            return True

    @staticmethod
    def add_company_simulation(company, facility):
        if Facilities.is_company_exist_simulation(company):
            return False
        else:
            Database.insertSimulation('facilities', json(company, facility))
            return True

    @staticmethod
    def remove_facility(company, facility):
        if Facilities.is_facility_exist(company, facility):
            _id = company + ' ' + facility
            Database.remove('facilities', {'_id': _id})
            return True
        else:
            return False

    @staticmethod
    def get_facilities(company):
        """
        :param company:
        :return: List of company's facilities
        """
        facility_dict = Database.find('facilities', {'company': company})

        facilities = []
        for facility in facility_dict:
            facility = facility['facility']
            facilities.append(facility)
        return facilities

    @staticmethod
    def is_facility_exist(company, facility):
        """
        :param company:
        :param facility:
        :return: True if this company already have this facility
        """
        _id = company + ' ' + facility
        data = Database.find_one('facilities', {'_id': _id})
        if data is not None:
            return True
        else:
            return False

    @staticmethod
    def is_facility_exist_simulation(company, facility):
        """
        :param company:
        :param facility:
        :return: True if this company already have this facility
        """
        _id = company + ' ' + facility
        data = Database.find_oneSimulation('facilities', {'_id': _id})
        if data is not None:
            return True
        else:
            return False

    @staticmethod
    def is_company_exist(company):
        """
        :param company:
        :param :
        :return: True if this company already exist
        """
        data = Database.find_one('facilities', {'company': company})
        if data is not None:
            return True
        else:
            return False

    @staticmethod
    def is_company_exist_simulation(company):
        """
        :param company:
        :param :
        :return: True if this company already exist
        """
        data = Database.find_oneSimulation('facilities', {'company': company})
        if data is not None:
            return True
        else:
            return False