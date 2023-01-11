<template>
<div>
  <Header></Header>
  <form class="add-form">
    <div class="form-control">
      
    </div>
    <div class="form-control">
      <label>Timestamp</label>
      <input
        type="text"
        v-model="log.timestamp"
        name="timestamp"
        placeholder="21/09/2022, 19:45:37"
      />
    </div>
    <div class="form-control">
      <label>Value</label>
      <input v-model="log.value" name="value"/>
    </div>
    <div class="form-control">
      <label>Note</label>
      <input type="text" v-model="log.note" name="note" />
    </div>

    <button type="button" v-on:click="updateLog" class="btn btn-primary">Save Log</button>
  </form>
  </div>
</template>

// <script>
import Header from '@/components/Header'
import axios from 'axios'
export default {
  name: 'UpdateLog',
  components: {
    Header
  },
  data() {
        return{
          log: {
            timestamp: '',
            value: '',
            note: ''
          }
            
        }
    },
    methods: {
      async updateLog(){
        const result = await axios.put('http://localhost:5000/api/log/'+this.$route.params.id,{
          
          timestamp:this.log.timestamp,
          value:this.log.value,
          note:this.log.note},{
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

        if (!this.value) {
            alert('Please add a value')
            return
        }

        if (!this.timestamp) {
          alert('Please write time')
        }


        }
    }, 
                       
    }

</script>