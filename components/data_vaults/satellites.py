from control_files.keys_and_sats.ustan.keys import ustan_keys
from control_files.keys_and_sats.ustan.sats import ustan_sats
from control_files.keys_and_sats.fcrb.keys import fcrb_keys
from control_files.keys_and_sats.fcrb.sats import fcrb_sats
from control_files.keys_and_sats.zmc.keys import zmc_keys
from control_files.keys_and_sats.zmc.sats import zmc_sats
import datetime
import decimal


def pick_sats_and_keys(hospital_id: str):
    """
    Uses the hospital id to select the relevant satellite definitions \
    and primary keys

        Parameters:
            hospital_id (str): The internal reference for the hospitals \
                               within the Serums system
        Returns:
            sats (dict): A dictionary containing the definitions for \
                         the various satellites which can be made \
                         based on the a hospital's schema
            keys (list): A list of primary keys which are used to \
                         track relationships across the data vault
    """
    if hospital_id.lower() == 'ustan':
        return ustan_sats, ustan_keys
    elif hospital_id.lower() == 'fcrb':
        return fcrb_sats, fcrb_keys
    elif hospital_id.lower() == 'zmc':
        return zmc_sats, zmc_keys


def process_value(value):
    """
    Used to parse various values to make them ready for transmission.
        Parameters:
            value (Any): The value which is to be parsed
        Returns:
            value (Any): A parsed value which can be serialized into json
    """
    if isinstance(value, datetime.datetime):
        return value.strftime("%d/%m/%Y %H:%M:%S")
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, datetime.time):
        return value.strftime("%H:%M:%S")
    if isinstance(value, decimal.Decimal):
        return float(value)
    return value


def process_satellites(data: dict):
    """
    Used to transform a patient's data into a structure \
    which can be added to a data vault structure. Specifically, \
    this handles the satellite construction. Essentially, it uses \
    a template to split individual tables into various smaller \
    satellites.
        Parameters:
            data (dict): The patient data which has been retrieved \
                         by the get_patient_data function defined \
                         in components.sphr.get_source_data file
        Returns:
            satellites (dict): The transformed tables which are \
                               ready to be appended to the rest \
                               of the data vault structure
    """
    results = {}
    for hospital in data:
        results[hospital] = {}
        sat_defs, keys = pick_sats_and_keys(hospital)
        for table_name in data[hospital]['data']:
            source_data = data[hospital]['data'][table_name]
            results[hospital][table_name] = {}
            results[hospital][table_name]['links'] = \
                sat_defs[table_name]['links']
            for satellite_name in sat_defs[table_name]:
                if satellite_name != 'links':
                    columns = sat_defs[table_name][satellite_name]['columns']
                    results[hospital][table_name][satellite_name] = {}
                    results[hospital][table_name][satellite_name]['hub'] = \
                        sat_defs[table_name][satellite_name]['hub']
                    results[hospital][table_name][satellite_name]['data'] = \
                        [{
                            k: process_value(row[k])
                            for k in row
                            if k in columns
                        } for row in source_data]
                    results[hospital][table_name][satellite_name]['keys'] = \
                        [{
                            k: row[k]
                            for k in row
                            if k in keys
                        } for row in source_data]
    return results
