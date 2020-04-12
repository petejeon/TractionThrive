from cumulusci.robotframework.pageobjects import BasePage
from cumulusci.robotframework.pageobjects import pageobject
from locators import community_home_locators
from locators import community_launchpad_locators
import datetime

@pageobject("Launchpad", "Community")
class CommunityLaunchpadPage(BasePage):

    def sal(self):
        return self.builtin.get_library_instance('SAL')

    def _is_current_page(self):
        """ Verify we are on the Launchpad page
            by verifying the My Agenda title
        """
        locator = community_launchpad_locators["launchpad_tab"]
        locator = community_launchpad_locators["agenda_header"]
        self.selenium.wait_until_page_contains_element(
            locator,
            error="Launchpad agenda is not available"
        )
    
    def expand_date_picker(self):
        "Clicks on the date so that advisee can see all days of the week in launchpad"
        locator = community_launchpad_locators["expand_date_picker_button"]
        self.selenium.click_element(locator)

    def check_first_day_of_week(self,value):
        "Checks first day of week is displaying in date picker"
        locator = community_launchpad_locators["first_day_of_week"].format(value)
        self.selenium.wait_until_page_contains_element(locator)
