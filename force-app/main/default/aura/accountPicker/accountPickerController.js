/**
 * Created by Heather Purvis on 2020-03-24.
 */
({
    /**
     * @description Initialises the component by finding the relevant accounts available for this user
     * @param component
     * @param event
     * @param helper
     */
    init: function (component, event, helper) {
        helper.getAccountData(component, event, helper);
    },

    /**
     * @description Handles when a user changes the selected authority. Finds the hospital list for the new authority
     *              and resets the division
     * @param component
     * @param event
     * @param helper
     */
    handleAuthorityChange: function (component, event, helper) {
        helper.getHospitals(component, event, helper);
        component.set("v.selectedHospital", null);
        component.set("v.selectedDivision", null);
        component.set("v.divisions", null);
        helper.fireDivisionSetEvent(component);
    },

    /**
     * @description Handles when a user changes the selected hospital. Finds the division list for the new hospital.
     *              Fires an event to alert that no division is currently selected
     * @param component
     * @param event
     * @param helper
     */
    handleHospitalChange: function (component, event, helper) {
        helper.getDivisions(component, event, helper);
        component.set("v.selectedDivision", null);
        helper.fireDivisionSetEvent(component);
    },

    /**
     * @description Fires an event to alert other components of the division selected
     * @param component
     * @param event
     * @param helper
     */
    handleDivisionChange: function (component, event, helper) {
        helper.fireDivisionSetEvent(component);
    },

})