from control_files.tags.ustan import ustan_tags


def tag_picker(hospital_id: str):
    """
    Returns a lowercased hospital id and tag definitions.
        Parameters:
            hospital_id (str): The internal reference for the hospitals \
                               within the Serums system
        Returns:
            hospital_tags (list): A list of tag definitions. These are \
                                  designed by the hospitals to subset \
                                  their data in ways that the patients can \
                                  intuitively understand when they create \
                                  rules. These definitions show:\n
            - The source table that holds the data
            - The columns within the source table that are governed by the tag
    """
    if hospital_id == 'ustan':
        return ustan_tags


def select_tags(tags_list: list, request_tags: list):
    """
    Selects the relevant tag definition(s) based on \
    the valid tags for a request
        Parameters:
            tags_list (list): The tag definitions as selected \
                              by tag_picker()
            request_tags (list): The list of valid tags which \
                                 have been requested
        Returns:
            selected_tags (list): A list of the tag definitions that \
                                  is based on the valid tags found \
                                  in the request body
    """
    selected_tags = []
    for request_tag in request_tags:
        for tag_definition in tags_list:
            # try:
            if tag_definition['tag'] == request_tag:
                selected_tags.append(tag_definition)
            # except:
            #     pass
    return selected_tags
