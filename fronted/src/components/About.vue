<template>
<div id="about">
<Header></Header>
<div class="container">
<div class="logo"><a href="/api/trackers">QuantifiedSelf<span>App.</span></a></div>
<h3> <blockquote class="blockquote">
  <p>Track your habits.</p>
</blockquote>
</h3>
<br>
<br>

<div class="row">
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h4 class="card-title"><b>Trackers</b></h4>
        <p class="card-text">A user can create as many trackers as he/she wants as per his/her daily habits. Created trackers can be updated and delated later.</p>
        
      </div>
    </div>
  </div>
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h4 class="card-title"><b>Logs</b></h4>
        <p class="card-text">For any habit tracker already created, a user can enter the logs/values at any time, system automatically captures the current time, this can also be updated or deleted later. </p>
      </div>
    </div>
  </div>
</div>
<br><br>
<div class="row">
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h4 class="card-title"><b>Daily Reminder</b></h4>
        <p class="card-text">If any of the user didn't logged any value for any trackers, he/she will get one reminder to log.</p>                               
        
      </div>
    </div>
  </div>
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h4 class="card-title"><b>Monthly Report</b></h4>
        <p class="card-text">An email will be sent to each user on the first day of every month this report will contain the information about trackers of since the last month.</p>
      </div>
    </div>
  </div>
</div>
<br><br>
<div class="row">
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h4 class="card-title"><b>Token Based Authentication</b></h4>
        <p class="card-text">Safe and highly user friendly with token based authentication. No need to login again and again, token will automatically expire if the user hits logout button.</p>                               
        
      </div>
    </div>
  </div>
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h4 class="card-title"><b>Caching</b></h4>
        <p class="card-text">To make the process smooth and to have lesser work on server side caching has been used in get request of tracker for short span.</p>
      </div>
    </div>
  </div>
</div><br><br>
<div class="row">
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h4 class="card-title"><b>Export</b></h4>
        <p class="card-text">A user can export data to download to their local system also user will get an email confirmation, saying your data have been exported. </p>                               
        
      </div>
    </div>
  </div>
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h4 class="card-title"><b>Import</b></h4>
        <p class="card-text"> A User can make upload the tracker information data from their csv file.</p>
      </div>
    </div>
  </div>
</div>
<br>
<br>
</div>
</div>


</div>

</div>

</template>

<script>
import Header from '@/components/Header'
export default {
    name: 'About',
    components : {
        Header
    }
}
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 50px auto;
  overflow: auto;
  min-height: 500px;
  border: 2px solid steelblue;
  
  border-radius: 15px;
}
.logo a{
    color: #000000;
    font-size: 35px;
    font-weight: 600;
}
.logo a span{
    color: #323c96;
    transition: all 0.3s ease;
}

</style>