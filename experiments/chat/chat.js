const backend = 'https://ucm.dev/chat';

async function send_message(event) {
	event.preventDefault();
	const text = document.getElementById('input').innerHTML.trim();
	if(!text) {
		return;
	}
	const body = JSON.stringify({message: text});
	try {
		const response = await fetch(backend, {
			method: 'POST',
			body,
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if(response.ok) {
			console.log('Message sent!');
		}
	} catch(error) {
		console.error(error);
	}
	document.getElementById('input').innerHTML = '';
	return false;
}

function setup() {
    const form = document.getElementById('input-form');

    form.addEventListener('submit', function(event) {
      event.preventDefault();
      console.log('Form submitted!');
    });
}

setup()
