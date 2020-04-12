from cumulusci.robotframework.pageobjects import HomePage
from cumulusci.robotframework.pageobjects import pageobject
from locators import task_locators


@pageobject("Home", "Task")
class TaskHomePage(HomePage):
    object_name = None

    def _is_current_page(self):
        """ Verify we are on the Task home page by verifying the 'New Task' header title """
        locator = task_locators["header_title"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="The header for this page is not 'New Task' as expected")
