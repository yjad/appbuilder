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
            // let FROM = document.forms["model_form"]["from_date"].value;
            // let TO = document.forms["myForm"]["to_date"].value;
            FROM=  document.getElementById('course_start_date').value;
            TO=  document.getElementById('course_end_date').value;
            console.log(FROM, TO)
            if (FROM > TO){
                // var from_dateError = document.querySelector("#course_end_date"+"span.error")
                // showError(from_dateError)
                console.log("Error - Invalidae date range .....", FROM , TO)
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
  
