<template>
<div id="sign-up">
<img class="logo" src="../assets/app_logo.png" />
<br>
<form>

    <div class="form-group">
    <label  for="name">Name</label>
    <input v-model="name" type="name" class="form-control" id="name" aria-describedby="emailHelp" placeholder="Enter email" required>
  </div>
  <div class="form-group">
    <label for="email">Email address</label>
    <input v-model="email" type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter email" required>
  </div>
  <div class="form-group">
    <label for="password">Password</label>
    <input v-model="password" type="password" class="form-control" id="password" placeholder="Password" required>
    <small>*Password must be at least 6 characters.</small>
  </div>
  <br>
  <button type="submit" class="btn btn-primary" v-on:click="SignUp">Submit</button>
</form>
<br>
<br>
<centre>Already a user: <router-link to="/login">Login</router-link></centre>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'SignUp',
    data()
    {
        return {
            name: '',
            email: '',
            password: ''
        }
    },
    methods: {
        async SignUp(){
            if (this.name=="" || this.email=="" || this.password=="" ){
                // alert('Please fill the required fields.')
            }
           
            else { let result = await axios({
                    method: 'post',
                    url: 'http://127.0.0.1:5000/register',
                    data: {
                        email: this.email,
                        password: this.password
                    }
                    })
                    .catch( err => {
                        if (err.response){
                            console.log(err.response.data);
                            console.log(err.response.data.response.errors);
                            console.log(err.response.status);
                            console.log(err.response.headers);
                        }
                    })
                    if (result.status == 200){
                        this.$router.push({name: 'login'})
                    }

            }
            
        }
    },
    mounted() {
        let user = localStorage.getItem('authentication_token');
        if (user){
            this.$router.push({name: 'home'})
        }
    }
}
</script>

<style>
form {
    text-align: center;
    background-color: white;
    
    display: inline-block;
    width: 400px;
    margin: 0 10px;
    border-radius: 8px;
    padding: 20px 40px;
    box-shadow: 0 10px 25px rgba(92, 99, 105, .2);

}
img {
    height: 200px;
}
</style>