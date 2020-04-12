import datetime
import logging
import time
import pytz

from cumulusci.robotframework.utils import selenium_retry,capture_screenshot_on_error
from locators import sal_lex_locators,modal_locators
from locators import appt_manager_locators
from locators import community_home_locators
from locators import appointment_locators
from locators import community_launchpad_locators
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys
from cumulusci.robotframework.locators_48 import lex_locators

@selenium_retry
class SAL(object):

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = 1.0

    def __init__(self, debug=False):
        self.debug = debug
        self.current_page = None
        self._session_records = []
        # Turn off info logging of all http requests
        logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(
            logging.WARN
        )

    @property
    def builtin(self):
        return BuiltIn()

    @property
    def cumulusci(self):
        return self.builtin.get_library_instance("cumulusci.robotframework.CumulusCI")

    @property
    def pageobjects(self):
        return self.builtin.get_library_instance("cumulusci.robotframework.PageObjects")

    @property
    def salesforce(self):
        return self.builtin.get_library_instance('cumulusci.robotframework.Salesforce')

    @property
    def selenium(self):
        return self.builtin.get_library_instance("SeleniumLibrary")

    def _check_if_element_exists(self, xpath):
        """ Checks if the given xpath exists
            this is only a helper function being called from other keywords
        """
        elements = int(self.selenium.get_element_count(xpath))
        return True if elements > 0 else False

    def _get_namespace_prefix(self, name):
        """ This is a helper function to capture the SAL namespace prefix of the target org """
        parts = name.split('__')
        if parts[-1] == 'c':
            parts = parts[:-1]
        if len(parts) > 1:
            return parts[0] + '__'
        else:
            return ''

    @capture_screenshot_on_error
    def click_related_item_link_record(self, heading, title):
        """ Clicks a link in the related list with the specified heading. """
        #This is same function as click_related_item_link function in Salesforce.py file just with a slight modification 
        # to click on the related item link in the SAL project, as the function `load_related_list` in the Salesforce file was not working for SAL tests
        self.builtin.log("loading related list...", "DEBUG")
        locator = sal_lex_locators["rel_link"].format(heading, title)
        self.builtin.log("clicking...", "DEBUG")
        self.salesforce._jsclick(locator)
        self.builtin.log("waiting...", "DEBUG")
        self.salesforce.wait_until_loading_is_complete()

    def click_save_button_and_verify_toast_message(self, toast_message):

        """ Click on the save button to save the changes
            and verify that the toast message matches the provided argument 'toast_message'
        """
        locator = sal_lex_locators["save"]
        self.selenium.wait_until_page_contains_element(locator)
        self.selenium.wait_until_element_is_enabled(locator, error="Save button is not enabled/visible",timeout=60)
        self.selenium.set_focus_to_element(locator)
        element = self.selenium.get_webelement(locator)
        self.selenium.driver.execute_script("arguments[0].click()", element)
        time.sleep(2)
        self.selenium.capture_page_screenshot()
        self.verify_toast_message(toast_message)

    def close_all_tabs(self):
        """ Gets the count of the tabs that are open and closes them all """
        locator = sal_lex_locators["close_tab"]
        count = int(self.selenium.get_element_count(locator))
        for i in range(count):
            self.selenium.wait_until_element_is_visible(locator)
            self.selenium.get_webelement(locator).click()

    def close_deleted_notes_window(self):
        """ Closes the modal,No IsReadOnly exists in 'ContentDocument' which appears after deleting the notes """
        #Salesforce delete Notes by id leaves the notes window open after verifying notes test suite,which affects consecutive test suites like reschedule_advising,tcns_edit_appointment
        #Since this modal appears while clicking on SAL advisor link placed it in SAL.py file.
        modal_locator = modal_locators["delete_notes_modal"]["close"]
        if self._check_if_element_exists(modal_locator):
            self.builtin.log("Notes Modal Exists")
            self.selenium.click_element(modal_locator)
            self.selenium.capture_page_screenshot()
            self.close_all_tabs()
            self.builtin.log("Tab Closed")
        self.close_all_tabs()

    def close_toast_message(self,value):
        """ Closes the toast message by clicking on the close button in the toast window,
            needs to have a locator value passed in
        """
        locator = sal_lex_locators[value].format(value)
        if self._check_if_element_exists(locator):
            self.selenium.click_element(locator)
        self.selenium.capture_page_screenshot()

    def convert_time_to_UTC_timezone(self, my_time):
        """ Converts the given datetime to UTC timezone
            my_time should be in the format %Y-%m-%d %H:%M:%S
        """
        my_time_format = datetime.datetime.strptime(my_time, "%Y-%m-%d %H:%M:%S.%f")
        my_time_local = pytz.timezone("America/Los_Angeles").localize(my_time_format, is_dst=None)

        my_time_utc = my_time_local.astimezone(pytz.utc)
        return datetime.datetime.strftime(my_time_utc, "%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    def get_next_monday(self):
        """This function helps find the next monday. This is required as the appointments can be scheduled only between Monday-Thursday.Currently, community
        Page does not have an option like First available as in New appointment modal that appears in the Appointment Manager"""
        today = datetime.datetime.today()
        coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
        self.builtin.log("Coming Monday:{}".format(coming_monday))
        day_of_week = today.strftime("%A")
        next_day = today + datetime.timedelta(days=1)
        days_exception =['Thursday','Friday','Saturday']
        if day_of_week in days_exception:
            find_monday = coming_monday - today
            split_str= (str(find_monday).split())
            no_of_days = (split_str[0])
            latest_monday = today+ datetime.timedelta(days=int(no_of_days))
            return latest_monday
        else:
            return next_day

    def format_all(self, loc, value):
        """ Formats the given locator with the value for all {} occurrences """
        count = loc.count('{')

        if count == 1:
            return loc.format(value)
        elif count == 2:
            return loc.format(value, value)
        elif count == 3:
            return loc.format(value, value, value)

    def get_sal_locator(self, path, *args, **kwargs):
        """ Returns a rendered locator string from the sal_lex_locators
            dictionary. This can be useful if you want to use an element in
            a different way than the built in keywords allow.
        """
        locator = sal_lex_locators
        for key in path.split('.'):
            locator = locator[key]
        main_loc = locator.format(*args, **kwargs)
        return main_loc

    def get_sal_namespace_prefix(self):
        """ Returns the SAL namespace value if the target org is a managed org else returns blank value """
        if not hasattr(self.cumulusci, '_describe_result'):
            self.cumulusci._describe_result = self.cumulusci.sf.describe()
        objects = self.cumulusci._describe_result['sobjects']
        level_object = [o for o in objects if o['label'] == 'Advising Pool'][0]
        return self._get_namespace_prefix(level_object['name'])

    def get_timezone(self):
        from time import gmtime, strftime
        import time
        gmt_tz= strftime("%Z", gmtime())
        print(time.tzname)
        return list(time.tzname)
    
    def set_timezone_based_on_user(self):
        user_timezone = self.get_timezone()
        timezone_list =['EST', 'EDT']
        for tz in user_timezone:
            if tz in timezone_list:
                user_timezone_locale = 'America/New_York'
                return user_timezone_locale
        else:
            user_timezone_locale = 'America/Los_Angeles'
            return user_timezone_locale

    def go_to_community_menu(self, value):
        """ Navigates to the given menu item in community
            :param value is the name of the tab
        """
        locator = community_home_locators["menu_item"].format(value)
        self.selenium.page_should_contain_element(
            locator,
            message="'" + value + "' menu item with locator '" + locator + "' is not available on the page")
        self.selenium.click_element(locator)

    def go_to_tab(self, value):
        """ Navigates to the given tab name in salesforce so it can log into community 
            :param value can be custom objects contact name/Walk-In/Appointment of the tab
        """
        locator = sal_lex_locators["tabs"]["tab"].format(value)
        self.selenium.page_should_contain_element(
            locator,
            message=f"'{value}' contact tab with locator '{locator}' is not available on the page")
        self.selenium.click_element(locator)

    def go_to_sal_home(self):
        """ Navigates to the Home view of the SAL app """
        url = self.cumulusci.org.lightning_base_url
        url = "{}/lightning/page/home".format(url)
        self.selenium.go_to(url)
        self.salesforce.wait_until_loading_is_complete()

    @capture_screenshot_on_error
    def login_as_devtest_advisor_user(self,value):
        """This function helps to login as different user in salesforce"""
        locator = sal_lex_locators["users"]["login"].format(value)
        self.selenium.wait_until_page_contains_element(locator)
        xpath_locator = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.driver.execute_script("arguments[0].click()", xpath_locator)

    def verify_login_details(self,user):
        login_user_locator = sal_lex_locators["users"]["login_user_detail"].format("Logged in as "+user)
        self.selenium.wait_until_page_contains_element(login_user_locator,error=f"unable to locate '{login_user_locator}'")

    def logout_as_devtest_advisor_user(self,user):
        """This function helps to logout a logged in user in salesforce"""
        logout_user_locator = sal_lex_locators["users"]["logout_user_detail"].format("Log out as "+user)
        self.selenium.wait_until_page_contains_element(logout_user_locator)
        locator = sal_lex_locators["users"]["logout"]
        self.selenium.wait_until_page_contains_element(locator)
        self.selenium.click_element(locator)

    def open_appointment_manager(self):
        """ Checks if the appointment manager window is available and clicks to open it
            and then loads the appointment manager page object
        """
        locator_window = appt_manager_locators["window"]
        self.selenium.page_should_contain_element(locator_window,
                                                  message="Appointment Manager dock is not available on the page")

        locator_docked = appt_manager_locators["docked"]
        if self.selenium.get_element_count(locator_docked) == 0:
            self.selenium.click_element(locator_window)
            time.sleep(1)
            # self.selenium.select_window()

        self.selenium.page_should_contain_element(locator_docked, message="Appointment Manager dock is not open")
        self.pageobjects.load_page_object("Popup", "ApptManager")
        #Adding this to see if there are any existing appointments in the appointment manager.
        #Sometimes while creating an One off appointment seeing the following error `Your requested Appointment is no longer available`
        self.selenium.capture_page_screenshot()

    def populate_placeholder(self, loc, value):
        """ Populates placeholder element with a value
            Finds the placeholder element, inputs value
            and waits for the suggestion and clicks on it
        """
        xpath_lookup = sal_lex_locators["input_placeholder"].format(loc)
        field = self.selenium.get_webelement(xpath_lookup)
        self.selenium.driver.execute_script("arguments[0].click()", field)
        field.send_keys(value)
        time.sleep(2)
        field.send_keys(Keys.ENTER)
        xpath_value = self.select_xpath("placeholder_lookup", value)
        self.selenium.click_element(xpath_value)

    def populate_placeholder_users(self, loc, value):
        """ Populates placeholder element with a value
            Finds the placeholder element, inputs value
            and waits for the suggestion and clicks on it
        """
        xpath_lookup = sal_lex_locators["input_placeholder"].format(loc)
        field = self.selenium.get_webelement(xpath_lookup)
        field.click()
        field.send_keys(value)
        time.sleep(2)
        field.send_keys(Keys.ENTER)
        xpath_value = sal_lex_locators["users"]["user"].format(value)
        element_menu = self.selenium.driver.find_element_by_xpath(xpath_value)
        self.selenium.wait_until_page_contains_element(xpath_value)
        self.selenium.click_element(element_menu)
        self.selenium.wait_until_location_contains("/lightning/setup/ManageUsers/home")

    def print_package_details(self):
        """ Captures all the package names and versions from SAL setup and prints them """
        package_name = sal_lex_locators["package"]["name"]
        package_version = sal_lex_locators["package"]["version"]

        name = self.selenium.get_text(package_name.format(2))
        version = self.selenium.get_text(package_version.format(2))
        self.builtin.log_to_console("\n******** Package Name/Version: " + name + "/" + version + " ********")

        if self._check_if_element_exists(package_name.format(3)):
            name = self.selenium.get_text(package_name.format(3))
            version = self.selenium.get_text(package_version.format(3))
            self.builtin.log_to_console("******** Package Name/Version: " + name + "/" + version + " ********\n")

    @capture_screenshot_on_error
    def select_app_launcher(self, app_name):
        """ Navigates to a Salesforce App via the App Launcher
            Locator got updated with Summer'19
            hence keyword is created specific to SAL (temporarily)
        """
        locator = sal_lex_locators["app_launcher"]["app_link"].format(app_name)
        self.builtin.log("Opening the App Launcher")
        self.salesforce.open_app_launcher()
        time.sleep(5)
        self.builtin.log("Getting the web element for the app")
        self.selenium.set_focus_to_element(locator)
        elem = self.selenium.get_webelement(locator)
        self.builtin.log("Getting the parent link from the web element")
        link = elem.find_element_by_xpath("../../..")
        self.selenium.set_focus_to_element(link)
        self.builtin.log("Clicking the link")
        link.click()
        self.close_deleted_notes_window()
        self.builtin.log("Waiting for modal to close")
        self.salesforce.wait_until_modal_is_closed()
        self.selenium.driver.refresh()
        self.selenium.capture_page_screenshot()

    def select_frame_with_value(self, value):
        """ Selects frame identified by the given value
            value should be the 'id', 'title' or 'name' attribute value of the webelement used to identify the frame
        """
        locator = sal_lex_locators["frame"]
        locator = self.format_all(locator, value)
        self.selenium.select_frame(locator)

    def select_navigation_tab(self, tab):
        """ Selects navigation tab - as passed in to the function """
        locator_menu = sal_lex_locators["navigation_menu"]
        element_menu = self.selenium.driver.find_element_by_xpath(locator_menu)
        locator_tab = sal_lex_locators["navigation_tab"].format(tab)

        self.selenium.wait_until_page_contains_element(
            locator_menu,
            error="Navigation menu drop down unavailable"
        )
        # javascript is being used here because the usual selenium click is highly unstable for this element on MetaCI
        self.selenium.driver.execute_script("arguments[0].click()", element_menu)
        time.sleep(1)

        # Sometimes, single click fails. Hence an additional condition to click on it again
        if not self._check_if_element_exists(locator_tab):
            self.selenium.driver.execute_script("arguments[0].click()", element_menu)
            time.sleep(1)

        self.selenium.wait_until_page_contains_element(
            locator_tab,
            error=tab + " item not found as an available option in: " + locator_tab
        )
        self.selenium.click_element(locator_tab)

    def select_tab_on_record_page(self, title):
        """ Switch between different tabs on a record page like Related, Details, News, Activity and Chatter
            :param title: name of the tab visible on the page
        """
        locator = sal_lex_locators["record_tab"].format(title)
        self.selenium.wait_until_page_contains_element(locator, error="Tab '" + title + "' isn't available on the page")
        self.selenium.get_webelement(locator).click()

    def select_value_from_listbox(self, title, value):
        """ Selects value from a listbox/dropdown identified by title """
        locator_title = sal_lex_locators["listbox"]["title"].format(title)
        locator_value = sal_lex_locators["listbox"]["value"].format(value)
        self.selenium.click_element(locator_title)
        time.sleep(1)
        self.selenium.click_element(locator_value)

    def select_xpath(self, loc, value):
        """ Selects the correct xpath by checking if it exists on the page
            from the given list of locator possibilities
        """
        locators = sal_lex_locators[loc].values()
        for i in locators:
            locator = self.format_all(i, value)
            if self._check_if_element_exists(locator):
                return locator

        assert "Button with the provided locator not found"

    @capture_screenshot_on_error
    def verify_toast_message(self, value):
        """ Verifies the toast message """
        locator = sal_lex_locators["toast_message"].format(value)
        self.selenium.wait_until_element_is_visible(locator)
        close_locator = sal_lex_locators["toast_close"]
        self.selenium.wait_until_page_contains_element(close_locator)
        self.selenium.click_element(close_locator)

    def wait_for_new_window(self, title):
        """ Waits for specified window to be available
            by checking every 1 seconds for 25 times
        """
        window_found = False

        for i in range(25):
            i += 1
            time.sleep(1)
            titles = self.selenium.get_window_titles()
            for j in titles:
                if j == title:
                    window_found = True
                    return window_found

            if window_found:
                return
            else:
                continue

        self.builtin.log("Timed out waiting for window with title " + title)
        return window_found

    def check_field_value_pair_is_disabled(self, field, value):
        """ Verify the given field-value pair is disabled on the new appointment page when creating a follow up appointment """
        locator = appointment_locators["edit_appointment"]["disabled_field"].format(field, value)
        self.selenium.wait_until_page_contains_element(
            locator,
            error="Disabled field '" + field + "' with value '" + value + "' is not available on the page"
        )