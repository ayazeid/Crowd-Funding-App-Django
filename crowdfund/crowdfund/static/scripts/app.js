var picPrompts = $(".cf-dy-hidden");
var fundProgress = $(".fund-progress");

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

// function getpercentage(progressBar) {
//   console.log(progressBar);
//   // percentage = currentFund / totalTarget
//   // fundProgress.style.width = `${percentage}%`
// //   aria-valuenow = percentage
// }
