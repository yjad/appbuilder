const form_title = document.getElementsByClassName('panel-title');

if (form_title.length > 0){
    console.log("form title: "+form_title, form_title.length);
    // console.log("form title: "+form_title[0].innerHTML);
    const form = document.querySelector("form");
    form.addEventListener("submit", (event) => {
        console.log("submit ....");
        if (!validateForm(form_title[0].innerHTML)){
            event.preventDefault(); // stop the form processing
        }   
        // event.preventDefault(); // stop the form processing
    });
} 


function showError(formFieldError) {
    // const from_dateError = document.querySelector("#"+field_name + "span.error");
    
    console.log("Error Date Range - from showError ..."+formFieldError);
    formFieldError.textContent = "Error Date Range"
    // Set the styling appropriately
    from_dateError.className = "error active";
}


function validateForm(form_title) {
    switch(form_title) {
        case "Add Courses Per Cycle":
            // let FROM = document.forms["model_form"]["course_start_date"].value;
            // let TO = document.forms["myForm"]["course_end_date"].value;
            FROM=  document.getElementById('course_start_date').value;
            TO=  document.getElementById('course_end_date').value;
            console.log("Dates Entered: ", FROM, TO)
            if (FROM > TO){
                try{
                    document.getElementById('course_end_date').enabled = true;
                    // var x =  document.getElementById('modal-confirm').value;
                    // var _dateError = document.querySelectorAll(".alert.alert-danger");
                    // var _dateError = document.querySelectorAll(".alert");
                    // console.log ("length: ", _dateError.length, 'x:', x)
                    // _dateError[0].innerHTML = 'Yahia ....'
                    // alert("This is an alert message box."); //worked
                    // var field = document.getElementById('course_end_date');
                    // field.innerHTML = field.value + "  **** Invalid Date Range"
                    // console.log ("field: ", field, "new value", field.innerHTML)
                    var x = document.getElementsByClassName('help-block');
                    console.log('alert.alert-danger', x);
                    x[3].outerText = 'Invalid Date Range';
                    

                } catch(err){
                    console.log("Error - Invalid query selector");
                }
                // _dateError.innerHTML = 'Invalid date range'
                // showError(from_dateError)
                
                return false;       // stop sending the form
            } else {
                return true;        // validation OK
            }
            break;
        // case y:
            // code block
            // break;
        // default:
            // code block
    }
    
}
  
