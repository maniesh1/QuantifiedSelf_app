<template>
    <div>
    <div class="nav">
    <router-link to="/">Home</router-link>
    <router-link to="add-tracker">Add Tracker</a></router-link></router-link>
    <router-link to="/about">About</router-link>
    <a href='#' v-on:click="Logout">Logout</a>
    </div>
    
<img class="logo" src="../assets/app_logo.png" /><b>QuantifiedSelf App</b>

    </div>
</template>

<script>
import axios from 'axios'
// import Logout from '@/components/Logout'
export default {
    name: 'Header',
    methods: {
       async Logout(){
            await axios({
                    method: 'get',
                    url: 'http://127.0.0.1:5000/logout'
                    })
                    .then(res => console.log('logged out'))
                    .catch(err => console.log(err));

                    localStorage.clear();
                    this.$router.push({name: 'login'});
        },
        
    },
    mounted() {
        let user = localStorage.getItem('authentication_token');
        if (!user){
            this.$router.push({name: 'login'})
        }
    }
    // components: {
    //     Logout
    // }
}
</script>

<style scoped>

.nav{
    background-color:#333;
    overflow: hidden
}
img{
    width: 100px;
    height: 100px;
}
.nav a {
    float: left;
    color: #f2f2f2f2;
    padding: 14px 16px;
    text-align: center;
    font-size: 17px;
    text-decoration: none;
    margin-right: 5px;
}
.nav a:hover{
    background:#ddd;
    color:#333
}
</style>