from bot import utils as bot_utils

LEAVES_TYPE_INDEX = {
    'Leaves': 0,
    'Half Days': 1,
    'RH': 2,
    'WFH': 3,
    'BL/ML/PL': 4
}
INTENT_RESPONSE_MAPPING = {
    'Contact_Request_Get_By_Name': bot_utils.get_contact_info_by_name,
    'Vacation_Query_Available': bot_utils.get_official_leaves,
    'Vacation_Query_Remaining': bot_utils.get_remaining_leaves_of_user,
    'Vacation_Query_Team_Status': bot_utils.get_team_status,
    'Vacation_Apply': bot_utils.apply_vacation,
    'Vacation_Query_Person_Status': bot_utils.get_user_availability,
    'default': lambda **kwargs: kwargs.get('response_text', '')
}
