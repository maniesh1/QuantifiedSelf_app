<template>
<div>

<Header />
    <br><br>
    
    <h1><b><u>Logs</u></b></h1>
    <button @click="toggle_show">Add Log</button>
    <br><br>
    <button type="button" class="btn btn-info" v-on:click="downloadCSVData1(); downloadCSVData()"><h4><center>Export⬇️</center></h4></button>
    <br>

    <div v-if="show_form">
    <AddLog @add-log="addLog" />
    </div>
    <br>
    <br>
    <div class="container">
    <br>
    <table class="table table-dark">
  <thead class="thead-dark">
    <tr>
      <th scope="col">Logged Time</th>
      <th scope="col">Value</th>
      <th scope="col">Note</th>
      <th scope="col">Actions</th>

    </tr>
  </thead>
  <tbody>
    <tr v-for="log in logs" :key="log.id">
      <th scope="row">{{log.timestamp}}</th>
      <td>{{log.value}}</td>
      <td>{{log.note}}</td>
      <td><router-link :to="'/update-log/'+log.id">Update</router-link> | <button class="delete" v-on:click="deleteLog(log.id)">Delete</button></td>
    </tr>
  </tbody>
</table>
<h2>Log Stats</h2>
<!--<button @click="ShowStats">Show Stats</button>--></button>
<div>
  <canvas id="myChart" style="position: relative; height:40vh; width:80vw"></canvas>
</div>
</div>
</div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

import axios from 'axios'
// import Chart from 'chart.js'
import Header from '@/components/Header'
import AddLog from '@/components/AddLog'

export default {
    name: 'Logs',
    components: {
        Header,
        AddLog
    },
    data(){
        return{
            tracker_name: "",
            logs: [],
            show_form: false,

        }
    },
    methods: {
      ShowStats(){

        
        console.log('stats')
      },
        toggle_show(){
            this.show_form=!this.show_form
            console.log(this.show_form)
        },
        async addLog(task){
      const res = await fetch('http://127.0.0.1:5000/api/log',{
        method: 'POST',
        headers: {
          'Content-type': 'application/json',
          'Authentication-Token': localStorage.getItem('authentication_token')
        },
        body: JSON.stringify(task),
      })
      const data= await res.json()
      console.log(data)
    },
    async deleteLog(id){
      
        const res = await fetch(`http://127.0.0.1:5000/api/log/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-type': 'application/json',
            'Authentication-Token': localStorage.getItem('authentication_token')
          }
        })
        res.status == 200 ? (this.logs= this.logs.filter((task) =>task.id != id )) : alert('Error')
      
    },
      downloadCSVData1() {
    let csv = 'Id,User_Id,Date,Time,Value,Note,Tracker_Name\n';
    this.logs.forEach((row) => {
      console.log(Object.values(row))
            csv += Object.values(row).join(',');
            csv += "\n";
    });
 
    const anchor = document.createElement('a');
    anchor.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
    anchor.target = '_blank';
    anchor.download = 'logs_data.csv';
    anchor.click();
},
  async downloadCSVData(){
      const res =  await fetch('http://127.0.0.1:5000/api/export', {
          method: 'GET',
          headers: {
            'Content-type': 'application/json',
            'Authentication-Token': localStorage.getItem('authentication_token')
          }
        })
        res.status == 200 ? ("ok") : alert('Error')
      },
    },
    async mounted() {
        name=this.$route.params.name;
        let user = localStorage.getItem('authentication_token');
        // this.email = JSON.parse(user).email;
        if (!user){
            this.$router.push({name: 'login'})
        };
        let result = await fetch(`http://127.0.0.1:5000/api/log/${name}`, { credentials: 'same-origin', 
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'Authentication-Token': localStorage.getItem('authentication_token'),
                                        }})
                                .then(r => r.json())
                                .then(data => {
                                    this.logs=data;
                                    // console.log(data)
                                });
                                console.log('log value list: ', [this.logs.map((log)=> log.timestamp)])
                                console.log(this.show_form);
                               
                                const ctx = document.getElementById('myChart');
                                const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: this.logs.map((log)=> log.timestamp),
        datasets: [{
            label: '# Value vs Time',
            data: this.logs.map((log)=> log.value),
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
myChart;
    }

}
</script>

<style>
.container {
  max-width: 700px;
  margin: 50px auto;
  overflow: auto;
  min-height: 300px;
  border: 2px solid steelblue;
  
  border-radius: 15px;
}
#myChart{
  width : 50px;
}
chart.canvas.parentNode.style{height: 128px;}
chart.canvas.parentNode.style{width : 128px;}
</style>