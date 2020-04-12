from cumulusci.robotframework.pageobjects import DetailPage
from cumulusci.robotframework.pageobjects import pageobject
from locators import appointment_attendee_locators
from cumulusci.robotframework.utils import selenium_retry,capture_screenshot_on_error
from robot.libraries.BuiltIn import BuiltIn
import time

@pageobject("Detail", "AppointmentAttendee__c")
class AppointmentAttendeeDetailPage(DetailPage):
    object = "AppointmentAttendee__c"
    @property
    def builtin(self):
        return BuiltIn()

    def _is_current_page(self):
        """ Verify we are on the Appointment Attendee detail page
            by verifying that the header title is 'Appointment Attendee'
        """
        locator = appointment_attendee_locators["header"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="Header title is not 'Appointment Attendee' as expected")

    def click_save_button(self):
        """ Click on the save button to save the changes made to the Appointment Attendee record """
        locator = appointment_attendee_locators["edit"]["save"]
        self.selenium.click_element(locator)

    @capture_screenshot_on_error
    def update_field_value(self, field, value):
        """ Update the field with label 'field' to the given 'value' """
        locator_field = appointment_attendee_locators["field"].format(field)
        locator_field_edit_dropdown = appointment_attendee_locators["edit"]["status"].format(field)
        locator_field_edit_select_value = appointment_attendee_locators["edit"]["select_value"].format(value)
        self.selenium.wait_until_page_contains_element(locator_field)
        self.selenium.double_click_element(locator_field)
        self.selenium.capture_page_screenshot()
        self.selenium.wait_until_element_is_visible(
            locator_field_edit_dropdown,
            error=f"Select drop down for field '{field}' is not available on the page")
        element = self.selenium.get_webelement(locator_field_edit_dropdown)
        self.selenium.wait_until_page_contains_element(locator_field_edit_dropdown)
        self.selenium.driver.execute_script("arguments[0].click()", element)
        self.selenium.wait_until_page_contains_element(
            locator_field_edit_select_value,
            error=f"'{value}' value is not available in the select drop down options for '{field}'")
        self.selenium.click_element(locator_field_edit_select_value)
