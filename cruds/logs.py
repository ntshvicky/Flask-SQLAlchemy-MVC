
# Import necessary modules
import logging
from helpers.db_helper import SessionLocal
from helpers.extra_helpers import getIPDetails

from sqlalchemy import or_
from sqlalchemy import asc, desc 

from dotenv import load_dotenv
load_dotenv()

from models.db_model import Logs

# save log
def saveChangeLog(
        user_id: str,
        action: str,
        ip_address: str,
        request_header: dict,
        browser: str,
        platform: str,
        mobile: str,
        referer: str,
        called_api: str,
        emp_id: str,
        req_data: str
):
    session = SessionLocal()
    try:
        gloc = getIPDetails(ip_address)
        obj = Logs(
            user_id = user_id,
            action = action,
            ip_address = ip_address,
            req_header = request_header,
            browser = browser,
            platform = platform,
            referer = referer,
            mobile = mobile,
            city = None if 'geoplugin_city' not in gloc else gloc['geoplugin_city'],
            country = None if 'geoplugin_countryName' not in gloc else gloc['geoplugin_countryName'],
            region = None if 'geoplugin_continentName' not in gloc else gloc['geoplugin_continentName'],
            latitude = None if 'geoplugin_latitude' not in gloc else gloc['geoplugin_latitude'],
            longitude = None if 'geoplugin_longitude' not in gloc else gloc['geoplugin_longitude'],
            timezone = None if 'geoplugin_timezone' not in gloc else gloc['geoplugin_timezone'],
            called_api = called_api,
            emp_id = emp_id,
            req_data = req_data
        )
        session.add(obj)
        session.commit()
        return obj.id
    except Exception as e:
        session.rollback()
        logging.error(f"Integrity Error: {e}")
        return None



# example of list all logs
def list_logs(offset: int = 0, limit: int = 10, order_by: str = None, order_direction: str = None, search_term: str = None):
    session = SessionLocal()

    p_res = session.query(Logs)

    if search_term:
        like_filter = or_(Logs.action.like(f'%{search_term}%'), Logs.called_api.like(f'%{search_term}%'))
        p_res = p_res.filter(like_filter)

    total_count = p_res.count()

    if order_direction == 'asc':
        p_res = p_res.order_by(asc(order_by))
    else:
        p_res = p_res.order_by(desc(order_by))

    p_res = p_res.offset(offset).limit(limit)
    p_res = p_res.all()
    return total_count, p_res
