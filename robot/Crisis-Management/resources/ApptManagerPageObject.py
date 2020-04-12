import time

from cumulusci.robotframework.pageobjects import BasePage
from cumulusci.robotframework.pageobjects import pageobject
from robot.libraries.BuiltIn import BuiltIn
from locators import appt_manager_locators
from locators import appointment_locators
from cumulusci.robotframework.utils import selenium_retry,capture_screenshot_on_error



@pageobject("Popup", "ApptManager")
class ApptManagerHomePage(BasePage):
    object_name = None

    @property
    def builtin(self):
        return BuiltIn()

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')

    def click_action_button(self):
        """ Clicks on the 'Action' button in Appointment Manager """
        locator = appt_manager_locators["action"]
        locator_close_action = appt_manager_locators["action_close"]

        # In some cases, the action dialog opens by default,
        # hence making sure it is closed, before opening it otherwise it would nullify the click command
        if self.sal._check_if_element_exists(locator_close_action):
            self.selenium.click_element(locator_close_action)

        self.selenium.wait_until_page_contains_element(
            locator,
            error="'Action' button is not available on the appointment manager"
        )
        self.selenium.click_element(locator)

    def click_action_close_button(self):
        """ Clicks on the 'Action Shortcut Close' button in Appointment Manager """
        locator_close_action = appt_manager_locators["action_close"]
        if self.sal._check_if_element_exists(locator_close_action):
            self.selenium.click_element(locator_close_action)

    def click_availability_settings_button(self):
        """ Click on the 'Availability Settings' button on appointment manager """
        locator = appt_manager_locators["availability_settings"]
        self.salesforce._jsclick(locator)

        # This sleep statement is required else we are receiving a pop up(core bug) and the remaining steps fail. This pop up doesnot appear when clicking on the availability 
        # settings gear manually. 
        time.sleep(5)
        
    def click_new_appointment_button(self):
        """ Clicks on the 'New Appointment' button on appointment manager """
        locator = appt_manager_locators["new_appointment_button"]
        element = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.wait_until_page_contains_element(locator)
        self.selenium.driver.execute_script("arguments[0].click()", element)

    def click_new_walkin_button(self):
        """ Clicks on the 'New Walkin' button on appointment manager """
        locator = appt_manager_locators["new_walkin_button"]
        element = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.wait_until_page_contains_element(locator)
        self.selenium.driver.execute_script("arguments[0].click()", element)

    def get_last_appointment(self,value):
        """This provides information of the last ended appoinment date when End appointment action is performed"""
        
        locator_close_action = appt_manager_locators["action_close"]
        # Making sure the action shortcut menu closes before the tests would look for the last appointment
        if not self.sal._check_if_element_exists(locator_close_action):
            locator = appt_manager_locators["last_appointment"].format(value)

            self.selenium.page_should_contain_element(
                locator,
                message="Last Appointment information locator " + locator + "with value " + value +" is not available on appointment manager"
            )


    def minimize_appointment_manager(self):
        """ Minimize the appointment manager """
        locator = appt_manager_locators["minimize"]
        self.selenium.page_should_contain_element(
            locator,
            message="Minimize button with locator " + locator + " is not available on appointment manager"
        )
        self.selenium.click_element(locator)

    def refresh_appointment_manager(self):
        """ Refresh the appointment manager by clicking on the refresh button
            in the appointment manager popup
        """
        locator = appt_manager_locators["refresh"]
        self.selenium.click_element(locator)
        # It takes a while for the updated status to appear even after clicking on the refresh button 
        time.sleep(2)
    
    def identify_locators_based_on_appointments(self,locator_appointment):
        """ Returns a locator specific to an appointment
        In the Spring 20 release, the locators are different for different appointments, 
        so this helps determine the locator based on the appointment type (advising/nonadvising)
        """
        appt_locator_length= len(locator_appointment)
        appt_locator_type = locator_appointment[46:appt_locator_length-3]
        if appt_locator_type == 'advising':
            locator = appt_manager_locators["appointment_type"][appt_locator_type]
            return locator
        else:
            locator = appt_manager_locators["appointment_type"][appt_locator_type]
            return locator

    def _locate_appointment_by_description(self, locator_appointment, description):
        """ Returns true if an appointment of type with the given description is available
            this is only a helper function being called from select_appointment_by_description keyword
            :param locator_appointment: locator to get all appointments on the current page of Appointment manager
            :param description: description to uniquely identify an appointment
        """
        locator_description = self.identify_locators_based_on_appointments(locator_appointment)
        appt_format = locator_description.format("Description", description)
        self.builtin.log(f"description appt_format {appt_format}")
        elements = self.selenium.get_webelements(locator_appointment)
        if len(elements) == 0:
            return False
        else:
            for element in elements:
                self.selenium.wait_until_page_contains_element(element)
                self.selenium.driver.execute_script("arguments[0].click()", element)
                time.sleep(1)
                self.view_record()
                if self.sal._check_if_element_exists(appt_format) :
                    self.sal.close_all_tabs()
                    self.sal.open_appointment_manager()
                    self.click_action_close_button()
                    return True
                self.sal.close_all_tabs()
                self.sal.open_appointment_manager()

        return False

    def description_select(self,description):
        if description == '':
            locator_description = appointment_locators["blank_description"].format("Description")
            self.builtin.log("locator description {}".format(locator_description))
            return locator_description
        else:
            locator_description = appointment_locators["field_value"].format("Description", description)
            self.builtin.log("locator description {}".format(locator_description))
            return locator_description

    def select_action(self, action):
        """ Select the given action from the list of Actions list on appointment manager """
        locator = appt_manager_locators["action_shortcut"].format(action)
        self.selenium.wait_until_page_contains_element(
            locator,
            error="Action '" + action + "' doesn't exist in the list of Action Shortcuts"
        )
        self.selenium.click_element(locator)
    
    def tomorrow_locator_clickable_check(self):
        """ Verifies whether the tomorrow appointment locator is clickable. 
        If not clickable then click on up_next locator button"""
        
        locator_tomorrow = appt_manager_locators["tomorrows_appointments"]
        locator_up_next = appt_manager_locators["up_next"]
        self.selenium.wait_until_page_contains_element(
            locator_tomorrow,
            error="Locator '" + locator_tomorrow + "' doesn't exist in the list of Appointment Manager"
        )
        if not self.selenium.click_element(locator_tomorrow) is True:
            self.selenium.click_element(locator_up_next)
            
    @capture_screenshot_on_error
    def select_appointment_by_description(self, appointment_type, description, page):
        """ Select the right appointment using the appointment_type and unique description
            if page is 'all', it looks for the appointment for the next 4 days
            if page is 'current', it only looks in today's appointments
        """
        locator_appointment = appt_manager_locators[appointment_type]
        appointment_found = self._locate_appointment_by_description(locator_appointment, description)
        print("Appt Found Value {}".format(appointment_found))
        if appointment_found is not True and page == "all":
            for i in range(5):
                self.tomorrow_locator_clickable_check()
                self.refresh_appointment_manager()
                appointment_found = self._locate_appointment_by_description(locator_appointment, description)
                print("Appointment Result {}".format(appointment_found))
                if appointment_found:
                    return
        assert appointment_found, appointment_type + " with description '" + description + "' not found."

    def verify_appt_does_not_exist_on_appt_manager(self, appointment_type, description, page):
        """ Verify that the appointment with given appointment_type and unique description
            does NOT exist on Appointment Manager
            if page is 'all', it looks for the appointment for the next 4 days
            if page is 'current', it only looks in today's appointments
        """
        locator_appointment = appt_manager_locators[appointment_type]
        locator_tomorrow = appt_manager_locators["tomorrows_appointments"]
        self.refresh_appointment_manager()
        appointment_found = self._locate_appointment_by_description(locator_appointment, description)
        if appointment_found is True:
            raise AssertionError("Appointment with description {} is found on Appt Manager. Expected: Not to be found"
                                 .format(description))
        elif appointment_found is False and page == "all":
            for i in range(10):
                self.selenium.wait_until_page_contains_element(locator_tomorrow)
                self.selenium.click_element(locator_tomorrow)
                appointment_found = self._locate_appointment_by_description(locator_appointment, description)
                if appointment_found:
                    raise AssertionError(
                        "Appointment with description {} is found on Appt Manager. Expected: Not to be found"
                        .format(description))

        self.builtin.log("Appointment with description {} is not found on Appt Manager as expected".format(description))

    @capture_screenshot_on_error
    def verify_current_appointment_status(self, status):
        """ Verify current appointment status is given 'status' on appointment manager """
        locator = appt_manager_locators["status"].format(status)
        self.refresh_appointment_manager()
        self.selenium.page_should_contain_element(
            locator,
            message="Current appointment status is not '" + status + "' as expected"
        )

    def verify_given_action_is_not_available(self, action):
        """ Verify given action is not available in the list of action options in appointment manager """
        locator = appt_manager_locators["action_shortcut"].format(action)
        self.selenium.page_should_not_contain_element(
            locator,
            message="Action '" + action + "' is available. Expected: Action should not be available"
        )

    def verify_given_action_is_disabled(self, action):
        """ Verify given action is disabled in the list of action options in appointment manager """
        locator = appt_manager_locators["disabled_action"].format(action)
        self.selenium.page_should_contain_element(locator,
                                                  message="Action '" + action + "' is not disabled as expected")

    def verify_given_action_is_enabled(self, action):
        """ Verify given action is enabled in the list of action options in appointment manager """
        locator_action = appt_manager_locators["action_shortcut"].format(action)
        locator_disabled = appt_manager_locators["disabled_action"].format(action)
        self.selenium.page_should_contain_element(
            locator_action,
            message="Action '" + action + "' doesn't exist in the list of enabled Action Shortcuts"
        )
        self.selenium.page_should_not_contain_element(locator_disabled,
                                                      message="Action '" + action + "' is not enabled as expected")

    def verify_time_of_selected_appointment(self, start_time, end_time):
        """ Verify the start and end time of the selected appointment
            start_time and end_time format is HH:MM AM
        """
        locator = appt_manager_locators["selected_time"].format(start_time, end_time)
        self.selenium.page_should_contain_element(
            locator,
            message="The time of the selected appointment is not '" + start_time + "' to '" + end_time + "'"
        )

    def verify_timezone(self):
        """ Verify that a timezone value exists
            there is currently an open bug on this,
            once fixed, the keyword needs to be modified to check for a specific timezone
        """
        locator = appt_manager_locators["timezone"]
        self.selenium.page_should_contain_element(locator)
        self.builtin.log("Actual timezone isn't checked; waiting for bug to be fixed", "WARN")

    def view_actions(self):
        """ Click on the 'Actions' button for the selected appointment in appointment manager """
        locator = appt_manager_locators["action"]
        locator_close_action = appt_manager_locators["action_close"]

        # In some cases, the action dialog opens by default,
        # hence making sure it is closed, before opening it otherwise it would nullify the click command
        if self.sal._check_if_element_exists(locator_close_action):
            self.selenium.click_element(locator_close_action)

        self.selenium.wait_until_page_contains_element(
            locator,
            error="'Action' button is not available on the appointment manager"
        )
        self.selenium.click_element(locator)

    def view_advisee(self,contact_id):
        """ Click on view_advisee button on appointment manager """
        locator = appt_manager_locators["view_advisee"]
        self.selenium.wait_until_page_contains_element(locator)
        self.selenium.click_element(locator)
        self.selenium.wait_until_location_contains("/lightning/r/Case/"+contact_id+"/view")

    def view_record(self):
        """ Click on view_record button on appointment manager """
        locator = appt_manager_locators["view_record"]
        element = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.wait_until_page_contains_element(locator)
        self.selenium.driver.execute_script("arguments[0].click()", element)
        self.salesforce.wait_until_loading_is_complete()
        self.selenium.capture_page_screenshot()

    def verify_location_of_selected_appointment(self,location):
        """Verifies that the correct location is displaying for an appointment in appointment manager"""
        locator = appt_manager_locators["selected_location"].format(location)
        self.selenium.page_should_contain_element(
            locator,
            message="The location of the selected appointment is not " + location
        )