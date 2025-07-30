<script>
import SummaryChart from "./SummaryChart.vue"

export default {
  components: {
    SummaryChart
  }
}
</script>





<template>
  <div class="main-content">
       <div class="header--wrapper">
        <div class="header--title">
          <span>Welcome User</span>
          <h2>Dashboard</h2>
        </div>
        <div class="user--info">
          <div class="search--box">
            <RouterLink to="/user/lot_search" class="btn-export">Lots</RouterLink>
          </div>
        </div>
      </div>
      
  
  <div class="p-6">
    <div class="row">
      <SummaryChart endpoint="http://localhost:5000/api/user/lots_by_status" />
      <SummaryChart endpoint="http://localhost:5000/api/user/most_used_lot" />
        
    </div>
  </div>
  </div>
</template>