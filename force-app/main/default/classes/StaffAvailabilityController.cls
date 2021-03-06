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
 * @author Christian Wico - cwico@tractionondemand.com
 * @description Staff Availability Component for communities
 */

public with sharing class StaffAvailabilityController {

	static final Integer MAX_RESULTS = 5;
	static final Integer DEFAULT_DAYS_AHEAD = 14;
	static final String DEFAULT_AVAILABILITY = 'Available';

	static Id userId = UserInfo.getUserId();
    static User user;

	static  {
		user = [SELECT Id, ContactId, Contact.Name, Contact.AccountId, Contact.Account.Name FROM User WHERE Id = :userId];
	}

	// returns the next 14 days availability
	@AuraEnabled
	public static AssignmentData getAssignmentData(Id contactId) {
		AssignmentData data = new AssignmentData();
		data.contactId = !String.isBlank(contactId)? contactId:user.ContactId;
		List<Contact> contacts = [SELECT Id, FirstName, LastName, AccountId, Account.Name  FROM Contact WHERE Id = :data.contactId];
		data.contact = contacts.size() > 0? contacts[0]:new Contact();
		data.daysAhead = DEFAULT_DAYS_AHEAD;
		data.startDate = Date.today();
		data.endDate = Date.today().addDays(DEFAULT_DAYS_AHEAD);
		data.accountName = data.contact.Account.Name;
		data.accountId = data.contact.AccountId;
		data.assignments = new List<Assignment__c>();
		data.assignmentRecords =  [
				SELECT
						Date__c,
						Available__c,
						Care_Facility__r.Name,
						Staff__c,
						LastModifiedDate
				FROM Assignment__c
				WHERE
				Staff__c = :data.contactId AND
				Date__c >= :data.startDate AND
				Date__c <= :data.endDate
				ORDER BY Date__c
		];
		for (Integer i = 0; i < data.daysAhead; i++) {
			Date d = Date.today().addDays(i);
			Assignment__c assignment = new Assignment__c(
					Date__c = d,
					Available__c = DEFAULT_AVAILABILITY,
					Care_Facility__c = data.AccountId,
					Staff__c = data.contactId
			);
			// scan existing assignment record for the date
			for (Assignment__c record: data.assignmentRecords) {
				if (record.Date__c == d) {
					assignment = record;
					break;
				}
			}
			data.assignments.add(assignment);
		}
		return data;
	}

	@AuraEnabled
	public static Assignment__c save(Assignment__c assignment) {

		SecureDml upsertObject = new SecureDml();
		try {
			upsertObject.dmlUpsert(Assignment__c.SObjectType, new List<Assignment__c> {assignment}, Assignment__c.Id);
		}
		catch(Exception e) {
			throw new AuraHandledException(e.getMessage() + ' : RECORD -> ' + JSON.serializePretty(assignment));
		}

		return [SELECT Date__c, Available__c, Care_Facility__r.Name, Staff__c, LastModifiedDate FROM Assignment__c WHERE Id =:assignment.Id LIMIT 1];
	}

	// custom lookup for sfdc-ui-lookup-lwc - https://github.com/pozil/sfdc-ui-lookup-lwc/tree/master/src-sample
	@AuraEnabled(Cacheable=true)
	public static List<LookupSearchResult> searchAccountLookup(String searchTerm, List<String> selectedIds) {
		// Prepare query paramters
		searchTerm += '*';

		// Execute search query
		List<List<SObject>> searchResults = [
				FIND :searchTerm
				IN ALL FIELDS
						RETURNING
						Account(Id, Name, BillingCity WHERE id NOT IN :selectedIds)
				LIMIT :MAX_RESULTS
		];

		// Prepare results
		List<LookupSearchResult> results = new List<LookupSearchResult>();

		// Extract Accounts & convert them into LookupSearchResult
		String accountIcon = 'standard:account';
		Account[] accounts = (List<Account>) searchResults[0];
		for (Account account : accounts) {
			results.add(
					new LookupSearchResult(
							account.Id,
							'Account',
							accountIcon,
							account.Name,
							'Account • ' + account.BillingCity
					)
			);
		}


		// Optionnaly sort all results on title
		results.sort();

		return results;
	}




	public class AssignmentData {

		@AuraEnabled
		public Integer daysAhead {get;set;}

		@AuraEnabled
		public Id contactId {get;set;}

		@AuraEnabled
		public Contact contact {get;set;}

		@AuraEnabled
		public Id accountId {get;set;}

		@AuraEnabled
		public String accountName {get;set;}

		@AuraEnabled
		public Date startDate {get;set;}

		@AuraEnabled
		public Date endDate {get;set;}

		@AuraEnabled
		public List<Assignment__c> assignments {get; set;}

		@AuraEnabled
		public List<Assignment__c> assignmentRecords {get;set;}

	}

}