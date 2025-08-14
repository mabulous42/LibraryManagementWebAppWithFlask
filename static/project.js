let password = document.getElementById('user-password')
let showpassword = document.getElementById("show-password")
let hidepassword = document.getElementById("hide-password")

hidepassword.style.display = 'none'


function showPassword() {
    if (password.type == 'password') {
        password.type = 'text' 
        showpassword.style.display = 'none'         
        hidepassword.style.display = 'block'         
    } 
}

function hidePassword() {
    if (password.type == 'text') {
        password.type = 'password' 
        showpassword.style.display = 'block'         
        hidepassword.style.display = 'none'         
    } 
}
