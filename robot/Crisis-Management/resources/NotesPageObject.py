import time

from cumulusci.robotframework.pageobjects import HomePage
from cumulusci.robotframework.pageobjects import pageobject
from locators import notes_locators


@pageobject("Home", "Notes")
class NotesHomePage(HomePage):
    object_name = None

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')

    def _is_current_page(self):
        """ Verify we are on the Notes home page by verifying the Notes header title """
        locator = notes_locators["header_title"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="The header for this page is not 'Notes' as expected")

    def add_note_to_records(self, object_type, object_value):
        """ Click on 'Add to Records' button
            select the given 'object' from the drop down. Eg: Contacts, Appointments etc
            select the given 'value' for the object and then click on 'Add' button
        """
        self.builtin.log("Clicking on 'Add to Records' button")
        locator = notes_locators["add_to_records"]["add_to_records_button"]
        self.selenium.wait_until_page_contains_element(
            locator,
            error="'Add to Record' button is not available in Notes"
        )
        self.selenium.click_element(locator)

        self.builtin.log("Clicking on the current object_type image to open the drop down")
        locator_object_type_dropdown = notes_locators["add_to_records"]["object_type_dropdown"]
        self.selenium.wait_until_page_contains_element(
            locator_object_type_dropdown,
            error="Object drop down is not available in Add Note to Records popup"
        )
        self.selenium.click_element(locator_object_type_dropdown)

        self.builtin.log("Selecting the object_type from list of drop down objects")
        locator_object_type = notes_locators["add_to_records"]["object_type"].format(object_type)
        self.selenium.wait_until_page_contains_element(
            locator_object_type,
            error="Given object type '" + object_type + "' is not available in the drop down list"
        )
        self.selenium.click_element(locator_object_type)

        self.builtin.log("Entering the object_value in the search box")
        locator_object_value_search = notes_locators["add_to_records"]["object_value_search"].format(object_type)
        self.selenium.click_element(locator_object_value_search)
        self.selenium.get_webelement(locator_object_value_search).send_keys(object_value)

        self.builtin.log("Selecting the object_value from the search results list")
        locator_object_value = notes_locators["add_to_records"]["object_value"].format(object_value)
        self.selenium.click_element(locator_object_value)
        locator = notes_locators["add_to_records"]["span"]
        self.selenium.get_webelement(locator).click()

        self.builtin.log("Clicking on add button")
        locator_add_button = notes_locators["add_to_records"]["add_button"]
        self.selenium.click_element(locator_add_button)

    def enter_plain_text_in_body_of_note(self, note):
        """ Add text to the text area -- main body in Notes """
        locator = notes_locators["add_body"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="'Enter a note...' field is not available in Notes")
        self.selenium.click_element(locator)
        self.selenium.get_webelement(locator).send_keys(note)
        # Since the note gets auto saved, if sleep is not added, the body text is not getting saved properly
        time.sleep(5)
        self.selenium.capture_page_screenshot()

    def enter_subject_for_note(self, subject):
        """ Clicks on the 'Subject' text field in Notes and enters the text passed in the argument """
        locator = notes_locators["add_subject"]
        self.selenium.wait_until_page_contains_element(locator,
                                                       error="'Enter a subject...' field is not available")
        self.selenium.click_element(locator)
        self.selenium.clear_element_text(locator)
        self.selenium.get_webelement(locator).send_keys(subject)

    def verify_notes_body(self, note):
        """ Verifies the contents of the notes body text area in the Notes section """
        locator = notes_locators["notes_body"].format(note)
        self.selenium.wait_until_page_contains_element(locator,
                                                       error=note + " text not found in text area of Notes")

    def verify_notes_subject(self, subject):
        """ Verifies the contents of the subject line in the Notes section """
        locator = notes_locators["notes_subject"].format(subject)
        self.selenium.wait_until_page_contains_element(
            locator, 
            error="Specific test note called " + subject + " not found in Notes home"
        )
        element = self.selenium.get_webelement(locator)
        self.selenium.driver.execute_script("arguments[0].click()", element)
