function deleteTask() {
  const tasks = document.querySelectorAll('.js-task')

  tasks.forEach(task => {
    const {taskId} = task.dataset

    const deleteBtn = document.querySelector(`.js-delete-btn-${taskId}`)

    deleteBtn.addEventListener('click', () => {
      fetch('http://127.0.0.1:5500/api/task', {
        method: 'DELETE',
        body: JSON.stringify({id: taskId}),
        headers: {"Content-Type" : 'application/json'}
      })

      task.remove()
    })

  })
}

function editTask() {
  const tasks = document.querySelectorAll('.js-task')

  tasks.forEach(task => {
    const {taskId} = task.dataset
    
    const editBtn = document.querySelector(`.js-edit-btn-${taskId}`)
    
    editBtn.addEventListener('click', () => {
      task.classList.add('edit-mode')

    })

  })

}

function saveTask() {
  /*fetch('http://127.0.0.1:5500/api/task', {
    method: 'PUT',
    body: JSON.stringify({id: taskId}),
    headers: {"Content-Type" : 'application/json'}
  })*/

  const tasks = document.querySelectorAll('.js-task')

  tasks.forEach(task => {
    const {taskId} = task.dataset
    
    const saveBtn = document.querySelector(`.js-save-btn-${taskId}`)
    
    saveBtn.addEventListener('click', () => {
      task.classList.remove('edit-mode')

    })

  })

}

window.addEventListener('load', () => {
  deleteTask()
  editTask()
  saveTask()
})
