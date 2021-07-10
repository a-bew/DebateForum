


    // document.getElementsByTagName('h1')[0].style.display = 'none';
    var server = "http://127.0.0.1:5000";

    function loginNow() {
        const appdir = '/login';
        const username = $("#username").val();
        const password = $("#password").val();
        console.log(email, username, password);

        fetch("/login", {
            method: "post",
            headers: {
              "Content-Type": "application/json"
            },
            body:JSON.stringify({username, password})
          }).then(function(response) 
        {

          return response.json();
        }).then(function(response) 
        {
           console.log(response);
        })
    }

    function submitReg() {
        const appdir = '/register';
        const email = $('#email').val();
        const username = $("#username").val();
        const password = $("#passw").val();

        console.log(email, username, password);
        fetch("/register", {
            method: "post",
            headers: {
              "Content-Type": "application/json"
            },
            body:JSON.stringify({username, password, email})
          }).then(function(response) 
        {

          return response.json();
        }).then(function(response) 
        {

           console.log(response);
        })



        // $.ajax({
        //     type: "POST",
        //     url: server+appdir,
        //     data: JSON.stringify({username, password, email}),
        //     dataType: 'json '
        // }).done(function(data) {
        //     console.log('data', data                                                                                                                                                        );
        //     // populate User Profile
        //     // $("welcomeMessage").val(`Welcome ${data.user.name})
        // })

    }

    function showRegister() {
        // hide login
        document.getElementById("loginForm").style.display = 'none';

                // show login
        document.getElementById("registerForm").style.display = 'block';
    }

    function showLogin(){
        // hide login
        document.getElementById("loginForm").style.display = 'block';

        // show login
        document.getElementById("registerForm").style.display = 'none';
    }

    showLogin();
