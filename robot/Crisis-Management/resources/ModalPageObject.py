from cumulusci.robotframework.pageobjects import BasePage
from cumulusci.robotframework.pageobjects import pageobject
from locators import modal_locators


@pageobject("Modal", "CancelAppointment")
class CancelAppointmentModal(BasePage):
    object_name = None

    def _is_current_page(self):
        """ Verify the 'Cancel Appointment' modal is open
            by verifying its header value
        """
        locator = modal_locators["cancel_appointment"]["header"]
        self.salesforce.wait_until_modal_is_open()
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="Modal with header 'Cancel Appointment' is not available")

    def close_modal(self):
        """ Close the modal popup by clicking on thee X button """
        locator = modal_locators["cancel_appointment"]["close"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="Cancel appointment modal doesn't have the Close X button")
        self.selenium.click_element(locator)

    def enter_comments_in_the_modal(self, comments):
        """ Input given value in the Comments section of the modal """
        locator = modal_locators["cancel_appointment"]["comments"]
        self.selenium.get_webelement(locator).send_keys(comments)

    def click_button_on_modal(self, button_name):
        """ Click on the button of the modal with label as 'button_name' """
        locator = modal_locators["cancel_appointment"]["button"].format(button_name)
        self.selenium.get_webelement(locator).click()
