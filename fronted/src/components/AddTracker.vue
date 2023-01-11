<template>
<div>
<Header></Header>
  <form @submit="onSubmit" class="add-form">
    <div class="form-control">
      <label>Task</label>
      <input type="text" v-model="tracker.name" name="name" placeholder="Add Task" />
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
      <small>*enter as space separated value.</small>
    </div>

    <button type="button" v-on:click="addTracker" class="btn btn-primary">Save Tracker</button>
  </form>
  </div>
</template>

<script>
import Header from '@/components/Header'
import axios from 'axios'
export default {
    name: "AddTask",
    components: {
      Header
    },
    data() {
        return{
          tracker: {
            name: '',
            description: '',
            tracker_type: '',
            settings: ''
          }
            
        }
    },
    methods: {
      async addTracker(){
        const result = await axios.post("http://localhost:5000/api/tracker",{
          name:this.tracker.name,
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
            name: this.name,
            description: this.description,
            tracker_type: this.tracker_type,
            settings: this.settings
        }

        this.$emit('add-task', newTask)

        this.name = ''
        this.description = ''
        this.tracker_type = false
        this.settings= ''

        }
    },
}
</script>


<style scoped>
.add-form {
  margin-bottom: 40px;
}

.form-control {
  margin: 20px 0;
}

.form-control label {
  display: block;
}

.form-control input {
  width: 100%;
  height: 40px;
  margin: 5px;
  padding: 3px 7px;
  font-size: 17px;
}

.form-control-check {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.form-control-check label {
  flex: 1;
}

.form-control-check input {
  flex: 2;
  height: 20px;
}
</style>
