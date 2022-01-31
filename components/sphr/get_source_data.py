from control_files.tags import ustan_tags


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