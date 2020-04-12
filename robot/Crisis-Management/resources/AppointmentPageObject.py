import time
from selenium.webdriver.common.action_chains import ActionChains
from cumulusci.robotframework.pageobjects import BasePage
from cumulusci.robotframework.pageobjects import DetailPage
from cumulusci.robotframework.pageobjects import pageobject
from locators import appointment_locators
from selenium.webdriver.common.keys import Keys


@pageobject("NewAdvisingAppointment", "Appointment")
class AdvisingAppointmentNewPage(BasePage):

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')

    def _is_current_page(self):
        """ Verify we are on the New Advising/Walkin Appointment page
            by verifying that the section title is 'Basics'
        """
        locator = appointment_locators["section_title"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="Section title is not 'Basics' as expected")
    
    def _select_appointment_form_dropdown_value(self,locator,key,value):
        """Helper function which selects the values of a dropdown based on key & label"""
        self.selenium.wait_until_page_contains_element(locator)
        self.selenium.set_focus_to_element(locator)
        self.selenium.click_element(locator)
        self.selenium.wait_until_element_is_visible(
                locator,
                error=f"'{key}' drop down, '{locator}' is not available on the page")
        dropdown_menu = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.select_from_list_by_label(dropdown_menu,value)

    def click_first_available_button(self):
        """ Click on the 'First Available' button
            that selects the first available time slot for the appointment
        """
        locator = appointment_locators["advising_appointment"]["date-picker"]
        scroll_locator=self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.wait_until_page_contains_element(
            locator,
            error=f"scroll into '{locator}' is not available"
        )
        # using javascript because the selenium method 'scroll_element_into_view isn't working here
        self.selenium.driver.execute_script("arguments[0].scrollIntoView(true)", scroll_locator)
        first_available_locator = appointment_locators["advising_appointment"]["first_available"]
        self.selenium.page_should_contain_element(first_available_locator)
        self.salesforce._jsclick(first_available_locator)

    def click_one_off_appointment_button(self):
        """ Click on the 'One-off Appointment' button
            that lets the user select customized time slot for the appointment
        """
        locator = appointment_locators["advising_appointment"]["one-off_appt"]["one-off-button"]
        self.selenium.click_element(locator)

    def click_enter_clear_locator(self,locator,value):
        """Clicks on the locator in order to clear and presses enter button to move to the next locator"""
            # If the locator is not clicked on, the contents within the text box does not clear
        self.selenium.click_element(locator)
        self.selenium.clear_element_text(locator)
        self.selenium.get_webelement(locator).send_keys(value)
        self.selenium.get_webelement(locator).send_keys(Keys.ENTER)

    def get_first_available_appointment(self):
        """This keyword gets the value of the first available appointment values while scheduling an appointment"""
        time_slot = dict()
        available_date = appointment_locators["advising_appointment"]["first_available_date"]
        time_slot['available_date_value'] = self.selenium.get_webelement(available_date).text
        available_timeslots = appointment_locators["advising_appointment"]["first_available_start_end_time"]
        element = self.selenium.get_webelements(available_timeslots)
        time_slot['start_time'] = element[0].text
        time_slot['end_time'] = element[1].text
        return time_slot

    def one_off_appointment_values(self, **kwargs):
        """Enters the Date and time in the One-Off Appointment section"""
        for key, value in kwargs.items():
            if key == 'StartDate':
                locator = appointment_locators["advising_appointment"]["one-off_appt"]["start_end_date"].format(key)
                self.selenium.wait_until_page_contains_element(locator)
                self.selenium.get_webelement(locator).send_keys(value)
            elif key == 'EndDate':
                locator = appointment_locators["advising_appointment"]["one-off_appt"]["start_end_date"].format(key)
                self.selenium.execute_javascript("window.scrollBy(0, 200)")
                self.click_enter_clear_locator(locator,value)
            elif key == 'StartDateTime':
                locator = appointment_locators["advising_appointment"]["one-off_appt"]["start_end_time"].format(key)
                self.click_enter_clear_locator(locator,value)
            elif key == 'EndDateTime':
                locator = appointment_locators["advising_appointment"]["one-off_appt"]["start_end_time"].format(key)
                self.selenium.execute_javascript("window.scrollBy(0, 200)")
                self.click_enter_clear_locator(locator,value)
            
            else:
                assert False, "Key provided by name '{}' does not exist".format(key)

    def populate_advising_appointment_form(self, **kwargs):
        """ Populates advising appointment form with the field-value pairs
            The supported keys are Invitee, Duration, Location, Topic, Subtopic, and Description
        """
        for key, value in kwargs.items():
            if key == 'Invitee':
                self.sal.populate_placeholder("Search Advisees", value)
                time.sleep(1)
            elif key == 'Duration':
                locator = appointment_locators["advising_appointment"]["select_field"].format("Duration")
                self.selenium.select_from_list_by_value(locator, value)
            elif key == 'Location':
                locator = appointment_locators["advising_appointment"]["select_field"].format("Location")
                self._select_appointment_form_dropdown_value(locator,key,value)
            elif key == 'Topic':
                locator = appointment_locators["advising_appointment"]["select_field"].format("Topic")
                self._select_appointment_form_dropdown_value(locator,key,value)
            elif key == 'Subtopic':
                locator = appointment_locators["advising_appointment"]["select_field"].format("Subtopic")
                self._select_appointment_form_dropdown_value(locator,key,value)
                time.sleep(2)
            elif key == 'Description':
                locator = appointment_locators["advising_appointment"]["description"]
                self.selenium.get_webelement(locator).send_keys(value)

            else:
                assert False, "Key provided by name '{}' does not exist".format(key)
    
    def populate_followup_advising_appointment_form(self, **kwargs):
        """ Populates a follow-up advising appointment form with the field-value pairs
            The supported keys are Location, Topic, Subtopic, and Description
        """
        for key, value in kwargs.items():
            if key == 'Location':
                locator = appointment_locators["advising_appointment"]["select_field"].format("Location")
                time.sleep(1)
                self.selenium.select_from_list_by_value(locator, value)
            elif key == 'Topic':
                locator = appointment_locators["advising_appointment"]["select_field"].format("Topic")
                option_loc = appointment_locators["advising_appointment"]["topic_subtopic"].format(value)
                self.selenium.click_element(option_loc)
            elif key == 'Subtopic':
                locator = appointment_locators["advising_appointment"]["select_field"].format("Subtopic")
                option_loc = appointment_locators["advising_appointment"]["topic_subtopic"].format(value)
                self.selenium.click_element(option_loc)
            elif key == 'Description':
                locator = appointment_locators["advising_appointment"]["description"]
                self.selenium.get_webelement(locator).send_keys(value)
            else:
                assert False, "Key provided by name '{}' does not exist".format(key)

@pageobject("EditAppointment", "Appointment__c")
class EditAppointmentPage(BasePage):

    def _is_current_page(self):
        """ Verify we are on the Edit Appointment page by verifying its header title """
        locator = appointment_locators["edit_appointment"]["header_title"]
        self.selenium.wait_until_page_contains_element(
            locator,
            error="'Edit Appointment' header title is not available on the page"
        )

    def update_appointment_field_value(self, field, value):
        """ Update the field with label 'field' to the given 'value' """
        if field in ('Duration', 'Location', 'Topic', 'Subtopic'):
            locator = appointment_locators["advising_appointment"]["select_field"].format(field)
            self.selenium.select_from_list_by_value(locator, value)
        elif field == 'Description':
            locator = appointment_locators["advising_appointment"]["description"]
            self.selenium.clear_element_text(locator)
            self.selenium.get_webelement(locator).send_keys(value)
        else:
            assert False, "Field provided by name '{}' does not exist".format(field)
        self.selenium.capture_page_screenshot()

    def update_appointment_time_to(self, start_time, end_time):
        """ Update the appointment time slot to the given value
            start_time format:  HH:MI AM/PM
            end_time format:    HH:MI AM/PM PDT
        """
        locator_timeslot = appointment_locators["edit_appointment"]["appointment_timeslot"].format(start_time, end_time)
        element_timeslot = self.selenium.driver.find_element_by_xpath(locator_timeslot)

        self.selenium.wait_until_page_contains_element(
            locator_timeslot,
            error="Time slot with start time '" + start_time + "' and end time '" + end_time + "' is not available"
        )
        # using javascript because the selenium method 'scroll_element_into_view isn't working here
        self.selenium.driver.execute_script("arguments[0].scrollIntoView(true)", element_timeslot)
        self.selenium.click_element(locator_timeslot)


@pageobject("Detail", "Appointment__c")
class AppointmentDetailPage(DetailPage):
    object_name = "Appointment__c"

    @property
    def object_name(self):
        object_name = self._object_name

        # the length check is to skip objects from a different namespace
        # like foobar__otherpackageobject__c
        if object_name is not None:
            parts = object_name.split("__")
            if len(parts) == 2 and parts[-1] == "c":
                # get_sal_namespace_prefix already takes care of returning an actual
                # prefix or an empty string depending on whether the package is managed
                object_name = "{}{}".format(
                    self.sal.get_sal_namespace_prefix(), object_name
                )
        return object_name

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')

    # This can be moved to Cumulusci Detail page keywords in the future
    def header_title_should_be(self, title):
        """ Verify the header title """
        locator = appointment_locators["header_title"].format(title)
        self.selenium.wait_until_page_contains_element(locator)
        self.selenium.page_should_contain_element(locator,
                                                  message="Header title is not " + title + " as expected")
        self.selenium.capture_page_screenshot()                                          

    def case_header_title_should_be(self, title):
        """ Verify the case header title """
        locator = appointment_locators["case_header_title"].format(title)
        self.selenium.page_should_contain_element(locator,
                                                  message="Case Header title is not " + title + " as expected")                                             

    def get_duration(self, start,end):
        """This function gets the total duration when a start and a end date is provided
        There are lot of date time coversions happening in this function to support different
        date time formats in appointment manager and community Page.This also validates the 
        total duration of an scheduled appointment.
        """
        #time library is interfering with the normal time.sleep library so had to call it
        #within the function explicitly instead of calling it in the top section
        from datetime import datetime,date, timedelta,time
        date_time_info = dict()
        start_time = datetime.strptime(start,'%m/%d/%Y, %H:%M %p').time()
        date_time_info['start_time_calendar_format'] = f'{start_time.hour}:{start_time.minute}'
        date_info = datetime.strptime(start,'%m/%d/%Y, %I:%M %p')
        date_time_info['start_date'] = datetime.strftime(date_info,'%A, %B %-d, %Y')
        end_time = datetime.strptime(end,'%m/%d/%Y, %H:%M %p').time()
        date_time_info['end_time_calendar_format'] = f'{end_time.hour}:{end_time.minute}'
        date_time_info['end_day'] = datetime.strptime(end,'%m/%d/%Y, %I:%M %p').date()
        duration = datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)
        self.builtin.log(f"Duration Difference '{duration}'")
        date_time_info['total_duration'] =int((duration.total_seconds()/60))
        self.builtin.log(f"Duration Difference '{date_time_info['total_duration']}'")
        return date_time_info

    def get_appointment_date_time(self):
        """This functions returns the Start & End datetime based on the locators in the 
            Details page of appointment.
        """
        start_locator = appointment_locators["appointmnet_start_end_time"].format('Start')
        self.selenium.wait_until_page_contains_element(
            start_locator,
            error=f"Field with label, '{start_locator}' is not available on the Details page"
        )
        start= self.selenium.get_webelement(start_locator)
        start_time = start.get_attribute('innerText')
        end_locator = appointment_locators["appointmnet_start_end_time"].format('End')
        self.selenium.wait_until_page_contains_element(
            end_locator,
            error=f"Field with label, '{end_locator}' is not available on the Details page"
        )
        end= self.selenium.get_webelement(end_locator)
        end_time = end.get_attribute('innerText')
        return start_time,end_time

    def verify_appointment_duration(self,duration):
        """ Verifies the total appointment duration"""
        start_end_time = self.get_appointment_date_time()
        start_time =  start_end_time[0]
        end_time = start_end_time[1]
        duration_difference = self.get_duration(start_time,end_time)
        if duration_difference['total_duration'] == int(duration):
            self.builtin.log(f"Total Duration '{duration_difference['total_duration']}'")
            return
        else:
            raise AssertionError(f"Appointment duration '{duration_difference['total_duration']}' does not match with the preset appointment length '{duration}'.Expected: Duration should match")

    def verify_field_value_exists(self, title, value):
        """ Verify that the field with label 'title' has its value as 'value' """
        locator = appointment_locators["field_value"].format(title, value)
        self.selenium.page_should_contain_element(
            locator,
            message="Field=" + title + " and value=" + value + " is not available on the page"
        )
