from cumulusci.robotframework.pageobjects import DetailPage
from cumulusci.robotframework.pageobjects import pageobject
from locators import case_locators
import time

@pageobject("Detail", "Case")
class CaseDetailPage(DetailPage):
    object_name = "Case"

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')
        
    # This can be moved to Cumulusci Detail page keywords in the future
    def header_title_should_be(self, title):
        """ Verify the header title """
        locator = case_locators["header_title"].format(title)
        self.selenium.page_should_contain_element(locator,
                                                  message="Header title is not " + title + " as expected")

    def select_tab_from_case_advisee_record(self, tab):
        """ Selects corresponding tab in Case object
            tab refers to the name of the tab. eg: Alerts, Notes, Success Plans etc
        """
        locator_more = case_locators["select_more_dropdown"]
        self.selenium.wait_until_page_contains_element(locator_more,
                                                       error="'More' drop down not found in Cases: " + locator_more)
        element = self.selenium.get_webelement(locator_more)
        self.selenium.driver.execute_script("arguments[0].click()", element)  
        time.sleep(2)

        locator = case_locators["tab_name"].format(tab)
        element_menu = self.selenium.driver.find_element_by_xpath(locator)
        self.selenium.wait_until_page_contains_element(
            locator,
            error=tab + " tab item not found in Case detail using locator: " + locator
        )
        element_tab_name = self.selenium.get_webelement(locator)
        self.selenium.driver.execute_script("arguments[0].click()", element_tab_name) 


    def verify_notes_body(self, note):
        """ Verifies the contents of the notes currently opened """
        locator_body = case_locators["notes_section"]["body"].format(note)
        locator_close = case_locators["notes_section"]["close"]
        self.selenium.wait_until_page_contains_element(
            locator_body,
            error=f"'{note}' text not found in text area of Notes"
        )
        self.selenium.click_element(locator_close)

    def verify_notes_subject(self, subject):
        """ Verifies the contents of the subject line for the note in the Case section
            and then click on it to open the note
        """
        locator = case_locators["notes_section"]["subject"].format(subject)
        self.selenium.wait_until_page_contains_element(
            locator,
            error="Specific note called '" + subject + "' not found in Notes section of Case"
        )
        element = self.selenium.get_webelement(locator)
        self.selenium.driver.execute_script("arguments[0].click()", element)

    def click_advising_appointment_table_dropdown_arrow(self):
        """Clicks on the drop down arrow for an upcoming appointment under Upcoming section on Advising case page and then clicks the Edit button"""
        locator = case_locators["advising_section"]["appointment_dropdown"]
        self.salesforce._jsclick(locator)
        edit_opt = case_locators["advising_section"]["dropdown_edit_button"]
        self.salesforce._jsclick(edit_opt)

