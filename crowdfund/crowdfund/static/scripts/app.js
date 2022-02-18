var picPrompts = $(".cf-dy-hidden");

// Dynamic picture prompt fields
function dynamicPicPromptsDisplay() {
  for (let prompt_id = 0; prompt_id < picPrompts.length; prompt_id++) {
    if (prompt_id > 0 && picPrompts[prompt_id - 1].files.length === 0) {
      picPrompts[prompt_id].style.display = "none";
    } else {
      picPrompts[prompt_id].style.display = "block";
    }
  }
}

// Reaveal more prompts on uploading file
picPrompts.on("change", () => {
  console.log("hi");
  dynamicPicPromptsDisplay();
});

// Show only the first prompt on load
dynamicPicPromptsDisplay();

//  Home Page Image Slider
let slideIndex = 1;
let myIndex = 0;

function showDivs(n) {
  let i;
  const x = document.getElementsByClassName("mySlides");
  if (n > x.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = x.length;
  }
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  x[slideIndex - 1].style.display = "block";
}

showDivs(slideIndex);

function plusDivs(n) {
  showDivs((slideIndex += n));
}
function carousel() {
  let i;
  const x = document.getElementsByClassName("mySlides");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  myIndex++;
  if (myIndex > x.length) {
    myIndex = 1;
  }
  x[myIndex - 1].style.display = "block";
  setTimeout(carousel, 5000); // Change image every 5 seconds
}
carousel();
