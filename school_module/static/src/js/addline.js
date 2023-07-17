function addRow(){
    // Get the table element in which you want to add row
    let table = document.getElementById("tableBody");
   //Create a row element

   let row = document.createElement("tr");

   //Create cells
   let c1 = document.createElement("td");
   let c2 = document.createElement("td");
   let c3 = document.createElement("td");

   //Create Input Elements
   let input1 = document.createElement("input");
   input1.name = "subject_name_"+table.rows.length;//Assign Unique Name
   input1.className = "form-control"
   var array = ["Select Priority","Mandatory","Optional"];
   
   var input2 = document.createElement("select");
   input2.id = "mySelect";
   input2.className = "form-select form-control"
   input2.name = "sub_priority_"+table.rows.length;//Assign Unique Name

   let input3 = document.createElement("img");
   input3.src = "/school_module/static/src/image/delete.png"
   input3.type = "button";
   input3.value = "Delete";

   //Input attribute
   input1.type = "text";

    for(var i=0; i <array.length; i++){
        var option = document.createElement("option");
        option.value = array[i];
        option.text = array[i];
        input2.appendChild(option);
    }

    // Eventlistner That will delete row 
    input3.addEventListener("click",function(){
        table.removeChild(row);
    });

    //Let append the input tag in cells
    c1.appendChild(input1);
    c2.appendChild(input2); 
    c3.appendChild(input3);
   //Append cell in created row
   row.appendChild(c1);
   row.appendChild(c2);
   row.appendChild(c3);

   //Append row to table
   table.appendChild(row);
   
   var a = document.getElementById("tableBody");
   var rows = a.rows.length;
   let row_count =  document.getElementById("subject_count");
   row_count.value = rows;
}

var loadFile = function(event) {
    var output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) // free memory
    }
  };
  
