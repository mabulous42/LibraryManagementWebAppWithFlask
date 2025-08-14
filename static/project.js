let password = document.getElementById('user-password')

function showAndHidePassword() {
    if (password.type == 'password') {
        password.type = 'text'   
        
    } else {
        password.type = 'password'   
    }
}
