<template>
  <form @submit="onSubmit" class="add-form">
    <div class="form-control">
      <label>Tracker Name</label>
      <input type="text" v-model="tracker_name" name="tracker_name" placeholder="Tracker Name" />
    </div>
    <div class="form-control">
      <label>Value</label>
      <input
        type="text"
        v-model="value"
        name="value"
        placeholder="Enter the value"
      />
    </div>
    <div class="form-control">
      <label>Note</label>
      <input v-model="note" name="note" placeholder="Enter a value note"/>
        
    </div>

    <input type="submit" value="Save Task" class="btn btn-block" />
  </form>
</template>

<script>
export default {
    name: "AddLog",
    data() {
        return{
            tracker_name: '',
            value: '',
            note: '',
        }
    },
    methods: {
        onSubmit(e){
            e.preventDefault()

        if (!this.tracker_name) {
            alert('Please add tracker_name')
        }

        if (this.value=="") {
          alert('Value is must')
        }

        const newLog = {
            // id: Math.floor(Math.random() * 100000),
            tracker_name: this.tracker_name,
            value: this.value,
            note: this.note,
        }

        this.$emit('add-log', newLog)

        this.tracker_name = ''
        this.value = ''
        this.note = ''

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
