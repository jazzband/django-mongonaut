function addInputFromPrevious(input, embeddedDoc){
    /* This is a fuction to insert an input after an existing
        input.  It will correclty update the id and name so the
        input can be posted as desired.

        embeddedDoc must be an array.
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
    $(newInput).attr('id', "id_" + currentName);

    if (embeddedDoc){
        embeddedDoc.push($(newInput));
    } else {
        $(newInput).insertAfter(input);
        $(newInput).before('<br />');
    }
    // Cleanly add the new input field to the DOM

    return newInput;
}

function attachButtonList(input) {
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

function attachButtonEmbedded(inputs) {
    /* Used to place the add button on the page.  Upon each click it
       copies the previous input and increments the id and name by using
       the addInputFromPrevious function. */
    var finalInput = null;
    for (var j = 0; j < inputs.length; j++) {
        if (j + 1 == inputs.length) {
            finalInput = inputs[j];
        }
    }
    var finalInputName = $(finalInput).attr('name');
    var button = "<div class='btn btn-primary " + finalInputName + "'>add</div>";
    var embeddedParentDIV = inputs.parent().parent().parent();
    $(button).insertAfter(finalInput);


    $(document).on('click', "div[class~=" + finalInputName +"]", function(e){
        e.preventDefault();
        var addedInputs = [];
        var embeddedDocs = [];

        for (var j = 0; j < inputs.length; j++) {
            var newInput = addInputFromPrevious($(inputs[j]), embeddedDocs);
            addedInputs.push(newInput);
        }

        var newEmbeddedDoc = $("<div class='well'></div>");
        for (var k = 0; k < embeddedDocs.length; k++) {
            var newFieldSet = $("<div class='clearfix'></div>");
            var newInputField = embeddedDocs[k];
            var newLabel = "<label for='" + newInputField.attr("id") + "'>" + newInputField.attr("name") + "</label>";

            newFieldSet.append(newLabel);
            newFieldSet.append(newInputField);
            newEmbeddedDoc.append(newFieldSet);

            if (k + 1 == embeddedDocs.length) {
                finalInput = newInputField;
            }
        }

        // Move button to next document
        $("[class*='btn btn-primary " + finalInputName + "']").remove();
        $(button).insertAfter(finalInput);

        $(embeddedParentDIV).append(newEmbeddedDoc);
        inputs = addedInputs;
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
    $(listDiv).wrapAll("<div class='well' />");
    listDiv = $(listDiv[listDiv.length - 1]);
    initialInputs.push(listDiv.children('div').children('.listField'));
}

// Process embedded documents
var embeddedFields = $('.embeddedField');
var embeddedClasses = [];

// Group Embedded docs together
for (var i = 0; i < embeddedFields.length; i++) {
    var field = embeddedFields[i];
    var allClasses = $(field).attr('class').split(' ');

    for (j = 0; j < allClasses.length; j++) {
        var embeddedClass = allClasses[j];
        if ($.inArray(embeddedClass, ['listField', 'embeddedField', 'span6', 'xlarge', '']) != -1) {
            continue;
        }
        // Make sure to only get the base class from the group of embedded fields
        if ($.inArray(embeddedClass, embeddedClasses) == -1) {
            embeddedClasses.push(embeddedClass);
        }
    }
}

for (var i = 0; i < embeddedClasses.length; i++){
    var inputDivs = $("[class~='" + embeddedClasses[i] + "']").parent().parent();
    var idBase = embeddedClasses[i];

    $(inputDivs).wrapAll("<div class='well' />");
    $(inputDivs[0]).parent().before("<div>" + embeddedClasses[i] + "</div>");
}

// Attach the buttons to the correct fields.
var alreadyAttached = [];

// Go in reverse order to correctly attach buttons
for (var i = initialInputs.length - 1; i >= 0; i--) {
    var inputField = initialInputs[i];

    // Remove the trailing number from our name so we can track what has
    // already been added.
    var inputNameArray = inputField.attr("name").split("_");
    inputNameArray.pop();
    var newInputName = inputNameArray.join("_");

    // Make sure we do not add a button to the same field twice
    if ($.inArray(newInputName, alreadyAttached) != -1) {
        continue;
    }

    if (inputField.hasClass("embeddedField")) {
        var newFields = $("[class*='" + inputField.attr("class") + "']");
        attachButtonEmbedded(newFields);
    } else {
        attachButtonList(initialInputs[i]);
    }
    alreadyAttached.push(newInputName);
}

// Remove any empty divs leftover by the re-organization of the page.
$(document).ready(function() {
    $('div:empty').remove();
    var allDivs = $("div");
    allDivs.each( function(index, element) {
        if (element.innerHTML === "") {
            $(element).remove();
        }
    });
});
