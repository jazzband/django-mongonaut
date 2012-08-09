function addInputFromPrevious(input){
    /* This is a fuction to insert an input after an existing
        input.  It will correclty update the id and name so the
        input can be posted as desired.
     */
    var newInput = input.clone();
    var currentNameArray = newInput.attr('name').split('_');
    var lastArrayString = currentNameArray.pop();
    var newIdNum = 1;
    var baseName = currentNameArray.join("_");
    var currentName = "";

    // Compute the name attribute for the input
    if (!isNaN(lastArrayString)) {
        newIdNum += +lastArrayString;
        currentName = baseName + '_' + newIdNum;
        newInput.attr('name', currentName);
    } else {
        if (currentNameArray.length > 0) {
            baseName = baseName + "_" + lastArrayString;
            currentName = baseName + "_" + newIdNum;
            newInput.attr('name', currentName);
        } else {
            baseName = lastArrayString;
            currentName = baseName + "_" + newIdNum;
            newInput.attr('name', currentName);
        }
    }

    // Default to no value for newly added fields
    var inputType = $(newInput).attr('type');
    if (inputType == "text") {
        $(newInput).attr('value', '');
    } else if (inputType == "checkbox" ) {
        $(newInput).attr('checked', false);
    } else {
        $(newInput).children("option[value='']").attr('selected', 'selected');
    }

    // Cleanly add the new input field to the DOM
    $(newInput).attr('id', "id_" + currentName);
    $(newInput).insertAfter(input);
    $(newInput).before('<br />');
    return newInput;
}

function attachButton(input) {
    /* Used to place the add button on the page.  Upon each click it
       copies the previous input and increments the id and name by using
       the addInputFromPrevious function. */
    var currentInput = input;
    var inputName = currentInput.attr('name');
    var button = "<div class='btn btn-primary " + inputName + "'>add</div>";
    $(button).insertAfter(currentInput);

    $(document).on('click', "div[class~=" + inputName +"]", function(e){
        e.preventDefault();
        var newInput = addInputFromPrevious(currentInput);
        currentInput = newInput;
    });
}

var listFields = $('.listField');
var listClasses = [];
var initialInputs = [];
for (var i = 0; i < listFields.length; i++) {
    var field = listFields[i];
    var listClass = $(field).attr('class').split(' ').pop();

    // Make sure to only get the base class from the grop of list fields
    if ($.inArray(listClass, listClasses) == -1) {
        listClasses.push(listClass);
    }
}

// Get the last list item in the group
for (var i = 0; i < listClasses.length; i++) {
    var inputs = $('.' + listClasses[i]);
    var listDiv = inputs.parent().parent();
    listDiv = $(listDiv[listDiv.length - 1]);
    initialInputs.push(listDiv.children('div').children('.listField'));
}

// Attach the button to the last item in the group.
for (var i = 0; i < initialInputs.length; i++) {
    attachButton(initialInputs[i]);
}