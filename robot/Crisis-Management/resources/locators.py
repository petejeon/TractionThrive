sal_lex_locators = {
    "app_launcher": {
        "view_all_button": "//button[text()='View All']",
        "app_link": "//p[contains(@title,'{}')]",
    },
    "listbox": {
        "title": "//label[contains(text(), '{}')]/following::input[contains(@class, 'slds-input slds-combobox__input') and @role='textbox']",
        "value": "//*[contains(@class, 'slds-listbox__option') and @data-value='{}']",
    },
    "package": {
        "name": "//table[@class='list']/tbody/tr[{}]/th/a",
        "version": "//table[@class='list']/tbody/tr[{}]/td[4]",
    },
    "placeholder_lookup": {
        "lookup1": "//div[@class='slds-lookup__result-text' and contains(text(), '{}')]",
        "lookup2": "//mark[text() = '{}']/ancestor::a",
        "lookup3": "//div[contains(@class,'slds-listbox__option-text') and text()='{}']"
    },
    "close_tab": "//div[contains(@class, 'oneGlobalNav')]/descendant::*[@data-key='close']/ancestor::button",
    "frame": "//iframe[contains(@id, '{}') or contains(@title, '{}') or contains(@name, '{}')]",
    "input_placeholder": "//input[contains(@placeholder,'{}')]",
    "navigation_menu": "//button[@title='Show Navigation Menu']",
    "navigation_tab": "//button[@title='Show Navigation Menu']/../descendant::a[@title='{}']",
    "record_tab": "//a[@data-label='{}']",
    "rel_link":"//article[contains(@class, 'forceRelatedListCardDesktop')][.//img][.//span[@title='{}']]//table[contains(@class,'forceRecordLayout')]/tbody/tr[.//th/div/a[contains(@class,'textUnderline')]][.//td//a[text()='{}']]/th//a",
    "save": "//button[contains(@class, 'slds-button') and @type='button' and contains(text(), 'Save')]",
    "tabs":{
        "tab": "//a[contains(@class, 'tabHeader slds-context-bar__label-action') and @title='{}']",
    },
    "toast_message": "//div[contains(@class,'toastContent')]/child::div/span[text()='{}']",
    "toast_close": "//button[contains(@class,'slds-button_icon toastClose') and (@title='Close')]",
    "toast_close_community": "//button[contains(@class,'slds-button toastClose slds-notify__close')]",
    "users": {
        "user" : "//li[@data-node-id='ManageUsers']/div[@title='{}']/a[contains(@href,'ManageUsers')]",
        "login": "//table[@class='list']/tbody/tr[./td/input[contains(@title,'Advisor, DevTest')]]/td[@class='actionColumn']/a[text()='{}']",
        "login_user_detail": "//div[@data-message-id='loginAsSystemMessage']/descendant::span[contains(text(),'{}')]",
        "logout": "//a[@class='action-link']",
        "logout_user_detail": "//div[@data-message-id='loginAsSystemMessage']/descendant::a[contains(text(),'{}')]",

    }
}


appt_manager_locators = {
    "action": "//div[contains(@class, 'slds-utility-panel')]/descendant::button[@type='button' and text()='Action']",
    "action_close": "//div[contains(@class, 'slds-utility-panel')]/descendant::div[contains(@class, 'slds-popover')]/button[@title='Close dialog']",
    "action_shortcut": "//div[contains(@class, 'slds-utility-panel')]/descendant::button[@type='button' and text()='{}']",
    "advising_appointment": "//li[contains(@class, 'appt-utility-item busy advising')]",
    "appointment_type":{
        "advising": "//div[contains(@class,'test-id__field-label-container')]/span[text()='{}']//following::slot/lightning-formatted-text[contains(text(),'{}')]",
        "non-advising": "//div[contains(@class,'test-id__field-label-container')]/span[text()='{}']//following::span[@class='uiOutputTextArea' and text()='{}']",
    },
    "availability_settings": "//div[contains(@class, 'slds-utility-panel')]/descendant::button[@title='Settings']",
    "comments": "//textarea[contains(@class, 'slds-textarea') and @name='comments']",
    "description": "//div[text()='Description']/following-sibling::div[contains(text(), '{}')]",
    "disabled_action": "//div[contains(@class, 'slds-utility-panel')]/descendant::button[@disabled='true' and text()='{}']",
    "docked": "//div[contains(@class, 'slds-utility-panel') and contains(@class, 'DOCKED')]/descendant::h2[@title='Appointment Manager']",
    "last_appointment":"//lightning-formatted-date-time[contains(text(),'{}')]",
    "minimize": "//div[contains(@class, 'slds-utility-panel')]/descendant::button[@title='Minimize']",
    "new_appointment_button": "//div[@id='main']//button[contains(text(), 'New Appointment')]",
    "new_walkin_button": "//div[@id='main']//button[contains(text(), 'New Walk-In')]",
    "nonadvising_appointment": "//li[contains(@class, 'appt-utility-item busy non-advising')]",
    "refresh": "//div[contains(@class, 'slds-utility-panel')]/descendant::div[contains(@class, 'slds-col')]/button[contains(@class, 'slds-button') and @type='button' and @title='Refresh']",
    "selected_time": "//div[contains(@class, 'slds-utility-panel')]/descendant::li[contains(@class, 'selected')]/descendant::div[@class='times']/div/lightning-formatted-date-time[text()='{}']/../following-sibling::div/lightning-formatted-date-time[text()='{}']",
    "selected_location": "//li[contains(@class,'appt-utility-item busy advising selected')]//div[@class='info']//div[@class='slds-truncate'][contains(text(),'{}')]",
    "status": "//div[contains(@class, 'slds-utility-panel')]/descendant::div[text()='Status']/following-sibling::span[text()='{}']",
    "tomorrows_appointments": "//button[contains(@class, 'slds-button') and @type='button' and contains(@title, 'Show tomorrow')]",
    "view_advisee": "//button[contains(text(), 'View Advisee')]",
    "view_record": "//button[contains(text(), 'View Record')]",
    "timezone": "//*[@class = 'timezone-name']",
    "today": "//div[contains(@class, 'slds-utility-panel')]/descendant::button[text()='Today']",
    "up_next": "//button[text()='Up Next']",
    "window": "//span[@class='itemTitle' and text()='Appointment Manager']",
}

appointment_attendee_locators = {
    "field": "//div[contains(@class, 'slds-form-element__label')]/span[text()='{}']",
    "header": "//div/descendant::div[contains(@class, 'slds-page-header_record-home')]/descendant::div[text()='Appointment Attendee']",
    "edit": {
        "save": "//div[contains(@class, 'footer')]/descendant::button[@title='Save']",
        "status":"//label[text()='{}']",
        "select_dropdown": "//div[contains(@class, 'slds-form-element')]/descendant::span[text()='{}']/../following-sibling::div/descendant::span",
        "select_value": "//lightning-base-combobox-item[@role='option' and @data-value='{}']",
    },
}

appointment_locators = {
    "appointmnet_start_end_time": "//span[@class='test-id__field-label' and text()='{}']/following::div/span[contains(@class,'test-id__field-value')]",
    "blank_description": "//div[contains(@class, 'slds-form-element__label')]/span[text()='Description']/ancestor::div[contains(@class, 'slds-form-element')]/descendant::span[@class='uiOutputTextArea']" ,
    "field_value":"//div[contains(@class, 'slds-form-element__label')]/span[text()='{}']/ancestor::div[contains(@class, 'slds-form-element')]/descendant::span//slot[@slot='outputField']/lightning-formatted-text[text()='{}']",
    "header_title": "//span[text()='{}']",
    "new_appointment_header_title": "//h1[contains(@class, 'slds-page-header__title') and text()='{}']",
    "case_header_title": "//lightning-formatted-text[@title='{}']",
    "section_title": "//h3[contains(@class, 'slds-section__title')]/span[text()='Basics']",
    "advising_appointment": {
        "date-picker": "//*[@class = 'slds-datepicker']",
        "description": "//label[text()='Description']/following::textarea[@class='slds-textarea']",
        "first_available": "//button[contains(@class, 'slds-button') and text()='First Available']",
        "first_available_date": "//div[contains(@class,'slot_selection')]//h4/lightning-formatted-date-time",
        "first_available_start_end_time":"//div[contains(@data-aura-class,'AdvisorTimeSlot')]/descendant::div/lightning-formatted-date-time",
        "select_field": "//div[.//span[text()='{}'] and contains(@class, 'slds-form-element') ]//select",
        "topic_subtopic": "//option[text()='{}']",
        "one-off_appt": {
            "one-off-button": "//a[@id='custom__item']",
            "start_end_date": "//lightning-datepicker[@class='slds-form-element']/descendant::div/input[contains(@name,'{}')]",
            "start_end_time": "//lightning-timepicker[@class='slds-form-element']/descendant::div/input[contains(@name,'{}')]",
        }
        
    },
    "edit_appointment": {
        "appointment_timeslot": "//lightning-formatted-date-time[text()='{}']/following-sibling::lightning-formatted-date-time[contains(text(),'{}')]/../preceding-sibling::div/descendant::span[@class='slds-radio']",
        "disabled_field": "//label[text()='{}']/following-sibling::div/lightning-formatted-text[text()='{}']",
        "header_title": "//h1[contains(@class, 'slds-page-header__title') and text()='Edit Appointment']",
    },
}

availability_locators = {
    "advance_notice": "//div[contains(@class, 'slds-form-element')]/input[@name='notice']",
    "appointment_length": "//div[contains(@class, 'slds-form-element__control')]/input[@name='length']",
    "appt_buffer_length": "//input[@name='buffer']",
    "cancel": "//div[contains(@class, 'slds-docked-form-footer')]/button[contains(@class, 'slds-button') and @type = 'button' and text()='Cancel']",
    "day": "//*[text()='{}']",
    "header": "//header[contains(@class, 'slds-card__header')]/descendant::span[text()='Edit Appointment Availability']",
    "new": "//button[contains(@class, 'slds-button') and @type='button' and text()='New']",
    "save": "//div[contains(@class, 'slds-docked-form-footer sfalAdvisorApptSettingsEditor') or contains(@class, 'slds-docked-form-footer cAdvisorApptSettingsEditor')]/button[contains(@class, 'slds-button_brand') and @type = 'button' and text()='Save']",
    "recurrence_modal": {
        "cancel": "//div[contains(@class, 'slds-modal__footer')]/button[contains(@class, 'slds-button') and @type = 'button' and text()='Cancel']",
        "header": "//div[contains(@class, 'uiModal open active')]/descendant::div[contains(@class, 'slds-modal__header')]/descendant::span[text()='New Availability Hours']",
        "input": "//input[@name='{}']",
        "repeat_on_day": "//div[contains(@class, 'slds-modal')]/descendant::lightning-formatted-date-time[text()='{}']/../lightning-input",
        "save": "//div[contains(@class, 'slds-modal__footer')]/button[contains(@class, 'slds-button') and @type = 'button' and text()='Save']",
        "select_field": "//div[.//span[text()='{}'] and contains(@class, 'slds-form-element') ]//select",
        "recurrence_error": "//div[contains(@class, 'slds-modal')]/descendant::div[contains(@class, 'slds-notify_toast')]/descendant::h2[text()=\"We've encountered an error with the information you provided. Please make the following corrections:\"]/following-sibling::p/descendant::span[contains(text(), 'Select an end date on or before ') and contains(text(), '.: Recurrence End')]",
    },
}

case_locators = {
    "header_title": "//div[contains(@class, 'slds-page-header__title')]/span[text()='{}']",
    "select_more_dropdown": "//slot[@name='main']//slot//flexipage-component2//force-progressive-renderer//slot//slot//button[@class='slds-button'][contains(text(),'More')]",
    "tab_name": "//lightning-menu-item[@role='presentation']/a[@role='menuitem']/span[text()='{}']",
    "notes_section": {
        "subject": "//a[contains(text(),'{}')]",
        "body": "//div[contains(@class, 'notesEditPanel')]/descendant::div[@data-placeholder='Enter a note...']/p[text()='{}']",
        "close": "//div[contains(@class, 'panel') and @role='dialog']/descendant::button[@title='Close']"
    },
    "advising_section": {
        "appointment_dropdown": "//div[@class='slds-dropdown-trigger slds-dropdown-trigger_click']//button[@class='slds-button slds-button_icon-border slds-button_icon-x-small']/lightning-primitive-icon",
        "dropdown_edit_button": "//span[@class='slds-truncate'][contains(text(),'Edit')]"
    }
    
}

email_locators = {
    "header_title": "//h2[text()='Send an Email']",
}

community_home_locators = {
    "appointment": "//a[text()='{}']/../following-sibling::div/*[contains(text(), '{}')]/../following-sibling::div/*[text()='{}']/following-sibling::*[2][text()='{}']/../following-sibling::div[text()='{}']/following-sibling::div[text()='{}']",
    "appointment_actions" : "//div[contains(@class,'cCOM_apptActionMenu') or contains(@class,'sfalCOM_apptActionMenu')]/descendant::button[text()='{}']//following::button[(text()='{}')]",
    "appointment_card_info" : "//div[@id='confirmation-details']//div//a[text()='{}']//following::div/lightning-formatted-date-time[text()='{}']//following::div[contains(lightning-formatted-date-time,'{}') and descendant::lightning-formatted-date-time[text()='{}']]/following-sibling::div[contains(text(),'{}')]/following::div[text()='{}']",
    "appointment_card_title": "//a[text()='{}']",
    "appointment_tab": "//div[@class='slds-tabs_default']/descendant::li[@data-tab='true' and @title='{}']/a[text()='{}']",
    "appointment_tab_list": "//div[@class='slds-tabs_default']/descendant::li[@data-tab='true']",
    "appointment_type": "//h2/span//span[text()='{}']",
    "card_info": "//div[@class='appt-view-tab-content']//article[contains(@class,'slds-card')]",
    "cancellation_reason":"//textarea[@name='cancelComments']",
    "menu_item": "//a[contains(@class, 'menuItemLink') and text()='{}']",
    "reschedule_cancel": "//button[text()='{}']",
    "subtopic_reschedule_cancel": "//button[@class='slds-button slds-button_neutral slds-align_absolute-center action-menu-button']",
    "settings": "//a[@title='My Settings']",
    "schedule_appt_btn": "//button[contains(@class,'schedule-btn')]",
    "schedule_appt":{
        "appointment_info" : "//div[contains(@class,'item-name') and text()='{}']",
        "actions": "//button[contains(text(),'{}')]",
        "appt_avatar_img": "//div[@class='slds-card__body']//descendant::lightning-avatar",
        "description":"//textarea[@name='comments']",
        "calender_box": "//div[@class='slds-select_container']/select[@class='slds-select']",
        "current_month":"//select[@class='slds-select']/option/lightning-formatted-date-time",
        "month_year": "//select[@class='slds-select']",
        "save_cancel": "//div[@id='comment-buttons']/button[text()='{}']",
        "walkin_appt_confirmation_info": "//div[@id='confirmation-details']//div[@class='slds-text-title_caps']/lightning-formatted-date-time[text()='{}']/following::div[contains(lightning-formatted-date-time,'{}') and descendant::lightning-formatted-date-time['{}']]/following::div[contains(text(),'{}')]/following::div[text()='{}']/following-sibling::div[text()='{}']",
        "time_slot": "//lightning-formatted-date-time[text()='{}']/following::div[contains(@class,'slds-text-title_bold')]/lightning-formatted-date-time[text()='{}']/following::lightning-formatted-date-time[text()='{}']",
        "time_slot_community":"//h2[@id='header{}']/lightning-formatted-date-time[text()='{}']/following::ul/li/button[@aria-describedby='header{}']//div[(@class='time-slot-times slds-text-color_default') and lightning-formatted-date-time[text()='{}'] and lightning-formatted-date-time[contains(text(),'{}')]]",
        "appt_confirmation_text": {
            "scheduled_appt_confirmation_text": "//div[@id='confirmation-header' and div[text()='{}']]",
            "walkin_appt_confirmation_text1": '//div[@id="confirmation-header"]//div[text()="{}"]/following::p[text()="{}"]',
            "walkin_appt_confirmation_text2": "//p[contains(@class,'walkin-conf-statement-2')]",
        },
        "close_button": "//button[@class='slds-button slds-button_inverse']"
    },
    "user_dropdown": "//a[contains(@class, 'trigger-link')]/span[@class='triggerDownArrow down-arrow']", 
    
}

community_settings_locators = {
    "header_title": "//h1[@class='texttitle' and text()='My Settings']",
    "timezone": "//label[text()='Time Zone']",
    "timezone_value" : "//span[@class='slds-media__body']/span[contains(@title,'{}')]",
}

community_launchpad_locators = {
    "launchpad_tab": "//div[@class='slds-tabs_default']/descendant::li[@data-tab='true' and @title='{}']/a[text()='{}']",
    "agenda_header": "//span[@class='agendaHeader']",
    "expand_date_picker_button": "//lightning-formatted-date-time[@class='slds-align_absolute-center slds-p-vertical_small slds-text-color_inverse viewingDate']",
    "first_day_of_week": "//lightning-layout-item[1]//lightning-formatted-date-time[1][contains(text(),'{}')]",
}

contact_locators = {
    "community_login_error": "//div[contains(@class, 'slds-modal__container')]/div[contains(@class, 'modal-body')]/div[contains(text(), 'Looks like this portal user is not a member of a community or your community is down')]",
    "login_to_community": "//a[@title='Log in to Community as User']",
    "show_more_actions": "//div[contains(@class, 'actionsContainer')]/descendant::li[contains(@class, 'oneActionsDropDown')]/descendant::a[contains(@title, 'more actions')]",
}

event_locators = {
    "appointment":"//a[contains(@class,'eventBox')]//div[@class='eventDescription slds-scrollable_none']//span[contains(@class,'assistiveText')][contains(text(), '{}') and contains(text(),'{}') and contains(text(),'{}')]",
    "calendar_home": "//div[@id='calendarHome']",
    "calender_day_header": "//div[@class='calendarDayHeaders slds-grid']/strong[contains(@class,'calendarDayHeader')][contains(text(), '{}')]",
    "close_popup": "//div[contains(@class, 'calendarHome')]/descendant::section[contains(@class, 'slds-popover')]/button[@title='Close']",
    "dialog": "//section[contains(@class, 'slds-popover')]/button[@title='Close']",
    "field_value": "//div[contains(@class, 'slds-form-element__label')]/span[text()='{}']/ancestor::div[contains(@class, 'slds-form-element')]/descendant::span[text()='{}']",
    "header_title": "//div[contains(@class, 'slds-page-header__title')]/span[text()='{}']",
    "new_event_button": "//button[contains(@class, 'slds-button') and @type='button' and text()='New Event']",
    "next": "//button[contains(@class, 'slds-button') and @type='button']/span[text()='Next']",
    "next_week":"//button[@title='Next Week']",
    "refresh": "//div[@class='calendarHeader']/descendant::button[@title='Refresh']",
    "select_type": "//span[(@class='slds-form-element__label') and (text()='{}')]",
    "standard_event": {
        "date": "//fieldset/legend[text()='{}']/../div/descendant::label[text()='{}']/../descendant::input",
        "description": "//label/span[text()='Description']/following::textarea[contains(@class, 'uiInputTextArea')]",
        "event_description":"//div[contains(@class,'test-id__field-label-container')]/span[text()='{}']//following::span[@class='uiOutputTextArea' and text()='{}']",
        "footer": "//div[contains(@class,'modal-footer')]",
        "location": "//div[contains(@class, 'uiInput')][.//label[contains(@class, 'uiLabel')][.//span[text()='Location']]]//*[self::input or self::textarea]",
        "new_event_title": "//h2[contains(@class, 'title') and text()='New Event: Standard Event']",
        "save": "//div[contains(@class, 'modal-footer')]/descendant::button[contains(@class, 'slds-button') and @type='button' and @title='Save']",
        "select_field": "//div[.//span[text()='{}'] and contains(@class, 'slds-form-element') ]//select",
    },
}

modal_locators = {
    "cancel_appointment": {
        "close": "//div[contains(@class, 'slds-modal')]/descendant::button[@title='Close this window']",
        "comments": "//div[contains(@class, 'slds-modal__container')]/descendant::textarea[@name='comments']",
        "header": "//header[contains(@class, 'slds-modal__header')]/descendant::span[text()='Cancel this appointment?']",
        "button": "//div[contains(@class, 'slds-modal__container')]/descendant::button[text()='{}']",
    },
    "delete_notes_modal":{
        "close": "//button[contains(@class,'closeIcon') and @title='Close this window']"
    }
}

notes_locators = {
    "add_body": "//div[@data-placeholder='Enter a note...']",
    "add_subject": "//div[contains(@class, 'notesTitle')]/descendant::input[contains(@class,'notesTitle')]",
    "header_title": "//div[contains(@class, 'slds-page-header')]/descendant::span[text()='Notes']",
    "notes_body": "//div[@data-placeholder='Enter a note...']/p[text()='{}']",
    "notes_subject": "//div[@class='listViewContent']/descendant::li/descendant::h2[contains(@class,'title')]/span[contains(text(),'{}')]",
    "add_to_records": {
        "add_button": "//div[contains(@class, 'modal-footer')]/descendant::button/following::span[text() = 'Add']",
        "add_to_records_button": "//div[contains(@class, 'bottomBar')]/descendant::span[contains(text(), 'Add to Records')]/parent::button",
        "object_type_dropdown": "//span[text()='Pick an object']/ancestor::a",
        "object_type": "//div[contains(@class, 'entityMenuList')]/descendant::li/a[@title='{}']",
        "object_value_search": "//div[contains(@class, 'modal-container')]/descendant::input[@title='Search {}']",
        "object_value": "//div[contains(@class, 'listContent')]/descendant::li[contains(@class, 'lookup__item')]/descendant::div[@title='{}']",
        "span": "//div[contains(@class, 'modal-container')]/descendant::span[contains(@class, 'panelText')]",
    },
}

task_locators = {
    "header_title": "//h2[contains(@class, 'inlineTitle') and text()='New Task: Academic']",
}