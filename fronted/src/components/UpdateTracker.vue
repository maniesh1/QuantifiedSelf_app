<template>
<div>
<Header></Header>
  <form class="add-form">
    <div class="form-control">
      
    </div>
    <div class="form-control">
      <label>Description</label>
      <input
        type="text"
        v-model="tracker.description"
        name="description"
        placeholder="Add Something"
      />
    </div>
    <div class="form-control">
      <label>Tracker Type</label>
      <select v-model="tracker.tracker_type" name="tracker_type">
        <option selected value="">--Please choose an option--</option>
        <option>Numerical</option>
        <option>Multiple Choice</option>
        <Option>Time Duration</Option>
        <Option>Boolean</Option>
      </select>
    </div>
    <div class="form-control">
      <label>Settings</label>
      <input type="text" v-model="tracker.Settings" name="Settings" />
      <small>*enter as comma separated value.</small>
    </div>

    <button type="button" v-on:click="updateTracker" class="btn btn-primary">Save Tracker</button>
  </form>
  </div>
</template>

<script>
import Header from '@/components/Header'
import axios from 'axios'
export default {
  name: 'UpdateTracker',
  components: {
    Header
  },
  data() {
        return{
          tracker: {
            description: '',
            tracker_type: '',
            settings: ''
          }
            
        }
    },
    methods: {
      async updateTracker(){
        const result = await axios.put('http://localhost:5000/api/tracker/'+this.$route.params.id,{
          
          description:this.tracker.description,
          tracker_type:this.tracker.tracker_type,
          settings:this.tracker.settings},{
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('authentication_token')
          },
          
        });
        if (result.status == 200){
          this.$router.push({name:'home'})
        }
        console.log(result)
      },
        onSubmit(e){
            e.preventDefault()

        if (!this.name) {
            alert('Please add a task')
            return
        }

        if (this.tracker_type=="") {
          alert('Please select a appropriate tracker_type')
        }

        const newTask = {
            // id: Math.floor(Math.random() * 100000),
            
            description: this.description,
            tracker_type: this.tracker_type,
            settings: this.settings
        }

        this.$emit('add-task', newTask)

        
        this.description = ''
        this.tracker_type = false
        this.settings= ''

        }
    }, 
                       
    }

</script>