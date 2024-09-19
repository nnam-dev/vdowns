document.getElementById('downloadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.getElementById('videoUrl').value;
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerText = data.error;
        } else {
            document.getElementById('result').innerHTML = `<a href="${data.download_link}" download>Download Video</a>`;
        }
    });
});
