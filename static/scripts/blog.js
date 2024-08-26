function deleteMessage() {
  const btns = document.querySelectorAll('.js-delete-btn')
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      const {messageId} = btn.dataset
      
      fetch('http://127.0.0.1:5500/api/message', {
        method: 'DELETE',
        body: JSON.stringify({id: parseInt(messageId)}),
        headers: {"Content-Type": "application/json"}
      })

      const message = document.querySelector(`.js-message-${messageId}`)
      message.remove()
    })
  })
}

function editMessage() {
  const editButtons = document.querySelectorAll('.js-edit-btn')

  editButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const {messageId} = btn.dataset
      
      const message = document.querySelector( `.js-message-${messageId}`)

      message.classList.add('edit-mode')

      console.log('edit')

    })
  })      
}

function saveMessage() {
  const saveButtons = document.querySelectorAll('.js-save-btn')

  saveButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const {messageId} = btn.dataset
      
      const message = document.querySelector( `.js-message-${messageId}`)

      message.classList.remove('edit-mode')

      console.log('save')
    })
  })

}

window.addEventListener('load', () => {
  deleteMessage()
  editMessage()
  saveMessage()
})
