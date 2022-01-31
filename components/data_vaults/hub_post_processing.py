def hub_equalizer(hubs: dict):
    """
    Used to fill all hubs to the same level. This ensures the data \
    is ready to be inserted into a database or DataFrame
        Parameters:
            hubs (dict): The hubs to be equalized
        Returns:
            None
    """
    for hub_name in hubs:
        hub = hubs[hub_name]
        max_key = max(hub, key=lambda x: len(set(hub[x])))
        for key in hub:
            while len(hub[key]) < len(hub[max_key]):
                hub[key].append(None)
