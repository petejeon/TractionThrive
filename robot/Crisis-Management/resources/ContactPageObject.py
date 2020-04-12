from cumulusci.robotframework.pageobjects import DetailPage
from cumulusci.robotframework.pageobjects import pageobject
from locators import contact_locators


@pageobject("Detail", "Contact")
class ContactDetailPage(DetailPage):
    object_name = "Contact"

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')

    def login_to_community_as_user(self):
        """ Click on 'Show more actions' drop down and select the option to log in to community as user """
        locator_actions = contact_locators["show_more_actions"]
        locator_login_link = contact_locators["login_to_community"]
        locator_login_error = contact_locators["community_login_error"]

        self.selenium.wait_until_page_contains_element(
            locator_actions,
            error="Drop down to show more actions is not available on the page"
        )
        self.selenium.click_element(locator_actions)
        self.selenium.wait_until_page_contains_element(
            locator_login_link,
            error="'Log in to community as user' option is not available in the list of actions"
        )
        self.selenium.click_element(locator_login_link)
        if self.sal._check_if_element_exists(locator_login_error):
            assert False, "Community login error with message: " \
                          "Looks like this portal user is not a member of a community or your community is down"
