picPrompts = document.getElementsByClassName(".cf-dy-hidden");

function dynamicPicPromptsDisplay() {
  for (let prompt_id = 0; prompt_id < picPrompts.length; prompt_id++) {
    if (prompt_id > 0 && picPrompts[prompt_id - 1].files.length === 0) {
      picPrompts[prompt_id].style.display = "none";
    } else {
      picPrompts[prompt_id].style.display = "block";
    }
  }
}

picPrompts.onchange = (event) => {
  console.log(event);
  dynamicPicPromptsDisplay();
};
