function remove_task(event) {
    const id = event.target.parentNode.id
    fetch('/remove/' + id).then(response => window.location.reload())
}