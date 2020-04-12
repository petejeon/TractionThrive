import time

from cumulusci.robotframework.pageobjects import HomePage
from cumulusci.robotframework.pageobjects import pageobject
from locators import availability_locators


@pageobject("Home", "Availability")
class AvailabilityHomePage(HomePage):
    object_name = None

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')

    def _is_current_page(self):
        """ Verify we are on the Availability Settings page
            by verifying that the header title is 'Edit Availability Settings'
        """
        locator = availability_locators["header"]
        self.selenium.page_should_contain_element(
            locator,
            message="Header with text 'Edit Availability Settings' is not available on the page"
        )

    def cancel_availability_settings(self):
        """ Click on the Cancel button on the Availability Settings page """
        locator = availability_locators["cancel"]
        self.selenium.page_should_contain_element(
            locator,
            message="Cancel button with locator " + locator + " on the availability page is not available"
        )
        self.selenium.click_element(locator)

    def cancel_recurrence(self):
        """ Click on the Cancel button of the recurrence modal """
        locator = availability_locators["recurrence_modal"]["cancel"]
        self.selenium.page_should_contain_element(
            locator,
            message="Cancel button with locator " + locator + " on the recurrence modal is not available"
        )
        self.selenium.click_element(locator)

    def click_on_new_recurrence(self):
        """ Scroll to the element and click on the 'New' button to create new recurrence
            Note: Scrolling to "New" button did not work since the footer is coming in the way
        """
        locator_new_button = availability_locators["new"]
        locator_day = availability_locators["day"].format("Tuesday")
        locator_modal_header = availability_locators["recurrence_modal"]["header"]

        self.selenium.scroll_element_into_view(locator_day)
        self.selenium.get_webelement(locator_new_button).click()

        self.selenium.page_should_contain_element(
            locator_modal_header,
            message="Recurrence modal with 'New Availability Hours' header is not available on the page"
        )

    def populate_new_recurrence_form(self, **kwargs):
        """ Populate the fields with data in the open modal to create a new recurrence """
        self.salesforce.wait_until_modal_is_open()
        for key, value in kwargs.items():
            if key == "Available For":
                locator = availability_locators["recurrence_modal"]["select_field"].format(key)
                self.selenium.select_from_list_by_value(locator, value)
            elif key == "Subject":
                locator = availability_locators["recurrence_modal"]["input"].format("subject")
                self.selenium.get_webelement(locator).send_keys(value)
            elif key == "Start Time":
                locator = availability_locators["recurrence_modal"]["input"].format("startTime")
                self.selenium.get_webelement(locator).send_keys(value)
            elif key == "End Time":
                locator = availability_locators["recurrence_modal"]["input"].format("endTime")
                self.selenium.get_webelement(locator).send_keys(value)
            elif key == "Repeat On":
                if value == "all":
                    day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                    for day in day_list:
                        locator = availability_locators["recurrence_modal"]["repeat_on_day"].format(day)
                        self.selenium.click_element(locator)
            elif key == "Repeat Every":
                locator = availability_locators["recurrence_modal"]["input"].format("recurrenceInterval")
                self.selenium.clear_element_text(locator)
                self.selenium.get_webelement(locator).send_keys(value)
            elif key == "Start On":
                locator = availability_locators["recurrence_modal"]["input"].format("startDate")
                self.selenium.clear_element_text(locator)
                self.selenium.get_webelement(locator).send_keys(value)
            elif key == "End On":
                locator = availability_locators["recurrence_modal"]["input"].format("endDate")
                self.selenium.get_webelement(locator).send_keys(value)

    def save_availability_settings_and_verify_toast_message(self, toast_message):
        """ Click on the 'Save' button to save changes to Availability Settings
            and verify that the toast message matches the provided argument 'toast_message'
        """
        locator = availability_locators["save"]
        element = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.wait_until_page_contains_element(
            locator,
            error=f"Save button with locator '{locator}' is not available on the availability page"
        )
        self.selenium.driver.execute_script("arguments[0].click()", element)
        self.sal.verify_toast_message(toast_message)

    def save_recurrence(self):
        """ Click on the save button of the recurrence modal """
        locator = availability_locators["recurrence_modal"]["save"]
        self.selenium.page_should_contain_element(
            locator,
            message=f"Save button with locator '{locator}' on the recurrence modal is not available"
        )
        self.selenium.click_element(locator)

    def update_advance_notice(self, value):
        """ Update the advance notice field in hours to the given value """
        locator = availability_locators["advance_notice"]
        self.selenium.set_focus_to_element(locator)
        self.selenium.clear_element_text(locator)
        self.selenium.get_webelement(locator).send_keys(value)

    def update_appointment_length(self, value):
        """ Update the appointment length field in mins to the given value """
        locator = availability_locators["appointment_length"]
        self.selenium.set_focus_to_element(locator)
        self.selenium.clear_element_text(locator)
        self.selenium.get_webelement(locator).send_keys(value)

    def update_appointment_buffer_length(self, value):
        """ Update the appointment buffer length field in mins to the given value """
        locator = availability_locators["appt_buffer_length"]
        self.selenium.set_focus_to_element(locator)
        self.selenium.clear_element_text(locator)
        self.selenium.get_webelement(locator).send_keys(value)

    def verify_recurrence_limit_error(self):
        """ Validate the error thrown when the recurrence is being set for an exceeded range of time """
        locator = availability_locators["recurrence_modal"]["recurrence_error"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="Application did not throw the expected recurrence error")
