from cumulusci.robotframework.pageobjects import HomePage
from cumulusci.robotframework.pageobjects import pageobject
from locators import community_home_locators
from selenium.webdriver.support.ui import Select
import datetime
import time

@pageobject("Home", "Community")
class CommunityHomePage(HomePage):

    @property
    def sal(self):
        return self.builtin.get_library_instance('SAL')

    def _is_current_page(self):
        """ Verify we are on the Community Home page
            by verifying the 'Upcoming' appointments tab
        """
        locator = community_home_locators["appointment_tab"]
        locator = self.sal.format_all(locator, "Upcoming")
        self.selenium.wait_until_page_contains_element(
            locator,
            error="Appointment manager tab for 'Upcoming' appointments is not available"
        )

    def _build_locator_for_appointment(self,locator, **kwargs):
        """ This is a helper function to build the locator for 'appointment' on the Community Home page """
        if len(kwargs) != 6:
            raise Exception("Required number of arguments were not passed during the method call")

        date = kwargs.get("date")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        subtopic = kwargs.get("subtopic")
        advisor = kwargs.get("advisor")
        location = kwargs.get("location")

        locator = locator.format(subtopic, date, start_time, end_time, advisor, location)
        self.builtin.log("Locator: " + locator)
        return locator

    def _build_locator_for_walkin_appointment(self,locator, **kwargs):
        """ This is a helper function to build the locator for 'appointment' on the Community Home page """
        if len(kwargs) != 6:
            raise Exception("Required number of arguments were not passed during the method call")

        date = kwargs.get("date")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        topic_subtopic = kwargs.get("topic_subtopic")
        advisor = kwargs.get("advisor")
        location = kwargs.get("location")

        locator = locator.format(date, start_time, end_time, topic_subtopic, advisor, location)
        self.builtin.log("Locator: " + locator)
        return locator

    def _iterate_card_info(self,locator):
        """ Card info provides the total number of appointments  booked and it is also required to iterate over a list of scheduled or walkin appointments in the community page 
        in order to validate whether a recently booked appointment appears in the list or not."""
        card_info_locator = community_home_locators["card_info"]
        card_info_length= self.selenium.get_element_count(card_info_locator)
        self.sal.builtin.log("card info length: {}".format(card_info_length))
        for i in range(card_info_length):
            card_info_locator[i]
            if not self.sal._check_if_element_exists(locator): 
                continue
            else:
                self.selenium.page_should_contain_element(
                locator,
                message="Appointment with given details is not available on Community Home. "
                        "Expected: Appointment should be available"
                )
                return True

    def click_actions_button(self,value):
        """This function clicks on Add Comments or Reschedule button in the community page"""
        locator= community_home_locators["schedule_appt"]["actions"].format(value)
        self.selenium.click_element(locator)

    def click_appointment_subtopic(self,subtopic):
        """This clicks on the subtopic title of the appointment in the Advisee Community Home page"""
        locator = community_home_locators["appointment_card_title"].format(subtopic)
        self.selenium.wait_until_page_contains_element(
            locator,
            error=f"The subtopic title with the value, '{locator}' is not available on the Community Home page")
        appt_card_info = self._iterate_card_info(locator)
        if appt_card_info:
            self.selenium.click_element(locator)
        assert f"Appointment card with the info '{locator}' is not found"

    def click_close_button(self):
        """This closes the appointment modal"""
        locator= community_home_locators["schedule_appt"]["close_button"]
        self.selenium.click_element(locator)

    def click_reschedule_cancel_button(self,value):
        """Reschedules or cancels an exisiting appointment """
        locator = community_home_locators["reschedule_cancel"].format(value)
        print(f"reschedule locator '{locator}'")
        self.selenium.wait_until_page_contains_element(
            locator,timeout=60,
            error=f"The button with the locator '{locator}' is not available on the Community Home page")
        field = self.selenium.get_webelement(locator)
        self.selenium.driver.execute_script("arguments[0].click()", field)
    
    def click_subtopic_reschedule_cancel_button(self):
        """Reschedules or cancels an exisiting appointment """
        locator = community_home_locators["subtopic_reschedule_cancel"]
        self.selenium.wait_until_page_contains_element(
            locator,timeout=60,
            error=f"The button with the locator '{locator}' is not available on the Community Home page")
        field = self.selenium.get_webelement(locator)
        self.selenium.driver.execute_script("arguments[0].click()", field)

    def confirm_reschedule_cancel_action(self,action):
        """Select reschedule or cancel action on an exisiting appointment """
        locator = community_home_locators["reschedule_cancel"].format(action)
        self.selenium.wait_until_page_contains_element(
            locator,
            error=f"The '{action}' apppointment button with the locator '" + locator + "' is not available on the Community Home page")
        self.selenium.click_element(locator)

    def click_schedule_appt_button(self):
        """This clicks on the schedule button in the Advisee Community Home page"""
        locator = community_home_locators["schedule_appt_btn"]
        self.selenium.page_should_contain_element(
            locator,
            message="The schedule apppointment button with the locator '" + locator + "' is not available on the Community Home page")
        self.selenium.click_element(locator)

    def click_appointment_tabs(self,title,value):
        """This clicks on the Upcoming tab in the Advisee Community Home page"""
        locator = community_home_locators["appointment_tab"].format(title,value)
        self.selenium.page_should_contain_element(
            locator,
            message="The upcoming tab with the locator '" + locator + "' is not available on the Community Home page")
        self.selenium.click_element(locator)

    
    def enter_cancel_reason_and_cancel(self,description,action):
        """Enters the reason for cancellation and clicks on the cancel appointment button"""
        locator = community_home_locators["cancellation_reason"]
        self.selenium.get_webelement(locator).send_keys(description)
        cancel_locator = community_home_locators["reschedule_cancel"].format(action)
        self.selenium.click_element(cancel_locator)

    def enter_comments_and_save(self,description,action):
        """Enters comments on an appointment and clicks on the save button"""
        locator = community_home_locators["schedule_appt"]["description"]
        self.selenium.get_webelement(locator).send_keys(description)
        save_locator = community_home_locators["schedule_appt"]["save_cancel"].format(action)
        self.selenium.click_element(save_locator)

    def go_to_my_settings(self):
        """ Navigate to 'My Settings' page by choosing the option from user profile drop down """
        locator_dropdown = community_home_locators["user_dropdown"]
        locator_settings = community_home_locators["settings"]

        self.selenium.page_should_contain_element(
            locator_dropdown,
            message="The drop down for user profile "
                    "with locator '" + locator_dropdown + "' is not available on the page")
        self.selenium.click_element(locator_dropdown)
        self.selenium.page_should_contain_element(
            locator_settings,
            message="My Settings option in the user drop down menu "
                    "with locator '" + locator_settings + "' is not available on the page")
        self.selenium.click_element(locator_settings)


    def schedule_appointment(self,**kwargs):
        """Chooses appropriate values to schedule an appointment with the field-value pairs
            The supported keys are Advisor, Location, and Topic
        """
        for key, value in kwargs.items():
            if key == 'Advisor':
                locator = community_home_locators["schedule_appt"]["appointment_info"].format(value)
                self.selenium.click_element(locator)
            if key == 'Location':
                locator = community_home_locators["schedule_appt"]["appointment_info"].format(value)
                self.selenium.click_element(locator)
            if key == 'Topic':
                locator = community_home_locators["schedule_appt"]["appointment_info"].format(value)
                self.selenium.click_element(locator)
            if key == 'Type':
                locator = community_home_locators["schedule_appt"]["appointment_info"].format(value)
                self.selenium.click_element(locator)

    def select_time_slot(self,start_time,end_time):
        """This function selects the timeslot required for the appointment and also selects the next month or year when the it is the last day of the appointment in the month or year in the calendar,
        depending on the appointment slots displayed in the booking modal of the community page"""
        
        locator = community_home_locators["schedule_appt"]["time_slot"]
        current= self.sal.get_next_monday()
        current_date=current.strftime('%Y-%m-%d')
        calendar_format_date = current.strftime('%A, %B %-d, %Y')
        locator = locator.format(calendar_format_date, start_time, end_time)
        print("Locator {}".format(locator))
        self.selenium.click_element(locator)

    def select_time_slot_community(self,start_time,end_time,appointment_type,month):
        """This function selects the timeslot required for the appointment and also selects the next month or year when the it is the last day of the appointment in the month or year in the calendar,
        depending on the appointment slots displayed in the booking modal of the community page"""

        locator = community_home_locators["schedule_appt"]["time_slot_community"]
        current= self.sal.get_next_monday()
        current_date=current.strftime('%Y-%m-%d')
        calendar_format_date = current.strftime('%A, %B %-d, %Y')
        locator = locator.format(current_date, calendar_format_date, current_date, start_time, end_time,appointment_type)
        print("Locator {}".format(locator))
        current_month_locator = community_home_locators["schedule_appt"]["current_month"]
        current_month= self.selenium.get_webelement(current_month_locator)
        if not self.sal._check_if_element_exists(locator) and current_month.text!= month:
            calendar_locator = community_home_locators["schedule_appt"]["calender_box"]
            self.selenium.wait_until_page_contains_element(
            calendar_locator,
            error=f"'{calendar_locator}' is not available in the appointment scheduling page")
            self.selenium.set_focus_to_element(calendar_locator)
            self.selenium.click_element(calendar_locator)
            self.selenium.wait_until_element_is_visible(
            calendar_locator,
            error=f"Calender drop down, '{calendar_locator}' is not available on the page")
            self.selenium.capture_page_screenshot()
            month_locator = community_home_locators["schedule_appt"]["month_year"].format(month)
            self.selenium.wait_until_page_contains_element(
            month_locator,
            error=f"'{month}' value is not available in the select drop down options for '{month_locator}'")
            month_menu = self.selenium.driver.find_element_by_xpath(month_locator)
            self.selenium.select_from_list_by_label(month_menu,month)
            self.selenium.capture_page_screenshot()
            current_date=current.strftime('%Y-%m-%d')
            calendar_format_date = current.strftime('%A, %B %-d, %Y')
            locator = locator.format(current_date, calendar_format_date, current_date, start_time, end_time,appointment_type)
            print("Locator {}".format(locator))
            self.selenium.wait_until_page_contains_element(
            locator,
            error=f"'{locator}' value is not available in the appointment scheduling page")
            self.selenium.click_element(locator)
        else:
            self.selenium.click_element(locator)


    def verify_action_buttons_exists_on_community_page(self,button1,button2):
        """Verifies the following action buttons are displayed on the appointment card
            1. Add Comments
            2. Reschedule or Cancel
        """
        locator = community_home_locators["appointment_actions"].format(button1,button2)
        self.selenium.page_should_contain_element(
            locator,
            message="Action buttons with the" + locator+ "does not exist in the appointment card of the community page"
        )
    
    def verify_action_buttons_does_not_exists_on_community_page(self,button1,button2):
        """Verifies the following action buttons are not displayed on the appointment card
            1. Add Comments
            2. Reschedule or Cancel
        """
        locator = community_home_locators["appointment_actions"].format(button1,button2)
        self.selenium.page_should_not_contain_element(
            locator,
            message="Action buttons with the" + locator+ "exists in the appointment card of the community page"
        )

    def verify_reschedule_cancel_button_does_not_exist_on_subtopic_link(self):
        """Verifies Reschedules or cancel button is not displayed on the subtopic link of the Community"""

        locator = community_home_locators["subtopic_reschedule_cancel"]
        self.selenium.page_should_not_contain_element(
            locator,
            message=f"Reschedule button with the locator '{locator}' is available on the subtopic link of the Community Home page")

    def verify_appointment_card_title(self,value):
        "Verifies the title of an appointment card in community"
        locator = community_home_locators["appointment_card_title"].format(value)
        self.selenium.page_should_contain_element(
            locator,
            message="Appointment with that title does not exist in community"
        )

    def verify_appointment_type(self,value):
        "Verifies the type of an existing appointment in community home page"
        locator = community_home_locators["appointment_type"].format(value)
        self.selenium.wait_until_page_contains_element(
            locator,
            error="Appointment with that appointment type does not exist in community"
        )

    def verify_scheduled_appointment_confirmation_text(self,value):
        """This function helps us verify the confirmation text of scheduled appointment once scheduled"""

        locator = community_home_locators["schedule_appt"]["appt_confirmation_text"]["scheduled_appt_confirmation_text"].format(value)
        self.selenium.page_should_contain_element(
            locator,
            message="Confirmation with the text, "+locator + "did not appear on Community Home. "
                    "Expected: text, 'Your appointment with DevTest Advisor has been scheduled' should be displayed"
        )

    def verify_walkin_appointment_confirmation_text(self,appointment_type,confirmation_stmt1,confirmation_stmt2):
        """This function helps us verify the confirmation text appears after the appointment has been scheduled"""

        confirmation_text1_locator = community_home_locators["schedule_appt"]["appt_confirmation_text"]["walkin_appt_confirmation_text1"].format(appointment_type,confirmation_stmt1)
        self.selenium.page_should_contain_element(
            confirmation_text1_locator,
            message=f"Confirmation with the text, '{confirmation_text1_locator}' did not appear on Community Home. "
        )
        confirmation_text2_locator = community_home_locators["schedule_appt"]["appt_confirmation_text"]["walkin_appt_confirmation_text2"]
        ele = self.selenium.get_webelement(confirmation_text2_locator).text
        self.selenium.page_should_contain_element(
            confirmation_text2_locator,
            message=f"Confirmation with the text, '{confirmation_text2_locator}' did not appear on Community Home. "
        )
        if ele == confirmation_stmt2:
            return True
        else:
            return f"Confirmation Text with '{confirmation_stmt2}' not found"

    def verify_appointment_details(self,**kwargs):
        """This function helps us verify the appointment details in the confirmation modal that appears while scheduling an appointment via Community page"""
        
        locator = community_home_locators["appointment_card_info"]
        appt_details_locator = self._build_locator_for_appointment(locator, **kwargs)
        self.selenium.page_should_contain_element(
            appt_details_locator,
            message="Scheduled Appointment with the details," + appt_details_locator + " does not exist on Community Home. "
                    "Expected: Scheduled Appointment details should be displayed"
        )

    def verify_appointment_tab_list(self):
        """This function helps us verify the following tabs: Upcoming,Past,Cancelled exists on Community Home. """

        locator = community_home_locators["appointment_tab_list"]
        tab_length= self.selenium.get_element_count(locator)
        tab_list = ["Upcoming","Past","Cancelled"]
        for i in range (tab_length):
            tab_locator = community_home_locators["appointment_tab"].format(tab_list[i],tab_list[i])
            self.selenium.page_should_contain_element(
                tab_locator,
                message="Appointment tab, "+locator + "with the following" + tab_list[i] +"does not exist in Community Home. "
                        "Expected: The following tabs: Upcoming,Past,Cancelled should be displayed"
            )

    def verify_avatar_exists_after_scheduling_appt(self):
        """ Verify that the avatar image appears after an appointment is being scheduled.
            After appointment schedule avatar appears in two places:
            1. In the appointment confirmation modal along with other appointment details
            2. In the Upcoming tab of the community home page
        """
        locator = community_home_locators["schedule_appt"]["appt_avatar_img"]
        self.selenium.page_should_contain_element(
            locator,
            message="Avatar image does not appear on the " +locator
        )

    def verify_avatar_does_not_exists_after_scheduling_walkin_appt_in_community(self):
        """ Verify that the avatar image does not appears after a walkin appointment is being scheduled. """
        locator = community_home_locators["schedule_appt"]["appt_avatar_img"]
        self.selenium.page_should_not_contain_element(
            locator,
            message="Avatar image does not appear on the " +locator
        )

    def verify_this_appt_does_not_exist_on_community_home(self, **kwargs):
        """ Verify that the appointment with given details does NOT exist on Community Home page
            all arguments are mandatory. kwargs: date, start_time, end_time, subtopic, advisor, location
            helper function '_build_locator_for_appointment' is being called to build the locator with the given args
        """
        appointment_info_locator = community_home_locators["appointment"]
        locator = self._build_locator_for_appointment(appointment_info_locator,**kwargs)
        self.selenium.page_should_not_contain_element(
            locator,
            message="Appointment with given details is available on Community Home. "
                    "Expected: Appointment should NOT be available"
        )

    def verify_this_appt_exists_on_community_home(self, **kwargs):
        """ Verify that the appointment with given details exists on Community Home page
            all arguments are mandatory. kwargs: date, start_time, end_time, subtopic, advisor, location
            helper function '_build_locator_for_appointment' is being called to build the locator with the given args
        """
        appointment_info_locator = community_home_locators["appointment"]
        locator = self._build_locator_for_appointment(appointment_info_locator,**kwargs)
        appt_card_info = self._iterate_card_info(locator)
        if appt_card_info:
            return
        assert f"'{appt_card_info}', '{appointment_info_locator}' with details not found."

    def verify_time_slot_does_not_exist_on_appt_schedule_modal(self,start_time,end_time,appointment_type,month):
        """This function verfies whether a given timeslot does not exist on the schedule appointment modal 
           Eg: An advisee(Andy Young) is booking an appointment between 10AM-10:30AM on current date with an 
           Advisor(DevTest Advisor)and there is another advisee (Sophia Student) who is trying to book an appointment with 
           the same Advisor (DevTest Advisor) on the same day & time slot, then the booked timeslot should not be displayed 
           in the appointment modal during appointment creation.
        """

        locator = community_home_locators["schedule_appt"]["time_slot_community"]
        current= self.sal.get_next_monday()
        current_date=current.strftime('%Y-%m-%d')
        calendar_format_date = current.strftime('%A, %B %-d, %Y')
        current_month_locator = community_home_locators["schedule_appt"]["current_month"]
        current_month= self.selenium.get_webelement(current_month_locator)
        if not self.sal._check_if_element_exists(locator) and current_month.text!= month:
            calendar_locator = community_home_locators["schedule_appt"]["calender_box"]
            self.selenium.wait_until_page_contains_element(
            calendar_locator,
            error=f"'{calendar_locator}' is not available in the appointment scheduling page")
            self.selenium.set_focus_to_element(calendar_locator)
            self.selenium.click_element(calendar_locator)
            self.selenium.wait_until_element_is_visible(
            calendar_locator,
            error=f"Calender drop down, '{calendar_locator}' is not available on the page")
            month_locator = community_home_locators["schedule_appt"]["month_year"].format(month)
            self.selenium.wait_until_page_contains_element(
            month_locator,
            error=f"'{month}' value is not available in the select drop down options for '{month_locator}'")
            month_menu = self.selenium.driver.find_element_by_xpath(month_locator)
            self.selenium.select_from_list_by_label(month_menu,month)
            self.selenium.capture_page_screenshot()
            locator = locator.format(current_date, calendar_format_date, current_date, start_time, end_time,appointment_type)
            print("Locator {}".format(locator))
            self.selenium.page_should_not_contain_element(
                locator,
                message="Selected time slot for an appointment is available for scheduling."
                        "Expected: Selected time slot for an appointment should NOT be available"
            )
        else:
            locator = locator.format(current_date, calendar_format_date, current_date, start_time, end_time,appointment_type)
            print("Locator {}".format(locator))
            self.selenium.page_should_not_contain_element(
                locator,
                message="Selected time slot for an appointment is available for scheduling."
                        "Expected: Selected time slot for an appointment should NOT be available"
            )


    def verify_walkin_appointment_details(self,**kwargs):
        """This function helps us verify the appointment details in the confirmation modal that appears while scheduling an appointment via Community page"""
        
        locator = community_home_locators["schedule_appt"]["walkin_appt_confirmation_info"]
        walkin_appt_details_locator =self._build_locator_for_walkin_appointment(locator,**kwargs)
        self.selenium.page_should_contain_element(
            walkin_appt_details_locator,
            message="Scheduled Appointment with the details," + walkin_appt_details_locator + " does not exist on Community Home. "
                    "Expected: Scheduled Appointment details should be displayed"
        )