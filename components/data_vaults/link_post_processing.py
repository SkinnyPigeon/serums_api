def add_id_values(links: dict):
    """
    Used to fill all links to the same level. This ensures the data \
    is ready to be inserted into a database or DataFrame
        Parameters:
            links (dict): The links to be equalized
        Returns:
            None
    """
    for link_name in links:
        link = links[link_name]
        max_key = max(link, key=lambda x: len(set(link[x])))
        for i, _ in enumerate(link[max_key]):
            link['id'].append(i + 1)
