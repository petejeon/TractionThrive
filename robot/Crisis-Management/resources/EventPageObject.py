from cumulusci.robotframework.pageobjects import BasePage
from cumulusci.robotframework.pageobjects import DetailPage
from cumulusci.robotframework.pageobjects import HomePage
from cumulusci.robotframework.pageobjects import pageobject
from locators import event_locators
import time
from cumulusci.robotframework.utils import selenium_retry,capture_screenshot_on_error

@pageobject("NewStandardEvent", "Event")
class StandardEventNewPage(BasePage):

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')

    def _is_current_page(self):
        """ Verify we are on the New Standard Event page
            by verifying that the header title is 'New Event: Standard Event'
        """
        locator_title = event_locators["standard_event"]["new_event_title"]
        self.selenium.page_should_contain_element(locator_title,
                                                  message="Title is not 'New Event: Standard Event' as expected")

    @capture_screenshot_on_error
    def click_save_button(self):
        """ Click on the save button """
        locator_footer = event_locators["standard_event"]["footer"]
        locator_save = event_locators["standard_event"]["save"]
        self.selenium.scroll_element_into_view(locator_footer)
        self.selenium.wait_until_page_contains_element(locator_save)
        self.selenium.wait_until_element_is_enabled(locator_save, error="Save button is not enabled")
        self.selenium.get_webelement(locator_save).click()

    def populate_standard_event_form(self, **kwargs):
        """ Populates standard event form with the field-value pairs """
        for key, value in kwargs.items():
            if key == 'Location':
                locator = event_locators["standard_event"]["location"]
                self.selenium.get_webelement(locator).send_keys(value)
            elif key == 'Subject':
                self.sal.select_value_from_listbox(key, value)
            elif key == 'StartDate':
                locator = event_locators["standard_event"]["date"].format("Start", "Date")
                self.selenium.clear_element_text(locator)
                self.selenium.get_webelement(locator).send_keys(value)
            elif key == 'Description':
                locator = event_locators["standard_event"]["description"]
                self.selenium.get_webelement(locator).send_keys(value)
            else:
                assert False, "Key provided by name '{}' does not exist".format(key)

@pageobject("Home", "Event")
class EventHomePage(HomePage):
    object_name = "Event"

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')

    def _go_to_page(self, **kwargs):
        """ Navigates to the Home view of the SAL Event page """
        locator_home = event_locators["calendar_home"]
        locator_dialog = event_locators["dialog"]

        url = self.cumulusci.org.lightning_base_url
        url = "{}/lightning/o/Event/home".format(url)
        self.selenium.go_to(url)
        self.selenium.wait_until_page_contains_element(locator_home)

        # In some cases, there is a dialog suggestion that blocks other elements on the page,
        # hence making sure it is closed, before performing other actions
        if self.sal._check_if_element_exists(locator_dialog):
            self.selenium.click_element(locator_dialog)

    def _build_locator_for_appointment(self, **kwargs):
        """ This is a helper function to build the locator for 'appointment' on the Calendar Home page """
        locator = event_locators["appointment"]
        if kwargs.__len__() != 4:
            raise Exception("Required number of arguments were not passed during the method call")

        date = kwargs.get("date")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        subject = kwargs.get("subject")

        locator = locator.format(date, start_time, end_time, subject)
        self.builtin.log("Locator: " + locator)
        return locator

    def verify_appt_day_on_calendar_home(self,day):
        """ Verify that the appointment on the given date does exist on Calendar Home page for the current week 
            else it looks for the same appointment for the next week. if the appointment is found in the current
            week of the calendar then it returns True. On False, it checks for the appointment in the next week of the 
            calendar. Again if found it returns True else it returns False
        """
        self.sal.close_deleted_notes_window()
        day_locator = event_locators["calender_day_header"].format(day)
        next_week_locator = event_locators["next_week"]
        refresh_locator = event_locators["refresh"]
        print("refresh_locator {}".format(refresh_locator))
        self.selenium.wait_until_page_contains_element(refresh_locator,
            error="Refresh button is not found")
        self.selenium.click_element(refresh_locator)
        if not self.sal._check_if_element_exists(day_locator):
            self.selenium.click_element(next_week_locator)
            self.selenium.wait_until_page_contains_element(refresh_locator)
            self.selenium.click_element(refresh_locator)
            if self.sal._check_if_element_exists(day_locator):
                return True
            else:
                return False
        else:
            return True

    def verify_this_appt_does_not_exist_on_calendar_home(self, day, **kwargs):
        """ Verify that the appointment with given details does NOT exist on Calendar Home page
            all arguments are mandatory. kwargs: date, start_time, end_time, subject
            helper function '_build_locator_for_appointment' is being called to build the locator with the given args
        """
        event_found = self.verify_appt_day_on_calendar_home(day)
        if not event_found:
            locator = self._build_locator_for_appointment(**kwargs)
            self.selenium.page_should_not_contain_element(
                locator,
                message="Appointment with given details is available on Calendar Home. "
                        "Expected: Appointment should NOT be available"
            )

    def verify_this_appt_exists_on_calendar_home(self, day, **kwargs):
        """ Verify that the appointment with given details exists on Calendar Home page
            all arguments are mandatory. kwargs: date, start_time, end_time, subject
            helper function '_build_locator_for_appointment' is being called to build the locator with the given args
        """
        event_found = self.verify_appt_day_on_calendar_home(day)
        if event_found:
            locator = self._build_locator_for_appointment(**kwargs)
            self.selenium.wait_until_page_contains_element(locator)
            element_timeslot = self.selenium.driver.find_element_by_xpath(locator)
            self.selenium.driver.execute_script("arguments[0].scrollIntoView(true)", element_timeslot)
            self.selenium.wait_until_page_contains_element(
                locator,
                error="Appointment with given details is not available on Calendar Home. "
                        "Expected: Appointment should be available"
            )

    def click_new_event_button(self):
        """ Clicks on the 'New Event' button in Calendar page """
        locator = event_locators["new_event_button"]
        element = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.wait_until_page_contains_element(locator)
        # javascript is used here since the behaviour of selenium click is quite unstable for this button
        # tried other workarounds like increasing timeout etc, but nothing else worked
        self.selenium.driver.execute_script("arguments[0].click()", element)

    def refresh_event_page(self):
        """ Refresh the current page by clicking on the Refresh button """
        locator = event_locators["refresh"]
        self.selenium.page_should_contain_element(
            locator,
            message="Refresh button with locator '" + locator + "' is not available on the Event home page"
        )
        self.selenium.click_element(locator)

    def select_event_type(self, event_type):
        """ Select an event of event_type while creating new event

            :param event_type: this should match the line of text next to the radio button
            eg: Advising Event, Advising Time, Standard Event
        """
        locator = event_locators["select_type"].format(event_type)
        self.selenium.get_webelement(locator).click()

        locator = event_locators["next"]
        self.selenium.click_element(locator)
        self.salesforce.wait_until_modal_is_open()


@pageobject("Detail", "Event")
class EventDetailPage(DetailPage):
    object_name = "Event"

    # This can be moved to Cumulusci Detail page keywords in the future
    def header_title_should_be(self, title):
        """ Verify the header title """
        locator = event_locators["header_title"].format(title)
        self.selenium.page_should_contain_element(locator,
                                                  message="Header title is not " + title + " as expected")

    # This can be moved to Cumulusci Detail page keywords in the future
    def verify_field_value_exists(self, title, value):
        """ Verify that the field with label 'title' has its value as 'value' """
        locator = event_locators["field_value"].format(title, value)
        self.selenium.page_should_contain_element(
            locator,
            message="Field=" + title + " and value=" + value + " is not available on the page"
        )
