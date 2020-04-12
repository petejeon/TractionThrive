from cumulusci.robotframework.pageobjects import HomePage
from cumulusci.robotframework.pageobjects import pageobject
from locators import email_locators


@pageobject("Home", "Email")
class EmailHomePage(HomePage):
    object_name = None

    def _is_current_page(self):
        """ Verify we are on the Email home page by verifying the 'Send an Email' header title """
        locator = email_locators["header_title"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="The header for this page is not 'Send an Email' as expected")
