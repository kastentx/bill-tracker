var lastClicked;

function toggleForm(sentence)
{
	var submissionForm = document.getElementById("submission");

	if (submissionForm.style.visibility != "visible")
	{
		submissionForm.style.visibility = "visible";
		sentence.style.backgroundColor = "yellow";
		lastClicked = sentence;
	}
	else
	{
		submissionForm.style.visibility = "hidden";
		lastClicked.style.backgroundColor = "inherit";
	}
}

function submitAnnotation(text)
{
	var annotationText = text.value;
	var submissionForm = document.getElementById("submission");

	submissionForm.style.visibility = "hidden";
	lastClicked.style.backgroundColor = "inherit";
	alert(annotationText + " submitted as annotation for sentence " + lastClicked.id + ".");
	text.value = "";

}