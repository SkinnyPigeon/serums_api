def generate_boilerplate():
    """
    We use a prescriptive schema for the core hubs and links in the \
    data vault structure. As such, we can use this boilerplate \
    constructor to build the basic layout in the form of a dictionary.
        Parameters:
            None
        Returns:
            boilerplate (dict): The basic boilerplate structure for \
                                a data vault
    """
    hubs = [
        'hub_time',
        'hub_person',
        'hub_object',
        'hub_location',
        'hub_event'
    ]
    links = [
        'time_person_link',
        'time_object_link',
        'time_location_link',
        'time_event_link',
        'person_object_link',
        'person_location_link',
        'person_event_link',
        'object_location_link',
        'object_event_link',
        'location_event_link'
    ]
    boilerplate = {}
    boilerplate['hubs'] = {hub: {'id': []} for hub in hubs}
    boilerplate['links'] = {link: get_id_columns(link) for link in links}
    return boilerplate


def get_id_columns(link: str):
    """
    Used to select the corresponding selection of link keys for a given link. \
    For instance, the link table time_person_link would always have a time_id \
    column and a person_id column
        Parameters:
            link (str): The link to select the keys for
        Returns:
            link_keys (dict): A dictionary with the required key lists ready \
                              for receiving values
    """
    id_columns = {
        'time_person_link': {'id': [], 'time_id': [], 'person_id': []},
        'time_object_link': {'id': [], 'time_id': [], 'object_id': []},
        'time_location_link': {'id': [], 'time_id': [], 'location_id': []},
        'time_event_link': {'id': [], 'time_id': [], 'event_id': []},
        'person_object_link': {'id': [], 'person_id': [], 'object_id': []},
        'person_location_link': {'id': [], 'person_id': [], 'location_id': []},
        'person_event_link': {'id': [], 'person_id': [], 'event_id': []},
        'object_location_link': {'id': [], 'object_id': [], 'location_id': []},
        'object_event_link': {'id': [], 'object_id': [], 'event_id': []},
        'location_event_link': {'id': [], 'location_id': [], 'event_id': []}
    }
    return id_columns[link]


def current_hub_values(hubs: dict):
    """
    Used to calculate the current 'hub id' value. This is required \
    in order to maintain the relationship between the various tables \
    within the data vault structure
        Parameters:
            hubs (dict): The current hubs. These are originally created \
                         in the boilerplate function and are continually \
                         updated as the process loops through the \
                         various source tables
        Returns:
            hub_values (dict): Contains the current length of the various \
                               hubs which enables the 'hub id' to be \
                               incremented as new rows are added
    """
    hub_values = {}
    for hub in hubs:
        hub_values[hub] = len(hubs[hub]['id'])
    return hub_values


def create_data_vault(sats: dict):
    """
    Used to create and fill the data vault with the data selected by \
    the standard get_patient_data function defined in components.sphr.\
    get_source_data file. This data is first processed via the satellites \
    functions before it can be married to the rest of the data vault \
    construction here.

        Parameters:
            sats (dict): The preprocessed patient data which is ready \
                         to be married to the rest of the data vault \
                         structure
        Returns:
            data_vault (dict): A dictionary which holds the relations \
                               for the smart patient health record in \
                               a data vault structure
    """

    dv = generate_boilerplate()
    results = {}
    results['satellites'] = {}
    results['hubs'] = {}
    results['links'] = {}
    for hospital in sats:
        for table in sats[hospital]:
            satellite_definitions = sats[hospital][table]
            links = sats[hospital][table]['links']
            hub_values = current_hub_values(dv['hubs'])
            for sat_name in satellite_definitions:
                if sat_name != 'links':
                    hub = satellite_definitions[sat_name]['hub']
                    keys = satellite_definitions[sat_name]['keys']
                    hub_class = hub.split('_')[1] + '_id'
                    next_hub_val = hub_values[hub] + 1
                    for i, row in enumerate(
                            satellite_definitions[sat_name]['data']):
                        for key in keys[i]:
                            # Inserting the business keys and their values
                            try:
                                while len(dv['hubs'][hub][key]) < \
                                        len(dv['hubs'][hub]['id']):
                                    dv['hubs'][hub][key].append(None)

                                dv['hubs'][hub][key].\
                                    append(keys[i][key])
                            except KeyError:
                                dv['hubs'][hub][key] = []
                                while len(dv['hubs'][hub][key]) < \
                                        len(dv['hubs'][hub]['id']):
                                    dv['hubs'][hub][key].append(None)
                                dv['hubs'][hub][key].\
                                    append(keys[i][key])

                            for link in links:
                                if hub_class in dv['links'][link]:
                                    if next_hub_val not in \
                                            dv['links'][link][hub_class]:
                                        dv['links'][link][hub_class].\
                                            append(next_hub_val)

                        row.update({f'{hub}_id': next_hub_val})
                        dv['hubs'][hub]['id'].append(next_hub_val)
                        next_hub_val = next_hub_val + 1

                    results['satellites'][f'{hospital.lower()}_{sat_name}'] = \
                        satellite_definitions[sat_name]['data']
    results['hubs'] = dv['hubs']
    results['links'] = dv['links']
    return results
