<template>
<div id="login">
<div class="login">
    <form>
  <!-- Email input -->
  <div class="form-outline mb-4">
    <input type="email" v-model="email" id="form2Example1" class="form-control" placeholder="Email Address"/>
  </div>

  <!-- Password input -->
  <div class="form-outline mb-4">
    <input type="password" v-model="password" id="form2Example2" class="form-control" placeholder="Password"/>
  </div>


  <!-- Submit button -->
  <button type="button" v-on:click="login" class="btn btn-primary btn-block mb-4">Sign in</button>

  <!-- Register buttons -->
  <div class="text-center">
    <p>Not a member? <router-link to='/signup'>Register</router-link></p>
    

    <button type="button" class="btn btn-link btn-floating mx-1">
      <i class="fab fa-google"></i>
    </button>
  </div>
</form>
</div>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Login',
    data(){
        return {
            email:"",
            password:""
        }
    },
    methods: {
        async login(){
            let result = await axios({
                method: 'post',
                url: 'http://127.0.0.1:5000/login?include_auth_token',
                data: {
                    email: this.email,
                    password: this.password
                    }
            })
            .then(res => {
                localStorage.setItem("authentication_token", res.data.response.user.authentication_token)
                this.$router.push({name: 'home'})
                // console.log(res.data.response.user.authentication_token)
            })
            .catch(err => {
                if (err.response){
                    console.log(err.response.status)
                    console.log(err.response.data.response.errors)
                }
            })
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