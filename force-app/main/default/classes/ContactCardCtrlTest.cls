/*
    Copyright (c) 2020, Traction Sales And Marketing Inc.
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    
    * Redistributions of source code must retain the above copyright
      notice, this List of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this List of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Salesforce.org nor the names of
      its contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.
 
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
    COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
    POSSIBILITY OF SUCH DAMAGE.
*/
/**
 * @author  Heather Purvis, Traction on Demand
 * @date    2020-03-19
 */
@IsTest
public with sharing class ContactCardCtrlTest {
    @IsTest
    static void getContactInfo() {
        Account account = TestUtils.createCommunityAccount('Test Account', TRUE);

        Contact testContact = TestUtils.createCommunityContact('Test Contact', FALSE);
        testContact.AccountId = account.Id;
        insert testContact;

        User communityUser = TestUtils.createCommunityUser(Constants.COMMUNITY_PROFILE_NAME, testContact.Id);

        System.runAs(new User(Id = UserInfo.getUserId())){
            insert communityUser;
        }

        ContactCardCtrl.ContactData currentContactAndUser;
        Test.startTest();
        System.runAs(communityUser) {
            currentContactAndUser = ContactCardCtrl.getContactInfo();
        }
        Test.stopTest();

        System.assertNotEquals(null, currentContactAndUser.contact, 'Expected contact to be returned');
        System.assertNotEquals(null, currentContactAndUser.user, 'Expected user to be returned');
        System.assertEquals(testContact.Id, currentContactAndUser.contact.Id, 'Expected contact to be returned');
        System.assertEquals(communityUser.Id, currentContactAndUser.user.Id, 'Expected user to be returned');
    }

    @IsTest
    static void getUserInfo() {
        ContactCardCtrl.ContactData currentContactAndUser;
        Test.startTest();
        currentContactAndUser = ContactCardCtrl.getContactInfo();
        Test.stopTest();

        System.assertNotEquals(null, currentContactAndUser.contact, 'Expected contact to be returned');
        System.assertNotEquals(null, currentContactAndUser.user, 'Expected user to be returned');
    }
}