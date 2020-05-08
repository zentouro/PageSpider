from requests import get
from requests.exceptions import RequestException
from contextlib import closing


#########################################################################################
# Copied/pasted from https://realpython.com/python-web-scraping-practical-introduction  #
# Forked from https://github.com/armish/bioRxiv-list                                    #
#########################################################################################


def simple_get(urls: object) -> object:
    """
    Attempts to get the content at `urls` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(urls, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
                print('got one')
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(urls, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)



