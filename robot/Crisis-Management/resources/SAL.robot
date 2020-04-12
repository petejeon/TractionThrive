*** Settings ***

Resource        cumulusci/robotframework/Salesforce.robot
Library         DateTime
Library         SAL.py
Library         cumulusci.robotframework.PageObjects
...             robot/SAL/resources/ContactPageObject.py
...             robot/SAL/resources/CommunityHomePageObject.py
...             robot/SAL/resources/CommunitySettingsPageObject.py
...             robot/SAL/resources/ApptManagerPageObject.py


*** Variables ***
${PRINT_PACKAGE}        true

*** Keywords ***

Open Test Browser And Print Package Details
    [Documentation]         Opens the test browser and runs a keyword that prints package details from setup
    Open Test Browser
    Run Keyword If          '${PRINT_PACKAGE.lower()}' == 'true'     Capture SAL and EDA package details

Capture SAL and EDA package details
    [Documentation]         Captures the package details from SAL setup page and prints it to console
    Set Global Variable                 ${PRINT_PACKAGE}            false
    Wait Until Loading Is Complete
    Go To Setup Home
    Wait For New Window                 Home | Salesforce
    Switch Window                       Home | Salesforce
    Wait Until Loading Is Complete
    Populate Placeholder                Quick Find          Installed Packages
    Wait Until Loading Is Complete
    Select Frame With Value             Installed Packages ~ Salesforce -
    Print Package Details
    Unselect Frame

Capture Screenshot and Delete Records and Close Browser
    [Documentation]         Captures screenshot if a test fails, deletes session records and closes the browser
    Run Keyword If Any Tests Failed      Capture Page Screenshot
    Close Browser
    Delete Session Records

Capture Screenshot and Delete Records and Close Browser in Tests
    [Documentation]         Captures screenshot if a test fails, deletes session records and closes the browser in the Test case level
    Run Keyword If Test Failed     Capture Page Screenshot
    Close Browser
    Delete Session Records

API Create Advising Or Walkin Appointment
    [Documentation]
    ...                     Creates an advising or walkin appointment through API. Returns dictionary representing the created advising appointment
    ...
    ...                     Required parameters are:
    ...
    ...                     |   location            |   value of Location field. Current existing values: 'In person' and 'By phone'    |
    ...                     |   advising_type       |   value of Topic field. Ex: 'Academic'    |
    ...                     |   advising_topic      |   value of Subtopic field. Ex: 'Degree Planning', 'Grade Concerns'    |
    ...                     |   advising_appt_type  |   value of Appointment type. Ex: 'Scheduled', 'Walk-In'              |
    ...                     |   StartDate           |   Start time of the appointment. Format should be YYYY-MM-DD HH:MI:SS |
    ...                     |   EndDate             |   End time of the appointment. Format should be YYYY-MM-DD HH:MI:SS   |
    ...                     |   user                |   value of a user.Ex: 'DevAdmin User','DevTest Advisor'               |
    ...                     |                       |   Any additional field-value pairs can be passed too  |
    [Arguments]             ${location}   ${advising_type}   ${advising_topic}   ${advising_appt_type}   ${user}
    ...                     ${StartDate}    ${EndDate}    &{fields}

    ${ns} =                 Get SAL namespace prefix
    ${description} =        Generate Random String
    ${end_date} =           Convert Time To UTC Timezone    ${EndDate}
    ${name} =               Set Variable    ${advising_type} - ${advising_topic}
    ${organizer_id} =       API Get Id      User        Name        ${user}
    ${start_date} =         Convert Time To UTC Timezone    ${StartDate}

    ${advisee_record} =     API Get Id      Case        Subject     Andy Young Advisee Record
    ${attendee_id} =        API Get Id      User        Name        Andy Young

    ${adv_appt_id} =        Salesforce Insert   ${ns}Appointment__c
    ...                         ${ns}Description__c=${description}
    ...                         ${ns}EndDateTime__c=${end_date}
    ...                         ${ns}Location__c=${location}
    ...                         Name=${name}
    ...                         OwnerId=${organizer_id}
    ...                         ${ns}StartDateTime__c=${start_date}
    ...                         ${ns}Subtopic__c=${advising_topic}
    ...                         ${ns}Topic__c=${advising_type}
    ...                         ${ns}Type__c=${advising_appt_type}
    ...                         &{fields}
    &{adv_appt} =           Salesforce Get      ${ns}Appointment__c   ${adv_appt_id}

    ${adv_attendee_id} =    Salesforce Insert   ${ns}AppointmentAttendee__c
    ...                         ${ns}AdviseeRecord__c=${advisee_record}
    ...                         ${ns}Appointment__c=&{adv_appt}[Id]
    ...                         ${ns}Attendee__c=${attendee_id}
    ...                         ${ns}Role__c=Attendee

    ${adv_organizer_id} =   Salesforce Insert   ${ns}AppointmentAttendee__c
    ...                         ${ns}Appointment__c=&{adv_appt}[Id]
    ...                         ${ns}Attendee__c=${organizer_id}
    ...                         ${ns}Role__c=Organizer

    [return]                &{adv_appt}

API Create Non-Advising Event
    [Documentation]
    ...                     Creates an non-advising event through API. Returns dictionary representing the created non-advising event
    ...
    ...                     Required parameters are:
    ...
    ...                     |   location    |   value of Location field. Any text value is accepted |
    ...                     |   subject     |   value of Subject field. Ex: 'Call', 'Email', 'Meeting' etc  |
    ...                     |   StartDate   |   Start time of the event. Format should be YYYY-MM-DD HH:MI:SS   |
    ...                     |   EndDate     |   End time of the event. Format should be YYYY-MM-DD HH:MI:SS |
    ...                     |               |   Any additional field-value pairs can be passed too  |
    [Arguments]             ${location}     ${subject}    ${StartDate}    ${EndDate}    &{fields}
    ${description} =        Generate Random String
    ${record_type_id} =     Get Record Type Id  Event  Standard
    ${owner_id} =           API Get Id      User        Name        DevAdmin User
    ${start_date} =         Convert Time To UTC Timezone    ${StartDate}
    ${end_date} =           Convert Time To UTC Timezone    ${EndDate}

    ${nonadv_event_id} =    Salesforce Insert   Event
    ...                         Location=${location}
    ...                         Subject=${subject}
    ...                         StartDateTime=${start_date}
    ...                         EndDateTime=${end_date}
    ...                         Description=${description}
    ...                         OwnerId=${owner_id}
    ...                         RecordTypeId=${record_type_id}
    ...                         IsVisibleInSelfService=true
    ...                         &{fields}
    &{nonadv_event} =       Salesforce Get      Event   ${nonadv_event_id}
    [return]                &{nonadv_event}

API create availability
    [Documentation]         Creates an availability block for the given start and end times with additional details through API
    [Arguments]             ${type}     ${StartDate}    ${EndDate}      ${duration}
    ...                     ${recurrenceEnd}     ${interval}     ${daysofweek}

    ${record_type_id} =     Get Record Type Id  Event  AdvisingTime
    ${owner_id} =           API Get Id      User        Name        DevAdmin User
    ${start_date} =         Convert time to UTC timezone        ${StartDate}
    ${end_date} =           Convert time to UTC timezone        ${EndDate}

    ${availability_id} =    Salesforce Insert   Event
    ...                         DurationInMinutes=${duration}
    ...                         EndDateTime=${end_date}
    ...                         IsRecurrence=true
    ...                         IsVisibleInSelfService=true
    ...                         OwnerId=${owner_id}
    ...                         RecordTypeId=${record_type_id}
    ...                         RecurrenceDayOfWeekMask=${daysofweek}
    ...                         RecurrenceEndDateOnly=${recurrenceEnd}
    ...                         RecurrenceInterval=${interval}
    ...                         RecurrenceStartDateTime=${start_date}
    ...                         RecurrenceType=RecursWeekly
    ...                         StartDateTime=${start_date}
    ...                         Subject=API recurring
    ...                         Type=${type}

API Get Appointment Id 
    [Documentation]         Returns the ID of a record identified by the given field_name and field_value input for a specific object
    ...                     The Appointment Id is retrieved based on the Attendee name in the community
    [Arguments]             ${obj_name}    ${field_name}     ${field_value}
    @{records} =            Salesforce Query      ${ns}${obj_name}
    ...                         select=${ns}Appointment__c
    ...                         ${ns}${field_name}=${field_value}
    &{Appointment__c} =                 Get From List  ${records}  0
    [return]                &{Appointment__c}[${ns}Appointment__c]

API Get Id
    [Documentation]         Returns the ID of a record identified by the given field_name and field_value input for a specific object
    [Arguments]             ${obj_name}    ${field_name}     ${field_value}
    @{records} =            Salesforce Query      ${obj_name}
    ...                         select=Id
    ...                         ${field_name}=${field_value}
    &{Id} =                 Get From List  ${records}  0
    [return]                &{Id}[Id]

API Get Case Id
    [Documentation]         Returns the ID of a case identified by the given field_name and field_value input for a specific object
    ...                     This returns the id of the case    
    [Arguments]             ${obj_name}    ${field_name}     ${field_value}
    @{records} =            Salesforce Query      ${obj_name}
    ...                         select=Id
    ...                         ${field_name}=${field_value}
    &{Id} =                 Get From List  ${records}  0
    [return]                &{Id}[Id]

API Get User Timezone
    [Documentation]         Returns the timezone of a User identified by the given field_name and field_value input for a specific object   
    [Arguments]             ${obj_name}    ${field_name}     ${field_value}
    ${ns} =                 Get SAL namespace prefix
    @{records} =            Salesforce Query      ${obj_name}
    ...                         select=Id,TimeZoneSidKey
    ...                         ${field_name}=${field_value}
    &{Id} =                 Get From List  ${records}  0
    &{user_info} =          Salesforce Get   User   &{Id}[Id]
    [return]                &{user_info}

Get Users
    [Documentation]         Returns the ID of a record identified by the given field_name and field_value input for a specific object
    ...                     This returns the users
    Go To Setup Home
    Wait For New Window                 Home | Salesforce
    Switch Window                       Home | Salesforce
    Wait Until Loading Is Complete
    Populate placeholder users          Quick Find          Users
    Wait Until Loading Is Complete
    Select Frame With Value             All Users ~ Salesforce -

Login As Devtest Advisor
    Get Users
    Login as devtest advisor user       Login
    Wait For New Window                 Home | Salesforce
    Get Window Handles
    Switch Window                       title=Home | Salesforce

API Get Name Based on Id
    [Documentation]         Returns the Name of a record identified by the given field_name and field_value input for a specific object
    [Arguments]             ${obj_name}    ${field_name}     ${field_value}
    @{records} =            Salesforce Query      ${obj_name}
    ...                         select=Name
    ...                         ${field_name}=${field_value}
    &{Name} =               Get From List  ${records}  0
    [return]                &{Name}[Name]

Go to community
    [Documentation]             Go to the given CONTACT_ID detail page and log in to community as that user
    [Arguments]                 ${contact_id}

    Go to record home           ${contact_id}
    ${contact_name} =           API Get Name Based on Id      Contact     Id      ${contact_id}
    Go to tab                   ${contact_name}   
    Current page should be      Detail      Contact
    Login to community as user
    Current page should be      Home        Community

Update advisee timezone in community
    [Documentation]             Go to user profile settings, update the timezone to the given value and return to Community Home. 
    ...                         Timezone parameter needs to be passed in the correct format: ex. America/Los_Angeles                       
    [Arguments]                 ${timezone}  ${menu}

    Load page object            Home        Community
    Go to my settings
    Current page should be      Settings    Community
    Update timezone             ${timezone}
    Click save button           
    Close toast message         toast_close_community
    Go to community menu        ${menu}