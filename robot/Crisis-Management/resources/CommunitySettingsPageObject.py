from cumulusci.robotframework.pageobjects import BasePage
from cumulusci.robotframework.pageobjects import pageobject
from locators import community_settings_locators, sal_lex_locators, community_home_locators
import time


@pageobject("Settings", "Community")
class CommunitySettingsPage(BasePage):
    object_name = None

    def _is_current_page(self):
        """ Verify we are on the Community Settings page by verifying the header title is 'My Settings' """
        locator = community_settings_locators["header_title"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="Header title is not 'My Settings' as expected")

    def update_timezone(self, value):
        """ Update the timezone of the user in settings page
            :param value: Should exactly match with the drop down values available on the page for timezone drop down
        """
        locator_timezone = community_settings_locators["timezone"]
        locator_timezone_value = community_settings_locators["timezone_value"].format(value)
        self.selenium.page_should_contain_element(
            locator_timezone,
            message="Timezone field with locator '" + locator_timezone + "' is not available on the page"
        )
        self.selenium.click_element(locator_timezone)
        element = self.selenium.driver.find_element_by_xpath(locator_timezone_value)
        self.selenium.page_should_contain_element(
            element,
            message="'" + locator_timezone_value + "' is not a valid timezone value"
        )
        self.selenium.driver.execute_script("arguments[0].click();", element)
        self.selenium.capture_page_screenshot()
        
    def click_save_button(self):
        """ Click on the save button to save the timezon changes in the user settings page"""
        locator = sal_lex_locators["save"]
        self.selenium.wait_until_page_contains_element(
            locator,
            error=f"Save button with the locator, '{locator}' is not available on the Community Settings page")
        element = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.driver.execute_script("arguments[0].click();", element)
        self.selenium.capture_page_screenshot()

        
