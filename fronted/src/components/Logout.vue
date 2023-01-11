<template>
<div id="logout">
<button type="submit" v-on:click="Logout">Logout</button>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Logout',
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
        mounted() {
        let user = localStorage.getItem('authentication_token');
        if (user==null){
            this.$router.push({name: 'login'})
        }
    }
    }
}
</script>

<style scoped>
button{
    background-color:#333;
    overflow: hidden;
    color: #f2f2f2f2;
    padding: 14px 16px;
    text-align: center;
    font-size: 17px;
    text-decoration: none;
    margin-right: 5px;
}
button:hover{
    background:#ddd;
    color:#333
}
</style>