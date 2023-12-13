   document.addEventListener("DOMContentLoaded", () => {
    const dropArea = document.getElementById("dropArea");
  
    //For Highlighting the user that 
    dropArea.addEventListener("dragover", (ev) => {
      ev.preventDefault();
      dropArea.classList.add("highlight");
    });
  
    dropArea.addEventListener("dragleave", () => {
      dropArea.classList.remove("highlight");
    });
  
    // When User Will Drop Image 
    dropArea.addEventListener("drop", (ev) => {
      ev.preventDefault();
      dropArea.classList.remove("highlight");
  
      const file = ev.dataTransfer.files[0];
      if (file) {
        handleFile(file);
      }
    });
  
    // When User will click on The Box
    dropArea.addEventListener("click", () => {
      const fileInput = document.createElement("input");
      fileInput.name ="MyName";
      fileInput.type = "file";
      fileInput.accept = "image/*, video/*";
  
      fileInput.addEventListener("change", (ev) => {
        const file = ev.target.files[0];
        if (file) {
          handleFile(file);
        }
      });
  
      document.body.appendChild(fileInput);
      fileInput.click();
      document.body.removeChild(fileInput);
    });
  
    function handleFile(file) {
      const fileType = file.type;
      const validImageTypes = ["image/jpeg", "image/png", "image/gif"];
      const validVideoTypes = ["video/mp4", "video/ogg", "video/webm"];
  
      if (validImageTypes.includes(fileType)) {
        // Display image preview
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.style.maxWidth = "500px";
        img.style.maxHeight = "500px";
        img.onload = () => {
          URL.revokeObjectURL(img.src);
        };
        dropArea.innerHTML = ""; // Clear previous content
        dropArea.appendChild(img);
      } else if (validVideoTypes.includes(fileType)) {
        // Display video preview
        const video = document.createElement("video");
        video.src = URL.createObjectURL(file);
        video.style.maxHeight = "500px";
        video.controls = true;
        video.onload = () => {
          URL.revokeObjectURL(video.src);
        };
        dropArea.innerHTML = ""; // Clear previous content
        dropArea.appendChild(video);
      } else {
        // Invalid file type
        dropArea.innerHTML = 'Invalid file type. Please upload an image or video.';
      }
    }

});
removeMedia.addEventListener("click", () =>{
      dropArea.innerHTML = '<p>Drag and Drop images or videos here</p>';
});

