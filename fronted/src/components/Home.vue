<template>
<div id="home">
<h1>
<Header></Header>
Hello there👋, Welcome!
<div class="container">

    <h1><b>Task Trackers</b></b></h1>
   
    <h6><small><input type="file" @change="uploadFile" ref="file"/></small></h6></input>
    <button type="button" class="btn btn-info" v-on:click="upload_tracker()">Import⬆️</button> | <button type="button" class="btn btn-info" v-on:click="downloadCSVData1(); downloadCSVData()">Export⬇️</button>  
    
    
    <br>
    <br>
    <table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Tracker type</th>
      <th scope="col">Description</th>
      <th scope="col">Date</th>
      <th scope="col">Actions</th>

    </tr>
  </thead>
  <tbody>
   <tr v-for="tracker in trackers" :key="tracker.id">
    
    <td ><router-link :to="'/logs/'+tracker.name">{{tracker.name}}</router-link></td>
    <td id='trname'>{{tracker.tracker_type}}</td>
    <td id='desc'>{{tracker.description}}</td>
    <td id="dat">{{tracker.date_created}}</td>
    <td><router-link :to="'/update-tracker/'+tracker.id">Update</router-link> | <button class="delete" v-on:click="deleteTracker(tracker.id)">Delete</button></td>
    </tr>

  </tbody>
</table>

   
</header>
</div>
</h1>
</div>
</template>

<script>
import Header from '@/components/Header'
import Button from '@/components/Button'
import axios from 'axios'

export default {
    name: 'Home',
    components: {
        Header,
        Button,
        
    },
    data(){
        return {
            email: "",
            name: "",
            trackers: [],
            csv_file: null,
        }
    },
    methods:{
        async deleteTracker(id){
      if (confirm('Are you Sure? \n This will delete all log of this tracker!!!')){
        const res = await fetch(`http://127.0.0.1:5000/api/tracker/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-type': 'application/json',
            'Authentication-Token': localStorage.getItem('authentication_token')
          }
        })
        res.status == 200 ? (this.trackers= this.trackers.filter((task) =>task.id != id )) : alert('Error')
      }
    },
      downloadCSVData1() {

    let csv = 'Id,Name,Description,Tracker_Type,Date,Settings\n';
    this.trackers.forEach((row) => {
      console.log(Object.values(row))
            csv += Object.values(row).join(',');
            csv += "\n";
    });
 
    const anchor = document.createElement('a');
    anchor.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
    anchor.target = '_blank';
    anchor.download = 'tracker.csv';
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
      uploadFile() {
        this.csv_file = this.$refs.file.files[0];
      },
       upload_tracker(){
          const formData = new FormData();
        formData.append('file', this.csv_file);
            // form=this.e.form
            // var input = document.querySelector('input[type="file"]')
            // var input = document.getElementById('upload')
            // input.submit()

            // form = document.getElementById('upload')
            // formData.append( 'method', this.form.method );
            //   formData.append( 'icon', this.form.icon );
          const headers = { 'Content-Type': 'multipart/form-data',
          'Authentication-Token': localStorage.getItem('authentication_token')
           };
        axios.post('http://127.0.0.1:5000/api/tracker_upload', formData, { headers }).then((res) => {
          res.data.files; // binary representation of the file
          res.status; // HTTP status
        });
          // this.$router.go()
      }
      
      },
    props:{
        showAddTask: Boolean,
    },
    
    async mounted() {
        let user = localStorage.getItem('authentication_token');
        
        // formData.append( 'method', this.form.method );
        // formData.append( 'icon', this.form.icon );
        // this.email = JSON.parse(user).email;
        if (!user){
            this.$router.push({name: 'login'})
        }
        let result = await fetch('http://127.0.0.1:5000/api/trackers', { credentials: 'same-origin', 
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'Authentication-Token': localStorage.getItem('authentication_token'),
                                        }})
                                .then(r => r.json())
                                .then(data => {
                                    this.trackers=data;
                                    console.log(this.content.data)
                                })
                               
                              
    },
    
}
</script>

<style scoped>

/* @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400&display=swap'); */

* {
  box-sizing: border-box;
}

.container {
  max-width: 1000px;
  margin: 50px auto;
  overflow: auto;
  min-height: 300px;
  border: 2px solid steelblue;
  
  border-radius: 15px;
}
.delete{
    color: 'red';
}
.btn btn-info{
  width: 80px;
  height: 40px;
}

.td{
    width:160px;
    height:40px;
}
th{
    font-size: 25px;
    align-items: center;
}
td{
    
    font-size: 25px
}
#desc {
    font-size: 18px;
}
#trname {
    font-size: 18px;
}
#dat {
    font-size: 18px;
}
button{
    width: 80px;
    height: 40px
}



</style>